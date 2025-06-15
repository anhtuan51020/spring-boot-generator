import re

from sqlglot import exp, parse
from sqlglot.expressions import Create, ForeignKey
from pathlib import Path
from spring_boot_generator.generators.from_object_to_java import generate_single_entity
from spring_boot_generator.generators.sql_mapper import (
    from_table_to_class_name,
    process_columns,
    from_column_name_to_java_field_name, from_table_name_to_class_name
)


def parse_sql(sql_content: str) -> list:
    statements = parse(sql_content, read="postgres")
    tables = []
    comment_map = extract_comments(statements)

    for stmt in statements:
        if isinstance(stmt, Create):
            table_expr = stmt.this
            table_name = None
            if hasattr(table_expr, "this") and hasattr(table_expr.this, "name"):
                table_name = table_expr.this.name
            elif hasattr(table_expr, "name"):
                table_name = table_expr.name

            columns = extract_columns(stmt, comment_map, table_name)
            foreign_keys = extract_foreign_keys(stmt)

            tables.append({
                "name": table_name,
                "columns": columns,
                "foreign_keys": foreign_keys,
                "comment": comment_map.get(table_name, {}).get("_table")
            })

    return tables


def extract_columns(stmt: exp.Create, comment_map: dict, table_name: str) -> list[dict]:
    columns = []

    for column_def in stmt.find_all(exp.ColumnDef):
        col_name = column_def.name
        kind = column_def.args.get("kind")
        data_type = kind.sql() if kind else "unknown"

        # Extract length if exists (e.g., varchar(50))
        length_match = re.search(r"\((\d+)\)", data_type)
        length = int(length_match.group(1)) if length_match else None

        # Normalize type name
        type_lower = data_type.lower().split("(")[0]

        # columnDefinition override if needed
        column_definition = None
        if type_lower in {"text", "json", "jsonb", "uuid"} or "(" not in data_type:
            column_definition = data_type

        # Extract constraints
        constraints = {
            "not_null": False,
            "unique": False,
            "primary_key": False,
            "default": None
        }

        for constraint in column_def.args.get("constraints", []):
            sql_text = constraint.sql().upper()

            if "NOT NULL" in sql_text:
                constraints["not_null"] = True
            elif "PRIMARY KEY" in sql_text:
                constraints["is_primary"] = True
                constraints["not_null"] = True
            elif "UNIQUE" in sql_text:
                constraints["unique"] = True
            elif sql_text.startswith("DEFAULT"):
                default_val = sql_text.split("DEFAULT", 1)[1].strip()
                constraints["default"] = default_val

        nullable = not constraints.get("not_null", False)

        columns.append({
            "name": col_name,
            "type": data_type,
            "length": length,
            "column_definition": column_definition,
            "nullable": nullable,
            "comment": comment_map.get(table_name, {}).get(col_name),
            **constraints
        })

    return columns


def extract_foreign_keys(stmt: exp.Create) -> list[dict]:
    foreign_keys = []

    for fk in stmt.find_all(ForeignKey):
        local_columns = fk.args.get("expressions") or []
        reference = fk.args.get("reference")
        if not local_columns or not reference:
            continue

        local_column = local_columns[0].sql()

        # Cố gắng lấy bảng và cột bằng sqlglot
        target_table = None
        target_column = None

        if reference.this and "(" in reference.this.sql():
            # Nếu không parse được, xử lý thủ công
            raw = reference.this.sql()
            match = re.match(r"(\w+)\s*\(\s*(\w+)\s*\)", raw)
            if match:
                target_table, target_column = match.groups()
        else:
            target_table = reference.this.sql() if reference.this else None
            target_columns = reference.expressions or []
            target_column = target_columns[0].sql() if target_columns else None

        foreign_keys.append({
            "column": local_column,
            "target_table": target_table,
            "target_column": target_column,
            "target_class": from_table_to_class_name(target_table) if target_table else None,
        })
    return foreign_keys


def extract_comments(statements: list[exp.Expression]) -> dict:
    comments = {}

    for stmt in statements:
        if not isinstance(stmt, exp.Comment):
            continue

        kind = stmt.args.get("kind")
        target = stmt.args.get("this")
        comment_expr = stmt.args.get("expression")

        if not (kind and target and comment_expr):
            continue

        kind = kind.lower()
        comment = comment_expr.name

        if kind == "table":
            table_name = target.name if hasattr(target, "name") else str(target)
            comments.setdefault(table_name, {})["_table"] = comment


        elif kind == "column":
            if isinstance(target, exp.Column):
                # Nếu là Column, lấy tên bảng và cột từ Column
                table_name = target.table
                col_name = target.name
            elif isinstance(target, exp.Dot):
                # Nếu là Dot expression, lấy tên bảng và cột từ các phần tử
                table_name = target.this.name if isinstance(target.this, exp.Identifier) else None
                col_name = target.expression.name if isinstance(target.expression, exp.Identifier) else None
            else:
                # Nếu không phải Column hay Dot, không xử lý
                table_name, col_name = None, None
            if table_name and col_name:
                # Lưu comment cho cột
                comments.setdefault(table_name, {})[col_name] = comment

    return comments


def build_referenced_map(tables: list) -> dict:
    """
    Xây dựng map từ tên bảng đến danh sách các bảng tham chiếu.
    """

    referenced_map = {}

    for table in tables:
        referenced_map[table["name"]] = []

    for table in tables:
        for fk in table.get("foreign_keys", []):
            target_table = fk["target_table"]
            if target_table == "tbl_user":
                continue
            if target_table in referenced_map:
                source_field = from_column_name_to_java_field_name(fk["column"]).removesuffix("Id")
                source_class = from_table_to_class_name(table["name"])
                field_name = from_table_name_to_class_name(table["name"]) + "List"
                referenced_map[target_table].append({
                    "source_table": table["name"],
                    "source_column": fk["column"],
                    "source_field": source_field,
                    "source_class": source_class,
                    "field_name": field_name,
                })
    return referenced_map


def generate_entity_from_sql(
        sql_path: Path,
        project_dir: Path,
        base_package: str,
        extend_from_base_entity: bool = True,
):
    sql_content = sql_path.read_text()
    tables = parse_sql(sql_content)
    referenced_map = build_referenced_map(tables)

    for table in tables:
        context = {
            "table_name": table["name"],
            "class_name": from_table_to_class_name(table["name"]),
            "fields": process_columns(table["columns"], table["foreign_keys"]),
            "foreign_keys": table["foreign_keys"],
            "referenced_by": referenced_map[table["name"]],
            "comment": table["comment"],
            "has_is_deleted": any(col["name"] == "is_deleted" for col in table["columns"]),
        }
        for field in context["fields"]:
            if field.get("is_primary"):
                context["id_type"] = field["type"]
                break

        generate_single_entity(
            context,
            project_dir,
            base_package,
            extend_from_base_entity
        )

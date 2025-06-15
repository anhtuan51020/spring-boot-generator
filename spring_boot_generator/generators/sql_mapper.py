from typing import Optional
import re

def from_table_to_class_name(table_name: str) -> str:
    name = re.sub(r'^tbl_', '', table_name)
    return ''.join(p.capitalize() for p in name.split('_'))

def from_table_name_to_class_name(table_name: str) -> str:
    table_name = re.sub(r'^tbl_', '', table_name)
    parts = table_name.lower().split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

def from_column_name_to_java_field_name(column_name: str) -> str:
    s = re.sub(r'_([a-z])', lambda m: m.group(1).upper(), column_name.lower())
    return s[0].lower() + s[1:] if s else s

def extract_column_type_length(sql_type: str) -> Optional[int]:
    match = re.search(r'\((\d+)\)', sql_type)
    if match:
        return int(match.group(1))
    return None

def from_sql_type_to_java_type(sql_type: str) -> str:
    sql_type = sql_type.lower()
    if 'serial' in sql_type or 'int' in sql_type:
        return 'Integer'
    if 'bigint' in sql_type:
        return 'Long'
    if 'varchar' in sql_type or 'text' in sql_type:
        return 'String'
    if 'timestamp' in sql_type or 'datetime' in sql_type:
        return 'LocalDateTime'
    if 'date' in sql_type:
        return 'LocalDate'
    if 'boolean' in sql_type:
        return 'Boolean'
    return 'Object'

def camel_to_kebab(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()

def process_columns(columns, foreign_keys):
    fk_map = {
        fk["column"]: fk for fk in foreign_keys
    }

    fields = []

    for col in columns:
        field_name = from_column_name_to_java_field_name(col["name"])
        java_type = from_sql_type_to_java_type(col["type"])

        is_fk = col["name"] in fk_map
        fk_info = fk_map.get(col["name"]) if is_fk else {}

        field = {
            "name": field_name,
            "original_name": col["name"],
            "type": (
                from_table_to_class_name(fk_info["target_table"])
                if is_fk else java_type
            ),
            "nullable": col.get("nullable", True),
            "unique": col.get("unique", False),
            "is_primary": col.get("is_primary", False),
            "comment": col.get("comment", None),
            "length": col.get("length", None),
            "is_relationship": is_fk,
            "relation_type": "ManyToOne" if is_fk else None,
            "related_table": fk_info["target_table"] if is_fk else None,
            "related_column": fk_info["target_column"] if is_fk else None,
        }
        fields.append(field)
    return fields

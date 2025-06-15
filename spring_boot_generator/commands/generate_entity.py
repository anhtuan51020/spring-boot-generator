import typer
from pathlib import Path
from spring_boot_generator.core.entity_generator import generate_entity_from_sql

generate_app = typer.Typer(help="🔧 Các lệnh generate")

@generate_app.command("entity")
def generate_entity_command(
    sql_file: Path = typer.Option(..., "--sql-file", "-s", help="Path tới file chứa SQL CREATE TABLE."),
    output: Path = typer.Option(..., "--output", "-o", help="Thư mục gốc project Spring Boot."),
    base_package: str = typer.Option(..., "--package", "-p", help="Package gốc, ví dụ: com.mdm"),
    extend_from_base_entity: bool = typer.Option(False, "--extend-from-base-entity", "-e", help="Kế thừa từ class base.")
):
    """
    🧬 Sinh Entity, DTO, Mapper, Repository, Service, Controller từ file SQL CREATE TABLE (PostgreSQL).
    """
    generate_entity_from_sql(
        sql_path=sql_file,
        project_dir=output,
        base_package=base_package,
        extend_from_base_entity=extend_from_base_entity
    )

def register(app: typer.Typer):
    app.add_typer(generate_app, name="generate")

import re
from pathlib import Path
import questionary
import typer
from spring_boot_generator.template_engine import generate_project_structure_from_templates


def init_project(verbose: bool):
    print("\n🚀 Spring Boot Project Generator - Initialization Wizard\n")

    try:
        project_name = questionary.text("Tên project (ví dụ: spring-boot-example)?").ask()
        if not project_name:
            project_name = "spring-boot-example"

        default_package = f"com.{re.sub(r'[^a-zA-Z0-9]', '', project_name)}"

        base_package = questionary.text(f"Package gốc (ví dụ: {default_package})?").ask()
        if not base_package:
            base_package = default_package

        database = questionary.select(
            "Chọn loại database:",
            choices=["postgresql", "mysql", "mariadb"]
        ).ask()
        if database is None:
            raise typer.Exit(code=1)

        project_path = Path.cwd() / project_name
        if project_path.exists():
            overwrite = questionary.confirm(
                f"Thư mục '{project_name}' đã tồn tại. Ghi đè?"
            ).ask()
            if overwrite is None or not overwrite:
                typer.echo("❌ Hủy tạo project.")
                raise typer.Exit(code=1)

        context = {
            "j2_project_name": project_name,
            "j2_base_package": base_package,
            "j2_base_package_path": base_package.replace(".", "/"),
            "j2_database_type": database
        }

        generate_project_structure_from_templates(context, verbose)

        typer.echo(f"\n✅ Đã tạo project '{project_name}' tại: {project_path.resolve()}\n")

    except KeyboardInterrupt:
        typer.echo("\n❌ Đã hủy bởi người dùng.")
        raise typer.Exit(code=1)

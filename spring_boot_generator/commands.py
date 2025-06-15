import typer
from spring_boot_generator.init_logic import init_project

app = typer.Typer(help="Spring Boot Project Generator CLI")

@app.command("new")
def new_project(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Hiển thị log chi tiết trong quá trình tạo project")
):
    """
    🎉 Tạo mới một project Spring Boot
    """
    init_project(verbose)

@app.command("version")
def show_version():
    """🔖 Hiển thị thông tin phiên bản của công cụ"""
    typer.echo("📦 Spring Boot Generator v1.0.0")
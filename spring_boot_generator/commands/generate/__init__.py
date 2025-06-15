import typer
from spring_boot_generator.commands.generate_entity import register as register_entity

generate_app = typer.Typer(help="🔧 Các lệnh generate")

def register(app: typer.Typer):
    register_entity(generate_app)
    app.add_typer(generate_app, name="generate")

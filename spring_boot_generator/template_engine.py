import os
import typer
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template

app = typer.Typer()

def pascal_case(s):
    return ''.join(word.capitalize() for word in s.replace('-', ' ').replace('_', ' ').split())

def get_jinja_env(path: Path):
    env = Environment(loader=FileSystemLoader(str(path)))
    env.filters['pascal_case'] = pascal_case
    return env

def render_template_file(template_path, context, output_path, verbose: bool = False):
    env = get_jinja_env(template_path.parent)
    template = env.get_template(template_path.name)
    rendered = template.render(context)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered)

    if verbose:
        output_path_abs = output_path.resolve()
        cwd = Path.cwd().resolve()
        try:
            relative = output_path_abs.relative_to(cwd)
            typer.echo(f"[✔] Đã tạo file: {relative}")
        except ValueError:
            typer.echo(f"[✔] Đã tạo file: {output_path_abs}")

def generate_project_structure_from_templates(context: dict, verbose: bool = False):
    project_name = context["project_name"]
    context["project_name"] = project_name

    template_base = Path(__file__).parent.parent / "templates" / "project"
    output_base = Path(project_name)

    jinja_env = get_jinja_env(template_base)

    typer.echo(f"🔧 Đang tạo project: {project_name}")
    if verbose:
        typer.echo(f"📂 Thư mục template: {template_base}")
        typer.echo(f"📁 Thư mục đầu ra: {output_base}")

    for root, dirs, files in os.walk(template_base):
        for file in files:
            if not file.endswith(".j2"):
                continue

            template_file_path = Path(root) / file
            rel_path = template_file_path.relative_to(template_base)
            output_rel_path = rel_path.with_suffix("")

            output_str_template = jinja_env.from_string(output_rel_path.as_posix())
            output_str = output_str_template.render(context)
            output_file_path = output_base / output_str

            if verbose:
                output_path_abs = output_file_path.resolve()
                cwd = Path.cwd().resolve()
                try:
                    rel_output_path = output_path_abs.relative_to(cwd)
                except ValueError:
                    rel_output_path = output_path_abs

                typer.echo(f"➡  Đang tạo: {template_file_path.name} → {rel_output_path}")

            render_template_file(template_file_path, context, output_file_path, verbose)

    typer.echo(f"\n✅ Project '{project_name}' đã được tạo thành công.")

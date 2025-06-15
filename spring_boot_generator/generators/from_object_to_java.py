from pathlib import Path
import json
import typer

from spring_boot_generator.generators.sql_mapper import camel_to_kebab


def generate(
        context: dict,
        output_dir: Path,
        template_name: str,
        class_name: str,
        extend_from_base_entity: bool = True,
):
    from spring_boot_generator.core.template_engine import render_template_file
    from spring_boot_generator.core.template_engine import get_jinja_env

    project_root = Path(__file__).resolve().parents[2]

    template_dir = project_root / "templates" / "entities" / (
        "extend_from_base" if extend_from_base_entity else "no_extend_from_base")
    env = get_jinja_env(template_dir)

    template = env.get_template(template_name)

    output_path = output_dir / class_name

    render_template_file(
        Path(template.filename),
        context,
        output_path,
        verbose=True
    )
    typer.echo(f"Đã tạo file {output_path} thành công.")

def generate_entity(
        context: dict,
        project_dir: Path, 
        base_package: str,
        extend_from_base_entity: bool = True,
):
    output_dir = project_dir / Path(base_package.replace(".", "/")) / "entity"

    generate(
        context,
        output_dir,
        "Entity.java.j2",
        context['class_name'] + ".java",
        extend_from_base_entity,
    )

def generate_entity_dto(
        context: dict,
        project_dir: Path,
        base_package: str,
        extend_from_base_entity: bool = True,
):
    output_dir = project_dir / Path(base_package.replace(".", "/")) / "dto"
    generate(
        context,
        output_dir,
        "EntityDTO.java.j2",
        context['class_name'] + "DTO.java",
        extend_from_base_entity,
    )


def generate_entity_mapper(
        context: dict,
        project_dir: Path,
        base_package: str,
        extend_from_base_entity: bool = True,
):
    output_dir = project_dir / Path(base_package.replace(".", "/")) / "mapper"
    generate(
        context,
        output_dir,
        "EntityMapper.java.j2",
        context['class_name'] + "Mapper.java",
        extend_from_base_entity,
    )

def generate_entity_repository(
        context: dict,
        project_dir: Path,
        base_package: str,
        extend_from_base_entity: bool = True,
):
    output_dir = project_dir / Path(base_package.replace(".", "/")) / "repository"
    generate(
        context,
        output_dir,
        "EntityRepository.java.j2",
        context['class_name'] + "Repository.java",
        extend_from_base_entity,
    )

def generate_entity_service(
        context: dict,
        project_dir: Path,
        base_package: str,
        extend_from_base_entity: bool = True,
):
    output_dir = project_dir / Path(base_package.replace(".", "/")) / "service"
    generate(
        context,
        output_dir,
        "EntityService.java.j2",
        context['class_name'] + "Service.java",
        extend_from_base_entity,
    )


def generate_entity_service_impl(
        context: dict,
        project_dir: Path,
        base_package: str,
        extend_from_base_entity: bool = True,
):
    output_dir = project_dir / Path(base_package.replace(".", "/")) / "service" / "impl"
    generate(
        context,
        output_dir,
        "EntityServiceImpl.java.j2",
        context['class_name'] + "ServiceImpl.java",
        extend_from_base_entity,
    )


def generate_entity_controller(
        context: dict,
        project_dir: Path,
        base_package: str,
        extend_from_base_entity: bool = True,
):
    output_dir = project_dir / Path(base_package.replace(".", "/")) / "controller"
    context["request_path"] = "/api/v1/" + camel_to_kebab(context["class_name"]) + "s"
    generate(
        context,
        output_dir,
        "EntityController.java.j2",
        context['class_name'] + "Controller.java",
        extend_from_base_entity,
    )


def generate_single_entity(
        context: dict,
        output_dir: Path,
        base_package: str,
        extend_from_base_entity: bool = True,
):
    context['j2_base_package'] = base_package

    generate_entity(
        context,
        output_dir,
        base_package,
        extend_from_base_entity
    )

    generate_entity_dto(
        context,
        output_dir,
        base_package,
        extend_from_base_entity
    )

    generate_entity_mapper(
        context,
        output_dir,
        base_package,
        extend_from_base_entity
    )

    generate_entity_repository(
        context,
        output_dir,
        base_package,
        extend_from_base_entity
    )

    generate_entity_service(
        context,
        output_dir,
        base_package,
        extend_from_base_entity
    )

    generate_entity_service_impl(
        context,
        output_dir,
        base_package,
        extend_from_base_entity
    )

    generate_entity_controller(
        context,
        output_dir,
        base_package,
        extend_from_base_entity
    )
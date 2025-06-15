from setuptools import setup, find_packages

setup(
    name='spring-boot-generator',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click==8.1.3',
        'jinja2==3.1.2',
        'questionary'
        'typer',
        'sqlparse',
        'sqlglot'
    ],
    entry_points={
        'console_scripts': [
            "spring-boot-generator = spring_boot_generator.commands:app"
        ],
    },
)

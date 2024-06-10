import os

import click

from py2flat.parser import Parser
from py2flat.utils import json_dump

CONTEXT_SETTINGS = dict(
    help_option_names=["-h", "--help"],
)


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """CLI"""


@click.command()
@click.argument("source")
@click.option("--schema", "-s", required=True)
@click.option("--output", "-o")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "text"], case_sensitive=False),
    default="json",
)
@click.option(
    "--separator",
    default=", ",
    help="Separator for plain text format.",
)
@click.option("--silent", is_flag=True, default=False)
def parse(source: str, output: str, silent: bool, **options):
    """Parse"""

    parser = Parser.from_file(options["schema"])

    if os.path.isdir(source):
        content = []
        for filepath, res in parser.read_dir(source, silent=silent):
            content.append({"file": filepath, "content": res})
    else:
        content = parser.read_file(source, silent=silent)

    message = f"{len(content)} file(s) found"

    if options["format"] == "json":
        content = json_dump(content)

    if output:
        with open(output, "w", encoding="utf-8") as file:
            file.write(content)
    else:
        click.echo(content)

    click.echo(message)


cli.add_command(parse)

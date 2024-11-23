import sys

import click

from .format import format_clo_string
from .toml_to_clo import toml_to_clo


@click.group()
def cli():
    """~~~~cloacal~~~~~"""
    ...


@cli.command()
@click.option(
    "-f",
    "--file",
    type=click.File("r"),
    default=None,
    help="Input .clo file (reads from stdin if not provided)",
)
@click.option(
    "--width",
    default=44,
    type=int,
    help="Maximum line width (default: 44)",
)
def format(file, width):
    """Format a .clo file."""

    if file:
        input_text = file.read()

    elif not sys.stdin.isatty():
        input_text = sys.stdin.read()

    else:
        click.echo(cli.get_help(click.Context(cli)))

        sys.exit(1)

    formatted_output = format_clo_string(input_text, max_line_length=width)

    click.echo(formatted_output)


@cli.command()
@click.option(
    "-f",
    "--file",
    type=click.File("r"),
    required=True,
    help="Input TOML file",
)
@click.option(
    "--width",
    default=44,
    type=int,
    help="Maximum line width (default: 44)",
)
def toml(file, width):
    """Convert TOML to Cloacal format."""

    toml_input = file.read()

    formatted_output = toml_to_clo(toml_input, max_line_length=width)

    click.echo(formatted_output)


def main():
    cli()


if __name__ == "__main__":
    main()

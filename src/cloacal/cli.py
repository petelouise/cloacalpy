import os
import sys
from pathlib import Path

import click

from .format import format_clo_string
from .toml2clo import toml2clo


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
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    default=None,
    help="Output file path (prints to stdout if not provided)",
    is_flag=False,
    flag_value="",
)
def format(file, width, output):
    """Format a .clo file."""

    if file:
        input_text = file.read()

    elif not sys.stdin.isatty():
        input_text = sys.stdin.read()

    else:
        click.echo(cli.get_help(click.Context(cli)))

        sys.exit(1)

    formatted_output = format_clo_string(input_text, max_line_length=width)

    if output is None:
        click.echo(formatted_output)
    else:
        output_path = output if output else file.name
        with open(output_path, 'w') as f:
            f.write(formatted_output)


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
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    default=None,
    help="Output file path (prints to stdout if not provided)",
    is_flag=False,
    flag_value="",
)
def toml(file, width, output):
    """Convert TOML to Cloacal format."""

    toml_input = file.read()

    formatted_output = toml2clo(toml_input, max_line_length=width)

    if output is None:
        click.echo(formatted_output)
    else:
        if output:
            output_path = output
        else:
            # Replace .toml extension with .clo
            input_path = Path(file.name)
            output_path = input_path.with_suffix('.clo')
        
        with open(output_path, 'w') as f:
            f.write(formatted_output)


def main():
    cli()


if __name__ == "__main__":
    main()

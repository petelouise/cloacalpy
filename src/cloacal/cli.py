import os
import sys
from pathlib import Path
import glob

import click

from .format import format_str
from .toml2clo import toml2clo


@click.group()
def cli():
    """~~~~cloacal~~~~~"""
    ...


@cli.command()
@click.option(
    "-f",
    "--file",
    type=str,
    default=None,
    help="Input .clo file or glob pattern (reads from stdin if not provided)",
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
        # Handle glob pattern
        input_files = glob.glob(file)
        if not input_files:
            click.echo(f"No files found matching pattern: {file}", err=True)
            sys.exit(1)
        
        for input_file in input_files:
            with open(input_file, 'r') as f:
                input_text = f.read()
            
            formatted_output = format_clo_string(input_text, max_line_length=width)
            
            if output is None:
                # Print with file header if multiple files
                if len(input_files) > 1:
                    click.echo(f"==> {input_file} <==")
                click.echo(formatted_output)
            else:
                if output:
                    # If specific output path and multiple files, append numbers
                    if len(input_files) > 1:
                        base, ext = os.path.splitext(output)
                        output_path = f"{base}_{input_files.index(input_file) + 1}{ext}"
                    else:
                        output_path = output
                else:
                    output_path = input_file
                
                with open(output_path, 'w') as f:
                    f.write(formatted_output)

    elif not sys.stdin.isatty():
        input_text = sys.stdin.read()
        formatted_output = format_clo_string(input_text, max_line_length=width)
        click.echo(formatted_output)

    else:
        click.echo(cli.get_help(click.Context(cli)))
        sys.exit(1)


@cli.command()
@click.option(
    "-f",
    "--file",
    type=str,
    required=True,
    help="Input TOML file or glob pattern",
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

    input_files = glob.glob(file)
    if not input_files:
        click.echo(f"No files found matching pattern: {file}", err=True)
        sys.exit(1)

    for input_file in input_files:
        with open(input_file, 'r') as f:
            toml_input = f.read()

        formatted_output = toml2clo(toml_input, max_line_length=width)

        if output is None:
            # Print with file header if multiple files
            if len(input_files) > 1:
                click.echo(f"==> {input_file} <==")
            click.echo(formatted_output)
        else:
            if output:
                # If specific output path and multiple files, append numbers
                if len(input_files) > 1:
                    base, ext = os.path.splitext(output)
                    output_path = f"{base}_{input_files.index(input_file) + 1}{ext}"
                else:
                    output_path = output
            else:
                # Replace .toml extension with .clo
                input_path = Path(input_file)
                output_path = input_path.with_suffix('.clo')
            
            with open(output_path, 'w') as f:
                f.write(formatted_output)


def main():
    cli()


if __name__ == "__main__":
    main()

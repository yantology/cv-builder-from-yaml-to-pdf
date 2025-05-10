"""Main module for CV Builder.

This module provides the main functionality and CLI for the CV Builder.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from typing import Optional, List, Union

import click
import yaml

from cv_builder_from_yaml_to_pdf.yaml_parser import parse_yaml_file, validate_cv_data
from cv_builder_from_yaml_to_pdf.pdf_generator import generate_cv_pdf
from cv_builder_from_yaml_to_pdf.templates import create_yaml_from_template
from cv_builder_from_yaml_to_pdf.schema import save_schema_to_file, generate_schema_markdown


@click.group()
def cli():
    """CV Builder: Convert YAML files to beautiful PDF CVs."""
    pass


@cli.command('generate')
@click.argument('yaml_file', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
@click.option('--output', '-o', type=click.Path(file_okay=True, dir_okay=False, writable=True),
              help='Output PDF file path.')
@click.option('--style', '-s', type=click.Choice(['classic', 'modern', 'minimal'], case_sensitive=False),
              default='classic', help='Style for the CV (classic, modern, or minimal).')
@click.option('--page-size', '-p', type=click.Choice(['A4', 'letter'], case_sensitive=False),
              default='A4', help='Page size for the PDF (A4 or letter).')
@click.option('--preview', is_flag=True, help='Open the PDF after generation.')
def generate_command(yaml_file: str, output: Optional[str] = None, style: str = 'classic',
                     page_size: str = 'A4', preview: bool = False):
    """Generate a PDF CV from a YAML file.
    
    YAML_FILE: Path to the YAML file containing CV data.
    """
    try:
        # Parse the YAML file
        cv_data_dict = parse_yaml_file(yaml_file)
        
        # Validate the CV data
        validation_result = validate_cv_data(cv_data_dict)
        if validation_result is not True:
            click.echo("Error: The YAML file contains validation errors:", err=True)
            for error in validation_result:
                click.echo(f"  - {error}", err=True)
            sys.exit(1)
        
        # Convert the dictionary to a CV object
        from cv_builder_from_yaml_to_pdf.models import CV
        cv_data = CV.model_validate(cv_data_dict)
        
        # If output is not specified, use the same name as the input file but with .pdf extension
        if not output:
            yaml_path = Path(yaml_file)
            output = str(yaml_path.with_suffix('.pdf'))
        
        # Generate the PDF
        pdf_path = generate_cv_pdf(cv_data, output, style, page_size)
        
        click.echo(f"Successfully generated PDF CV: {pdf_path}")
        
        # Open the PDF if preview is True
        if preview:
            open_pdf(pdf_path)
        
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except yaml.YAMLError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)
        sys.exit(1)


@cli.command('init')
@click.argument('output_file', type=click.Path(file_okay=True, dir_okay=False, writable=True))
@click.option('--template', '-t', type=click.Choice(['default', 'academic', 'minimal']), default='default',
              help='Template to use for the YAML file.')
def init_command(output_file: str, template: str = 'default'):
    """Initialize a new CV YAML file using a template.
    
    OUTPUT_FILE: Path where the YAML file will be saved.
    """
    try:
        # Create the YAML file from the template
        yaml_path = create_yaml_from_template(template, output_file)
        click.echo(f"Successfully created CV YAML file: {yaml_path}")
        click.echo("Edit the file with your information, then use 'cv-builder generate' to create a PDF.")
        
        click.echo("\nAvailable templates for CV initialization:")
        click.echo("  - default: Standard professional CV for software engineers and other tech roles")
        click.echo("  - academic: Academic CV with focus on publications, teaching experience, and research")
        click.echo("  - minimal: Simplified CV format with essential sections only")
        
        click.echo("\nAvailable styles for PDF generation:")
        click.echo("  - classic: Traditional CV style with serif fonts")
        click.echo("  - modern: Contemporary design with blue accents and sans-serif fonts")
        click.echo("  - minimal: Clean, minimalist design with subtle formatting")
        
        click.echo("\nExample usage:")
        click.echo(f"  cv-builder init my-cv.yaml --template academic")
        click.echo(f"  cv-builder generate {output_file} --style modern --page-size A4")
        click.echo(f"  cv-builder generate {output_file} --preview")
        click.echo(f"  cv-builder preview {Path(output_file).with_suffix('.pdf')}")
        
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)
        sys.exit(1)


@cli.command('preview')
@click.argument('pdf_file', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
def preview_command(pdf_file: str):
    """Preview an existing PDF CV file.
    
    PDF_FILE: Path to the PDF file to preview.
    """
    try:
        open_pdf(pdf_file)
    except Exception as e:
        click.echo(f"An error occurred while opening the PDF: {e}", err=True)
        sys.exit(1)


@cli.command('validate')
@click.argument('yaml_file', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
def validate_command(yaml_file: str):
    """Validate a YAML file against the CV schema.
    
    YAML_FILE: Path to the YAML file to validate.
    """
    try:
        # Parse the YAML file
        cv_data = parse_yaml_file(yaml_file)
        
        # Validate the CV data
        validation_result = validate_cv_data(cv_data)
        if validation_result is True:
            click.echo(click.style("✓ Valid CV file - your CV data structure is correct.", fg='green'))
        else:
            click.echo(click.style("✗ Invalid CV file - the following errors were found:", fg='red'))
            for error in validation_result:
                click.echo(click.style(f"  - {error}", fg='red'))
            sys.exit(1)
    except (FileNotFoundError, yaml.YAMLError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command('schema')
@click.option('--output', '-o', type=click.Path(file_okay=True, dir_okay=False, writable=True),
              help='Output file path for the schema (JSON format).')
@click.option('--markdown', '-m', type=click.Path(file_okay=True, dir_okay=False, writable=True),
              help='Output file path for the schema documentation (Markdown format).')
def schema_command(output: Optional[str] = None, markdown: Optional[str] = None):
    """Generate the schema for the CV data model.
    
    This command generates a JSON schema file and/or markdown documentation for the CV data model.
    """
    if output:
        try:
            json_path = save_schema_to_file(output)
            click.echo(f"JSON schema saved to: {json_path}")
        except Exception as e:
            click.echo(f"Error saving JSON schema: {e}", err=True)
            sys.exit(1)
    
    if markdown:
        try:
            md_content = generate_schema_markdown()
            md_path = Path(markdown)
            md_path.parent.mkdir(parents=True, exist_ok=True)
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            click.echo(f"Markdown documentation saved to: {md_path.absolute()}")
        except Exception as e:
            click.echo(f"Error saving markdown documentation: {e}", err=True)
            sys.exit(1)
    
    if not output and not markdown:
        click.echo("Please specify at least one output option: --output or --markdown")
        sys.exit(1)


def open_pdf(pdf_path: str):
    """Open a PDF file with the default PDF viewer.
    
    Args:
        pdf_path: Path to the PDF file
    """
    pdf_path = os.path.abspath(pdf_path)
    
    try:
        # Open PDF with the default application based on the operating system
        if platform.system() == 'Windows':
            os.startfile(pdf_path)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', pdf_path], check=True)
        else:  # Linux and other Unix-like systems
            subprocess.run(['xdg-open', pdf_path], check=True)
        click.echo(f"Opened PDF file: {pdf_path}")
    except Exception as e:
        click.echo(f"Warning: Could not open PDF file: {e}", err=True)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()

"""CV Template Manager module.

This module provides template generation for CVs.
"""

import os
from pathlib import Path
from typing import Dict, Any

import yaml

TEMPLATES_DIR = Path(__file__).parent / "yaml_templates"


def _load_template_content(template_name: str) -> str:
    """Load raw content from a YAML template file."""
    file_path = TEMPLATES_DIR / f"{template_name}.yaml"
    if not file_path.exists():
        raise FileNotFoundError(f"Template file {file_path} not found.")
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def create_sample_cv_yaml(output_path: str = None) -> str:
    """Create a sample CV in YAML format from the default template.
    
    Args:
        output_path: Optional path where to save the sample CV YAML file
        
    Returns:
        Path to the generated sample CV YAML file or dictionary if no output_path
    """
    content = _load_template_content('default')
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return output_path
    else:
        return yaml.safe_load(content)


def create_yaml_from_template(template_name: str, output_path: str) -> str:
    """Create a YAML file from a template.
    
    Args:
        template_name: Name of the template to use
        output_path: Path where the YAML file will be saved
        
    Returns:
        Path to the generated YAML file
        
    Raises:
        ValueError: If the template_name is not valid
        FileNotFoundError: If the template file does not exist
    """
    available_templates = [f.stem for f in TEMPLATES_DIR.glob("*.yaml")]
    if template_name not in available_templates:
        valid_templates = ', '.join(available_templates)
        raise ValueError(f"Invalid template name: {template_name}. Valid templates are: {valid_templates}")
    
    content = _load_template_content(template_name)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return output_path

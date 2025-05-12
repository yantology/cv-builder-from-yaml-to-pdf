"""YAML Parser for CV Builder.

This module handles the parsing of YAML files containing CV data.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Union, List
from pydantic import ValidationError

from cv_builder_from_yaml_to_pdf.models import CV


def parse_yaml_file(file_path: str) -> Dict[str, Any]:
    """Parse a YAML file and return its contents as a dictionary.
    
    Args:
        file_path: Path to the YAML file
        
    Returns:
        Dict containing the parsed YAML data
        
    Raises:
        FileNotFoundError: If the file does not exist
        yaml.YAMLError: If the file cannot be parsed as YAML
    """
    yaml_path = Path(file_path)
    
    if not yaml_path.exists():
        raise FileNotFoundError(f"YAML file not found: {file_path}")
    
    try:
        with open(yaml_path, 'r', encoding='utf-8') as yaml_file:
            data = yaml.safe_load(yaml_file)
        return data
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file: {e}")


def validate_cv_string(yaml_string: str) -> Union[bool, List[str]]:
    """Validates a CV from a YAML string.
    
    Args:
        yaml_string: YAML string containing CV data
        
    Returns:
        True if valid, or a list of validation errors
    """
    try:
        # Parse the YAML string
        data = yaml.safe_load(yaml_string)
        
        # Validate the data
        return validate_cv_data(data)
    except yaml.YAMLError as e:
        return [f"YAML parsing error: {e}"]


def validate_cv_data(data: Dict[str, Any]) -> Union[bool, List[str]]:
    """Validates that the CV data is properly structured using Pydantic models.
    
    Args:
        data: Dictionary containing CV data
        
    Returns:
        True if data is valid, or a list of validation errors if invalid
    """
    try:
        cv = CV.model_validate(data)
        return True
    except ValidationError as e:
        return [f"{err['loc']}: {err['msg']}" for err in e.errors()]

"""Schema utility module for CV Builder.

This module provides utilities for working with the CV data schema.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

from cv_builder_from_yaml_to_pdf.models import CV


def get_cv_schema() -> Dict[str, Any]:
    """Get the JSON schema for the CV model.
    
    Returns:
        Dict containing the JSON schema for the CV model
    """
    schema = CV.model_json_schema()
    return schema


def save_schema_to_file(output_path: str) -> str:
    """Save the CV schema to a JSON file.
    
    Args:
        output_path: Path where the schema will be saved
        
    Returns:
        The absolute path to the saved schema file
    """
    schema = get_cv_schema()
    
    # Ensure the output directory exists
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the schema to the file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=2)
    
    return str(output_file.absolute())


def generate_schema_markdown() -> str:
    """Generate a markdown description of the CV schema.
    
    Returns:
        Markdown string describing the CV schema
    """
    schema = get_cv_schema()
    
    # Start with a header
    markdown = "# CV Schema Documentation\n\n"
    markdown += "This document describes the schema for the CV data used by CV Builder.\n\n"
    
    # Add the main CV schema
    markdown += "## CV Schema\n\n"
    
    if 'properties' in schema:
        for prop_name, prop_data in schema['properties'].items():
            required = prop_name in schema.get('required', [])
            markdown += f"### {prop_name}" + (" (required)" if required else "") + "\n\n"
            
            # Add description if available
            if 'description' in prop_data:
                markdown += f"{prop_data['description']}\n\n"
            
            # Add type information
            if 'type' in prop_data:
                markdown += f"**Type**: `{prop_data['type']}`\n\n"
            elif '$ref' in prop_data:
                ref_name = prop_data['$ref'].split('/')[-1]
                markdown += f"**Type**: `{ref_name}`\n\n"
            elif 'items' in prop_data and prop_data.get('type') == 'array':
                if '$ref' in prop_data['items']:
                    item_type = prop_data['items']['$ref'].split('/')[-1]
                    markdown += f"**Type**: Array of `{item_type}`\n\n"
                else:
                    markdown += f"**Type**: Array\n\n"
    
    # Add documentation for nested models
    markdown += "\n## Model Definitions\n\n"
    
    for definition_name, definition_data in schema.get('$defs', {}).items():
        markdown += f"### {definition_name}\n\n"
        
        # Add description if available
        if 'description' in definition_data:
            markdown += f"{definition_data['description']}\n\n"
        
        # List properties
        if 'properties' in definition_data:
            markdown += "| Property | Type | Required | Description |\n"
            markdown += "|----------|------|----------|-------------|\n"
            
            for prop_name, prop_data in definition_data['properties'].items():
                # Determine type
                if 'type' in prop_data:
                    prop_type = prop_data['type']
                elif '$ref' in prop_data:
                    prop_type = prop_data['$ref'].split('/')[-1]
                elif 'items' in prop_data and prop_data.get('type') == 'array':
                    if '$ref' in prop_data['items']:
                        item_type = prop_data['items']['$ref'].split('/')[-1]
                        prop_type = f"Array of {item_type}"
                    else:
                        prop_type = "Array"
                else:
                    prop_type = "Any"
                
                # Check if required
                required = prop_name in definition_data.get('required', [])
                
                # Get description
                description = prop_data.get('description', '')
                
                markdown += f"| {prop_name} | {prop_type} | {'Yes' if required else 'No'} | {description} |\n"
            
            markdown += "\n"
    
    return markdown

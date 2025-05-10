#!/usr/bin/env python
"""
Sample script demonstrating how to use the CV Builder's Pydantic models programmatically.

This script shows how to:
1. Parse a YAML file into Pydantic models
2. Create and validate a CV model from scratch
3. Export a CV model to YAML
4. Handle validation errors

Run this script to see how the Pydantic models work.
"""

import sys
import yaml
from pathlib import Path
from pydantic import ValidationError

from cv_builder_from_yaml_to_pdf.models import CV, PersonalInfo, Education, Experience
from cv_builder_from_yaml_to_pdf.yaml_parser import parse_yaml_file, validate_cv_data


def load_cv_from_yaml(file_path):
    """Load a CV from a YAML file and validate it with Pydantic."""
    print(f"Loading CV from {file_path}...")
    
    try:
        # Parse the YAML file
        yaml_data = parse_yaml_file(file_path)
        
        # Validate with Pydantic model
        cv = CV.model_validate(yaml_data)
        print("✓ CV data successfully loaded and validated!")
        print(f"Name: {cv.personal_info.name}")
        print(f"Email: {cv.personal_info.email}")
        print(f"Number of education entries: {len(cv.education)}")
        print(f"Number of experience entries: {len(cv.experience)}")
        
        return cv
    
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return None
    
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML format - {e}")
        return None
    
    except ValidationError as e:
        print(f"Error: Validation failed - {e}")
        return None


def create_cv_programmatically():
    """Create a CV from scratch using Pydantic models."""
    print("\nCreating a CV programmatically...")
    
    try:
        # Create personal info
        personal_info = PersonalInfo(
            name="John Developer",
            email="john@example.com",
            phone="+1 (555) 123-4567",
            summary="Software developer with experience in Python and web development"
        )
        
        # Create education entries
        education = [
            Education(
                institution="Code University",
                degree="Bachelor of Science in Computer Science",
                start_date="2015-09",
                end_date="2019-06"
            )
        ]
        
        # Create experience entries
        experience = [
            Experience(
                company="Tech Company",
                title="Software Engineer",
                start_date="2019-08",
                end_date="Present",
                description="Working on web applications",
                achievements=["Developed feature X", "Improved performance by 30%"]
            )
        ]
        
        # Create the full CV
        cv = CV(
            personal_info=personal_info,
            education=education,
            experience=experience
        )
        
        print("✓ CV successfully created and validated!")
        
        # Export to YAML
        cv_dict = cv.model_dump()
        yaml_str = yaml.dump(cv_dict, sort_keys=False, indent=2)
        print("\nGenerated YAML:")
        print("-" * 40)
        print(yaml_str)
        print("-" * 40)
        
        return cv
    
    except ValidationError as e:
        print(f"Error creating CV: {e}")
        return None


def demo_validation_error():
    """Demonstrate validation error handling."""
    print("\nDemonstrating validation error handling...")
    
    try:
        # Missing required fields
        cv = CV(
            personal_info=PersonalInfo(name="Missing Email"),  # Email is required
            education=[],  # Empty but valid
            experience=[]  # Empty but valid
        )
        print("This should not print as validation should fail")
    
    except ValidationError as e:
        print("✓ Validation error correctly caught:")
        print(f"  - {e.errors()[0]['loc'][1]}: {e.errors()[0]['msg']}")


if __name__ == "__main__":
    # Use example_cv.yaml by default, or accept a file path argument
    file_path = "example_cv.yaml"
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    
    # Full path to the example CV
    base_dir = Path(__file__).parent
    example_path = base_dir / file_path
    
    # Demonstrate loading from YAML
    cv = load_cv_from_yaml(example_path)
    
    # Demonstrate creating programmatically
    create_cv_programmatically()
    
    # Demonstrate validation error
    demo_validation_error()

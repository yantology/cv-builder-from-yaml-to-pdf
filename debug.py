"""Simple script to test the CV builder."""

import sys
import yaml
from pathlib import Path


def main():
    """Run a simple test of the CV builder."""
    if len(sys.argv) < 2:
        print("Usage: python debug.py <yaml_file>")
        sys.exit(1)
    
    yaml_file_path = sys.argv[1]
    yaml_path = Path(yaml_file_path)
    
    if not yaml_path.exists():
        print(f"YAML file not found: {yaml_file_path}")
        sys.exit(1)
    
    try:
        with open(yaml_path, 'r', encoding='utf-8') as yaml_file:
            data = yaml.safe_load(yaml_file)
        
        # Debug: Print the contents of the YAML file
        print("YAML data loaded:")
        print(f"Keys in data: {list(data.keys())}")
        
        # Check if required sections are present
        required_sections = ['personal_info', 'education', 'experience']
        for section in required_sections:
            print(f"Checking section: {section}")
            if section not in data:
                print(f"  - Missing section: {section}")
            else:
                print(f"  - Found section: {section}")
        
        # Check personal_info
        personal_info = data.get('personal_info', {})
        print(f"Personal info: {personal_info}")
        
        required_personal_fields = ['name', 'email']
        for field in required_personal_fields:
            print(f"Checking personal info field: {field}")
            if field not in personal_info:
                print(f"  - Missing field: {field}")
            else:
                print(f"  - Found field: {field}")
        
        print("\nSkills section:")
        skills = data.get('skills', [])
        print(f"Skills type: {type(skills)}")
        print(f"Skills: {skills}")
        
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

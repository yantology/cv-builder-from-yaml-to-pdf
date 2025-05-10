# Working with Pydantic Models in CV Builder

This document provides a guide to working with the Pydantic models in the CV Builder tool.

## Introduction

The CV Builder tool uses [Pydantic](https://docs.pydantic.dev/) for data validation and parsing. Pydantic provides:

- Data validation
- Settings management
- Parsing and serialization
- Error handling with clear error messages

## Basic Usage

### Validating a YAML File

The simplest way to validate a YAML file is using the CLI:

```bash
cv-builder validate my-cv.yaml
```

### Programmatic Usage

You can also use the Pydantic models programmatically in your own code:

```python
from cv_builder_from_yaml_to_pdf.models import CV
from cv_builder_from_yaml_to_pdf.yaml_parser import parse_yaml_file

# Parse the YAML file
yaml_data = parse_yaml_file("my-cv.yaml")

# Validate with Pydantic model
try:
    cv = CV.model_validate(yaml_data)
    print(f"CV for {cv.personal_info.name} is valid!")
    
    # Access data through the model
    print(f"Email: {cv.personal_info.email}")
    print(f"Education entries: {len(cv.education)}")
    
except ValidationError as e:
    print(f"Validation error: {e}")
```

## Model Structure

The CV model is hierarchical:

- `CV` - Main model containing all sections
  - `personal_info` - Personal information (name, email, etc.)
  - `education` - List of education entries
  - `experience` - List of experience entries
  - Optional sections: skills, projects, certifications, etc.

## Creating CV Data Programmatically

You can create CV data programmatically:

```python
from cv_builder_from_yaml_to_pdf.models import CV, PersonalInfo, Education, Experience

# Create a CV from scratch
cv = CV(
    personal_info=PersonalInfo(
        name="John Developer",
        email="john@example.com",
        phone="+1-555-123-4567",
        summary="Software developer with experience in Python"
    ),
    education=[
        Education(
            institution="Tech University",
            degree="BS in Computer Science",
            start_date="2015-09",
            end_date="2019-05"
        )
    ],
    experience=[
        Experience(
            company="Tech Corp",
            title="Software Engineer",
            start_date="2019-06",
            end_date="Present",
            description="Working on web applications",
            achievements=["Developed feature X", "Improved performance by 30%"]
        )
    ]
)

# Export to dictionary
cv_dict = cv.model_dump()

# Export to YAML
import yaml
yaml_str = yaml.dump(cv_dict)
```

## Error Handling

Pydantic provides detailed error messages:

```python
try:
    # Missing required field 'email'
    cv = CV(
        personal_info=PersonalInfo(name="John"),  # Missing email
        education=[],
        experience=[]
    )
except ValidationError as e:
    for error in e.errors():
        print(f"Field: {'.'.join(map(str, error['loc']))}")
        print(f"Error: {error['msg']}")
        print(f"Type: {error['type']}")
```

## Advanced Validation

You can extend the models with custom validators:

```python
from pydantic import BaseModel, validator

class CustomCV(CV):
    @validator('experience')
    def validate_experience_dates(cls, v):
        # Custom validation logic
        for exp in v:
            if exp.end_date == "Present" and exp.start_date > "2022":
                raise ValueError("Present job cannot start in the future")
        return v
```

## Reference

For the full schema, generate the schema documentation:

```bash
cv-builder schema --markdown cv-schema.md
```

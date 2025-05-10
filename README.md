# CV Builder: YAML to PDF

A tool to generate beautiful PDF CVs from YAML files.

## Features

- Define your CV in a simple YAML format
- Robust data validation with Pydantic
- Generate professional PDFs with different style options
- Support for multiple page sizes (A4, Letter)
- Preview generated PDFs
- Command-line interface for easy integration into workflows

## Installation

Make sure you have Python 3.11 or higher installed.

```bash
# Install using pip (from PyPI)
pip install cv-builder-from-yaml-to-pdf

# Or install directly from the repository
git clone https://github.com/yourusername/cv-builder-from-yaml-to-pdf.git
cd cv-builder-from-yaml-to-pdf
poetry install
```

## Usage

### Create a new CV YAML template

```bash
# Create a new CV YAML template
cv-builder init my-cv.yaml

# Create a specific type of CV (academic, minimal, or default)
cv-builder init my-cv.yaml --template academic
```

### Edit the YAML file

Open the generated YAML file and update it with your information. The file contains sections for:

- Personal Information
- Education
- Work Experience
- Skills
- Projects

### Generate a PDF from the YAML file

```bash
# Generate a PDF from the YAML file
cv-builder generate my-cv.yaml

# Optionally specify an output file
cv-builder generate my-cv.yaml --output my-cv.pdf

# Choose a different style
cv-builder generate my-cv.yaml --style modern

# Generate a PDF and open it immediately
cv-builder generate my-cv.yaml --preview

# Preview an existing PDF file
cv-builder preview my-cv.pdf
```

### Validate your YAML file

```bash
# Validate a YAML file against the CV schema
cv-builder validate my-cv.yaml
```

### Generate Schema Documentation

```bash
# Generate JSON schema file
cv-builder schema --output cv-schema.json

# Generate Markdown documentation
cv-builder schema --markdown cv-schema.md

# Generate both formats
cv-builder schema --output cv-schema.json --markdown cv-schema.md
```

## CV Schema and Validation

This tool uses Pydantic for data validation, ensuring that your CV data follows the correct structure. The CV schema includes:

- **Personal Information**: name, email, phone, location, website, etc.
- **Education**: institution, degree, dates, location, details
- **Experience**: company, title, dates, description, achievements
- **Skills**: categorized lists of skills
- **Projects**: name, description, technologies used
- **And more**: certifications, languages, references, publications

### Schema Enforcement

The schema enforces:
- Required fields (e.g., name, email in personal info)
- Data types (e.g., dates as strings, achievements as lists)
- Structural validation (e.g., personal_info, education, and experience sections are required)

Use the `cv-builder validate` command to check your YAML file against this schema.

#### Available Styles

The CV Builder supports multiple styles for your PDF CV:

- `classic` (default): Traditional CV style with serif fonts
- `modern`: Contemporary design with blue accents and sans-serif fonts
- `minimal`: Clean, minimalist design with subtle formatting

#### Page Sizes

The CV Builder supports the following page sizes:

- `A4` (default): 210 × 297 mm
- `letter`: 8.5 × 11 inches (215.9 × 279.4 mm)

## YAML Format

The YAML file should contain the following sections:

- `personal_info`: Contains basic information like name, email, etc.
- `education`: A list of educational qualifications
- `experience`: A list of work experiences
- `skills`: A list of skills, optionally categorized
- `projects`: A list of projects (optional)

Additional sections for academic CVs:
- `publications`: A list of academic publications
- `teaching`: Teaching experience
- `grants_and_awards`: Grants and awards received

See the generated template for a complete example.

## Available Templates

The CV Builder provides multiple templates for different types of CVs:

- `default`: Standard professional CV for software engineers and other tech roles
- `academic`: Academic CV with focus on publications, teaching experience, and research
- `minimal`: Simplified CV format with essential sections only

## Development

This project uses Poetry for dependency management. To set up a development environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/cv-builder-from-yaml-to-pdf.git
cd cv-builder-from-yaml-to-pdf

# Install dependencies
poetry install

# Run the application
poetry run cv-builder --help
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Using Pydantic Models Programmatically

If you want to use the Pydantic models in your own scripts, you can do so as follows:

```python
from cv_builder_from_yaml_to_pdf.models import CV, PersonalInfo, Education
from cv_builder_from_yaml_to_pdf.yaml_parser import validate_cv_data

# Create a CV from scratch
personal_info = PersonalInfo(
    name="John Doe",
    email="john@example.com",
    phone="+1-555-123-4567"
)

education = [
    Education(
        institution="University",
        degree="Bachelor of Science",
        start_date="2015",
        end_date="2019"
    )
]

# Create the full CV (minimal example)
cv = CV(
    personal_info=personal_info,
    education=education,
    experience=[]  # Empty but required
)

# Validate a CV from a dictionary
data = {
    "personal_info": {
        "name": "Jane Smith",
        "email": "jane@example.com"
    },
    "education": [
        {
            "institution": "College",
            "degree": "Associate's Degree",
            "start_date": "2010"
        }
    ],
    "experience": [
        {
            "company": "Company XYZ",
            "title": "Developer",
            "start_date": "2020"
        }
    ]
}

result = validate_cv_data(data)
if result is True:
    print("CV is valid!")
else:
    print("Validation errors:", result)
```
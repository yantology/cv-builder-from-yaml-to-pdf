"""CV Builder: Convert YAML files to beautiful PDF CVs."""

from cv_builder_from_yaml_to_pdf.main import main
from cv_builder_from_yaml_to_pdf.yaml_parser import parse_yaml_file, validate_cv_data
from cv_builder_from_yaml_to_pdf.pdf_generator import generate_cv_pdf
from cv_builder_from_yaml_to_pdf.templates import create_sample_cv_yaml, create_yaml_from_template

__version__ = "0.1.0"
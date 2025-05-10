"""Tests for CV Builder.

This module contains tests for the CV Builder functionality.
"""

import os
import tempfile
from pathlib import Path

import pytest
import yaml

from cv_builder_from_yaml_to_pdf.yaml_parser import parse_yaml_file, validate_cv_data
from cv_builder_from_yaml_to_pdf.pdf_generator import generate_cv_pdf
from cv_builder_from_yaml_to_pdf.templates import create_sample_cv_yaml


def test_parse_yaml_file():
    """Test parsing a YAML file."""
    # Create a temporary YAML file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.yaml') as temp_file:
        temp_file.write('''
            personal_info:
              name: Test User
              email: test@example.com
            education:
              - institution: Test University
                degree: Test Degree
            experience:
              - company: Test Company
                title: Test Title
        ''')
        temp_path = temp_file.name
    
    try:
        # Parse the YAML file
        data = parse_yaml_file(temp_path)
        
        # Check the parsed data
        assert data['personal_info']['name'] == 'Test User'
        assert data['personal_info']['email'] == 'test@example.com'
        assert data['education'][0]['institution'] == 'Test University'
        assert data['experience'][0]['company'] == 'Test Company'
    finally:
        # Clean up the temporary file
        os.unlink(temp_path)


def test_validate_cv_data():
    """Test validating CV data."""
    # Valid data
    valid_data = {
        'personal_info': {
            'name': 'Test User',
            'email': 'test@example.com'
        },
        'education': [
            {
                'institution': 'Test University',
                'degree': 'Test Degree'
            }
        ],
        'experience': [
            {
                'company': 'Test Company',
                'title': 'Test Title'
            }
        ]
    }
    
    assert validate_cv_data(valid_data) is True
    
    # Invalid data: missing personal_info
    invalid_data1 = {
        'education': [],
        'experience': []
    }
    
    assert validate_cv_data(invalid_data1) is False
    
    # Invalid data: missing name in personal_info
    invalid_data2 = {
        'personal_info': {
            'email': 'test@example.com'
        },
        'education': [],
        'experience': []
    }
    
    assert validate_cv_data(invalid_data2) is False


def test_create_sample_cv_yaml():
    """Test creating a sample CV YAML file."""
    # Create a temporary output path
    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, 'sample_cv.yaml')
        
        # Create the sample YAML file
        created_path = create_sample_cv_yaml(output_path)
        
        # Check that the file was created
        assert os.path.exists(created_path)
        
        # Parse the created file to ensure it's valid YAML
        with open(created_path, 'r') as yaml_file:
            data = yaml.safe_load(yaml_file)
        
        # Check some content
        assert 'personal_info' in data
        assert 'education' in data
        assert 'experience' in data


def test_generate_cv_pdf():
    """Test generating a PDF from CV data."""
    # Create a temporary output path
    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, 'test_cv.pdf')
        
        # Create some test CV data
        cv_data = {
            'personal_info': {
                'name': 'Test User',
                'email': 'test@example.com'
            },
            'education': [
                {
                    'institution': 'Test University',
                    'degree': 'Test Degree',
                    'start_date': '2015',
                    'end_date': '2019'
                }
            ],
            'experience': [
                {
                    'company': 'Test Company',
                    'title': 'Test Title',
                    'start_date': '2019',
                    'end_date': 'Present',
                    'description': 'Test description'
                }
            ]
        }
        
        # Generate the PDF
        pdf_path = generate_cv_pdf(cv_data, output_path)
        
        # Check that the PDF was created
        assert os.path.exists(pdf_path)
        
        # Check that it's a PDF file (begins with %PDF)
        with open(pdf_path, 'rb') as pdf_file:
            header = pdf_file.read(4)
            assert header == b'%PDF'

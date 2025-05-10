# Test cases for Pydantic model validation

import unittest
from pathlib import Path

import yaml
from pydantic import ValidationError

from cv_builder_from_yaml_to_pdf.yaml_parser import parse_yaml_file, validate_cv_data, validate_cv_string, validate_cv_dict
from cv_builder_from_yaml_to_pdf.models import CV, PersonalInfo, Education, Experience, Skill


class TestPydanticModels(unittest.TestCase):
    """Test cases for CV Pydantic models."""
    
    def test_valid_cv_from_file(self):
        """Test that a valid CV from a file validates correctly."""
        # Get the path to the example CV
        example_path = Path(__file__).parent.parent / "example_cv.yaml"
        
        # Parse and validate
        data = parse_yaml_file(str(example_path))
        result = validate_cv_data(data)
        
        self.assertTrue(result, "Valid CV should validate correctly")
        
        # Test model instantiation
        cv = CV.model_validate(data)
        self.assertEqual(cv.personal_info.name, "Jane Doe")
        self.assertEqual(len(cv.education), 2)
        self.assertEqual(len(cv.experience), 2)
    
    def test_valid_cv_from_string(self):
        """Test that a valid CV from a YAML string validates correctly."""
        yaml_string = """
        personal_info:
          name: John Doe
          email: john@example.com
        education:
          - institution: University
            degree: Degree
            start_date: "2020"
        experience:
          - company: Company
            title: Title
            start_date: "2021"
        """
        
        result = validate_cv_string(yaml_string)
        self.assertTrue(result, "Valid CV string should validate correctly")
    
    def test_valid_cv_from_dict(self):
        """Test that a valid CV from a dictionary validates correctly."""
        cv_dict = {
            "personal_info": {
                "name": "John Doe",
                "email": "john@example.com"
            },
            "education": [
                {
                    "institution": "University",
                    "degree": "Degree",
                    "start_date": "2020"
                }
            ],
            "experience": [
                {
                    "company": "Company",
                    "title": "Title",
                    "start_date": "2021"
                }
            ]
        }
        
        result = validate_cv_dict(cv_dict)
        self.assertTrue(result, "Valid CV dict should validate correctly")
    
    def test_invalid_cv_missing_required(self):
        """Test that a CV missing required fields fails validation."""
        # Missing email in personal_info
        cv_dict = {
            "personal_info": {
                "name": "John Doe"
                # Missing email field
            },
            "education": [
                {
                    "institution": "University",
                    "degree": "Degree",
                    "start_date": "2020"
                }
            ],
            "experience": [
                {
                    "company": "Company",
                    "title": "Title",
                    "start_date": "2021"
                }
            ]
        }
        
        result = validate_cv_dict(cv_dict)
        self.assertIsInstance(result, list, "Invalid CV should return list of errors")
        self.assertTrue(any("email" in error for error in result), 
                       "Error should mention missing email field")
    
    def test_invalid_cv_wrong_type(self):
        """Test that a CV with wrong field types fails validation."""
        # start_date should be a string, not a number
        cv_dict = {
            "personal_info": {
                "name": "John Doe",
                "email": "john@example.com"
            },
            "education": [
                {
                    "institution": "University",
                    "degree": "Degree",
                    "start_date": 2020  # Should be a string
                }
            ],
            "experience": [
                {
                    "company": "Company",
                    "title": "Title",
                    "start_date": "2021"
                }
            ]
        }
        
        result = validate_cv_dict(cv_dict)
        self.assertIsInstance(result, list, "Invalid CV should return list of errors")
    
    def test_model_direct_instantiation(self):
        """Test direct instantiation of CV model and submodels."""
        # Create personal info
        personal_info = PersonalInfo(
            name="John Developer",
            email="john@example.com",
            phone="+1 (555) 123-4567"
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
        
        # Create skills
        skills = [
            Skill(
                category="Programming",
                name="Python, JavaScript"
            )
        ]
        
        # Create the full CV
        cv = CV(
            personal_info=personal_info,
            education=education,
            experience=experience,
            skills=skills
        )
        
        # Test model properties
        self.assertEqual(cv.personal_info.name, "John Developer")
        self.assertEqual(cv.education[0].institution, "Code University")
        self.assertEqual(cv.experience[0].company, "Tech Company")
        self.assertEqual(cv.skills[0].category, "Programming")
        
        # Test model serialization
        cv_dict = cv.model_dump()
        self.assertIn("personal_info", cv_dict)
        self.assertIn("education", cv_dict)
        self.assertIn("experience", cv_dict)
        self.assertIn("skills", cv_dict)


if __name__ == "__main__":
    unittest.main()

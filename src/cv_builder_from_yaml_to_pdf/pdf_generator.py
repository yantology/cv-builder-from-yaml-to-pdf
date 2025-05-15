"""PDF Generator for CV Builder.

This module handles the generation of PDF files from CV data.
"""

import os
from pathlib import Path
from typing import List

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem

from cv_builder_from_yaml_to_pdf.models import CV, PersonalInfo, Education, CompanyExperience, Role, Project, Skill # Updated import
from cv_builder_from_yaml_to_pdf.styles import get_style


class CVPDFGenerator:
    """Class to generate a PDF CV from structured data."""
    
    def __init__(self, output_path: str, data: CV, style: str = "classic", page_size: str = "A4"):
        """Initialize the PDF generator.
        
        Args:
            output_path: Path where the PDF will be saved
            data: CV model containing the CV data
            style: Style name for the CV (e.g., 'classic', 'modern', 'minimal')
            page_size: Size of the page ('A4' or 'letter')
        """
        self.output_path = Path(output_path)
        self.data = data
        
        # Set page size
        if page_size.lower() == "a4":
            self.page_size = A4
        elif page_size.lower() == "letter":
            self.page_size = letter
        else:
            # Default to A4
            self.page_size = A4
        
        # Apply style
        try:
            cv_style = get_style(style)
            self.styles = cv_style.get_styles()
        except ValueError:
            # Fall back to classic style
            cv_style = get_style("classic")
            self.styles = cv_style.get_styles()
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_path.parent, exist_ok=True)
        
        # Initialize document
        self.doc = SimpleDocTemplate(
            str(self.output_path),
            pagesize=self.page_size,
            rightMargin=1*cm, # Reduced right margin
            leftMargin=2*cm,
            topMargin=1*cm, # Reduced top margin
            bottomMargin=2*cm
        )
        
        # Elements to be added to the PDF
        self.elements = []
    
    def generate(self):
        """Generate the PDF document."""
        # Add all sections
        self._add_content()
        
        # Build the document
        self.doc.build(self.elements)
        
        return self.output_path
    
    def _add_content(self):
        """Add all CV content to the PDF."""
        # Add personal info
        personal_info = self.data.personal_info
        if personal_info:
            self._add_personal_info(personal_info)
        
        # Add experience
        experience = self.data.experience
        if experience:
            self._add_section('Work Experience', experience, self._format_company_experience) # Renamed formatter
        
        # Add education
        education = self.data.education
        if education:
            self._add_section('Education', education, self._format_education)
        
        # Add skills
        skills = self.data.skills
        if skills:
            self._add_skills(skills)
        
        # Add projects
        projects = self.data.projects
        if projects:
            self._add_section('Projects', projects, self._format_project)
    
    def _add_personal_info(self, personal_info: PersonalInfo):
        """Add personal information to the PDF."""
        # Add name
        if personal_info.name:
            self.elements.append(Paragraph(personal_info.name, self.styles['Name']))
        
        # Add title if present
        if personal_info.title:
            self.elements.append(Paragraph(personal_info.title, self.styles['ContactInfo']))
        
        # Combine contact information
        contact_parts = []
        if personal_info.email:
            contact_parts.append(f"Email: {personal_info.email}")
        if personal_info.phone:
            contact_parts.append(f"Phone: {personal_info.phone}")
        if personal_info.location:
            contact_parts.append(f"Location: {personal_info.location}")
        if personal_info.website:
            contact_parts.append(f"Website: {personal_info.website}")
        if personal_info.linkedin:
            contact_parts.append(f"LinkedIn: {personal_info.linkedin}")
        
        contact_info = " | ".join(contact_parts)
        self.elements.append(Paragraph(contact_info, self.styles['ContactInfo']))
        
        # Add summary if present
        if personal_info.summary:
            self.elements.append(Paragraph('Summary', self.styles['SectionHeading']))
            # Split summary into paragraphs if it contains newlines
            summary_lines = personal_info.summary.split('\n')
            for line in summary_lines:
                if line.strip(): # Add non-empty lines as paragraphs
                    indented_line = f"{line.lstrip()}" # Add 4 dashes to the start of the line
                    self.elements.append(Paragraph(indented_line, self.styles['Paragraph']))
            self.elements.append(Spacer(1, 12))
    
    def _add_section(self, title, items, formatter):
        """Add a section to the PDF with formatted items."""
        self.elements.append(Paragraph(title, self.styles['SectionHeading']))
        
        for item in items:
            formatter(item)
            self.elements.append(Spacer(1, 6)) # Add a bit more space after a full company entry
    
    def _format_company_experience(self, company_exp: CompanyExperience):
        """Format a company experience entry, including all its roles."""
        # Company name and optional location
        company_text = company_exp.company
        if company_exp.location:
            company_text += f" ({company_exp.location})"
        self.elements.append(Paragraph(company_text, self.styles['ExperienceTitle'])) # Style for company name
        
        for role in company_exp.roles:
            # Role title
            self.elements.append(Paragraph(role.title, self.styles['RoleTitle'])) # Potentially a new style or reuse ExperienceDetails/Normal
            
            # Dates for the role
            dates = f"{role.start_date} - {role.end_date or 'Present'}"
            if role.location: # Role-specific location
                dates += f" | {role.location}"
            self.elements.append(Paragraph(dates, self.styles['ExperienceDetails']))
            
            # Description for the role
            if role.description:
                self.elements.append(Paragraph(role.description, self.styles['Normal']))
            
            # Achievements for the role
            if role.achievements:
                items = []
                for achievement in role.achievements:
                    items.append(ListItem(Paragraph(achievement, self.styles['Normal'])))
                self.elements.append(ListFlowable(items, bulletType='bullet', leftIndent=0.5*cm, bulletFontName='Helvetica-Bold', bulletFontSize=10))
            self.elements.append(Spacer(1, 4)) # Spacer between roles within the same company

    def _format_education(self, edu: Education):
        """Format an education entry."""
        # Degree and institution
        degree_text = f"{edu.degree} - {edu.institution}"
        self.elements.append(Paragraph(degree_text, self.styles['ExperienceTitle']))
        
        # Dates and location
        dates = f"{edu.start_date} - {edu.end_date or 'Present'}"
        if edu.location:
            dates += f" | {edu.location}"
        self.elements.append(Paragraph(dates, self.styles['ExperienceDetails']))
        
        # Additional details
        if edu.details:
            self.elements.append(Paragraph(edu.details, self.styles['Normal']))
    
    def _add_skills(self, skills: List[Skill]):
        """Add skills to the PDF."""
        self.elements.append(Paragraph('Skills', self.styles['SectionHeading']))
        
        # Group skills by category if they have categories
        categorized_skills = {}
        uncategorized_skills = []
        
        for skill in skills:
            category = skill.category
            skill_name = skill.name
            if category not in categorized_skills:
                categorized_skills[category] = []
            categorized_skills[category].append(skill_name)
        
        # Add categorized skills
        for category, skill_list in categorized_skills.items():
            self.elements.append(Paragraph(category, self.styles['ExperienceTitle']))
            # Make sure we have a list of strings before joining
            skill_text = ", ".join([s for s in skill_list if s])
            self.elements.append(Paragraph(skill_text, self.styles['Normal']))
            self.elements.append(Spacer(1, 4))
    
    def _format_project(self, project: Project):
        """Format a project entry."""
        # Project name
        project_text = project.name
        if project.link:
            project_text += f" ({project.link})"
        self.elements.append(Paragraph(project_text, self.styles['ExperienceTitle']))
        
        # Dates
        if project.start_date:
            date_text = project.start_date
            if project.end_date:
                date_text += f" - {project.end_date}"
            self.elements.append(Paragraph(date_text, self.styles['ExperienceDetails']))
        
        # Description
        if project.description:
            self.elements.append(Paragraph(project.description, self.styles['Normal']))
        
        # Technologies used
        if project.technologies:
            tech_text = f"Technologies: {', '.join(project.technologies)}"
            self.elements.append(Paragraph(tech_text, self.styles['Normal']))


def generate_cv_pdf(cv_data: CV, output_path: str, style: str = "classic", page_size: str = "A4") -> str:
    """Generate a PDF CV from the provided data.
    
    Args:
        cv_data: CV model containing the CV data
        output_path: Path where the PDF will be saved
        style: Style name for the CV (e.g., 'classic', 'modern', 'minimal')
        page_size: Size of the page ('A4' or 'letter')
        
    Returns:
        Path to the generated PDF file
    """
    generator = CVPDFGenerator(output_path, cv_data, style, page_size)
    return str(generator.generate())

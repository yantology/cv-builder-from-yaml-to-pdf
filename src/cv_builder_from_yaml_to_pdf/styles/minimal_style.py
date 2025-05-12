\
# filepath: c:\\Users\\LENOVO\\Documents\\python\\yaml-to-pdf\\cv-builder-from-yaml-to-pdf-2\\src\\cv_builder_from_yaml_to_pdf\\styles\\minimal_style.py
"""Minimal style for CVs."""

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from .base_style import CVStyle

class MinimalStyle(CVStyle):
    """Minimal style for CVs."""
    
    def _setup_styles(self):
        """Setup minimal style."""
        # Name style
        self.styles.add(ParagraphStyle(
            name='Name',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))
        
        # Section headings
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=11,
            spaceAfter=6,
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderPadding=0,
            borderColor=colors.black,
            textTransform='uppercase'
        ))
        
        # Contact info style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=12
        ))
        
        # Experience title style
        self.styles.add(ParagraphStyle(
            name='ExperienceTitle',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            spaceAfter=1
        ))
        
        # Experience details style
        self.styles.add(ParagraphStyle(
            name='ExperienceDetails',
            parent=self.styles['Normal'],
            fontSize=9,
            fontName='Helvetica-Oblique',
            spaceAfter=1
        ))
        
        # Role Title style
        self.styles.add(ParagraphStyle(
            name='RoleTitle',
            parent=self.styles['Normal'],
            fontSize=9, 
            fontName='Helvetica-Bold', 
            spaceBefore=2,
            spaceAfter=1,
            leftIndent=10 # Indent roles
        ))
        
        # Normal text style
        normal_style = self.styles['Normal']
        normal_style.fontSize = 9
        normal_style.spaceAfter = 6

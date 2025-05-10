\
# filepath: c:\\Users\\LENOVO\\Documents\\python\\yaml-to-pdf\\cv-builder-from-yaml-to-pdf-2\\src\\cv_builder_from_yaml_to_pdf\\styles\\classic_style.py
"""Classic style for CVs."""

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from .base_style import CVStyle

class ClassicStyle(CVStyle):
    """Classic style for CVs."""
    
    def _setup_styles(self):
        """Setup classic style."""
        # Name style
        self.styles.add(ParagraphStyle(
            name='Name',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=6
        ))
        
        # Section headings
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=6,
            fontName='Times-Bold'
        ))
        
        # Contact info style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=12
        ))
        
        # Experience title style
        self.styles.add(ParagraphStyle(
            name='ExperienceTitle',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Times-Bold',
            spaceAfter=1
        ))
        
        # Experience details style
        self.styles.add(ParagraphStyle(
            name='ExperienceDetails',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Times-Italic',
            spaceAfter=1
        ))
        
        # Normal text style
        normal_style = self.styles['Normal']
        normal_style.fontSize = 10
        normal_style.spaceAfter = 6
        normal_style.fontName = 'Times-Roman'

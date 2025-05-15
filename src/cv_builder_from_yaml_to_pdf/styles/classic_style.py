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
            fontSize=18,  # Increased font size
            spaceAfter=8, # Adjusted spacing
            leading=22    # Added leading
        ))
        
        # Section headings
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,  # Increased font size
            spaceAfter=8, # Adjusted spacing
            fontName='Times-Bold',
            leading=18    # Added leading
        ))
        
        # Contact info style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=14, # Adjusted spacing
            leading=12     # Added leading
        ))
        
        # Experience title style
        self.styles.add(ParagraphStyle(
            name='ExperienceTitle',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Times-Bold',
            spaceAfter=2,  # Adjusted spacing
            leading=14     # Added leading
        ))
        
        # Role Title style (new)
        self.styles.add(ParagraphStyle(
            name='RoleTitle',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Times-Bold',
            leftIndent=0, # Removed indent
            spaceBefore=3, # Adjusted spacing
            spaceAfter=2,  # Adjusted spacing
            leading=12     # Added leading
        ))

        # Experience details style
        self.styles.add(ParagraphStyle(
            name='ExperienceDetails',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Times-Italic',
            leftIndent=0, # Ensure no indent
            spaceAfter=2,  # Adjusted spacing
            leading=12     # Added leading
        ))
        
        # Normal text style
        normal_style = self.styles['Normal']
        normal_style.fontSize = 10
        normal_style.spaceAfter = 6
        normal_style.fontName = 'Times-Roman'
        normal_style.leading = 12 # Added leading
        
        # Paragraph style (similar to Normal)
        self.styles.add(ParagraphStyle(
            name='Paragraph',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName='Times-Roman',
            leading=12,
            firstLineIndent=15
        ))

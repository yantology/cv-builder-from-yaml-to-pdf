"""Modern style for CVs."""

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from .base_style import CVStyle

class ModernStyle(CVStyle):
    """Modern style for CVs."""
    
    def _setup_styles(self):
        """Setup modern style."""
        # Name style (large, bold)
        self.styles.add(ParagraphStyle(
            name='Name',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=6,
            textColor=colors.darkblue
        ))
        
        # Section headings (with colored background)
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=6,
            textColor=colors.white,
            backColor=colors.darkblue,
            borderWidth=1,
            borderColor=colors.darkblue,
            borderPadding=3,
            leftIndent=0,
            rightIndent=0
        ))
        
        # Contact info style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=12,
            textColor=colors.darkgrey
        ))
        
        # Experience title style
        self.styles.add(ParagraphStyle(
            name='ExperienceTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            fontName='Helvetica-Bold',
            spaceAfter=1,
            textColor=colors.darkblue
        ))
        
        # Experience details style
        self.styles.add(ParagraphStyle(
            name='ExperienceDetails',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Oblique',
            spaceAfter=1,
            textColor=colors.darkgrey
        ))
        
        # Role Title style
        self.styles.add(ParagraphStyle(
            name='RoleTitle',
            parent=self.styles['Normal'],
            fontSize=11, # Slightly smaller than ExperienceTitle
            fontName='Helvetica-Bold', # Consistent with ExperienceTitle font
            textColor=colors.darkblue, # Consistent with ExperienceTitle color
            spaceBefore=2,
            spaceAfter=1,
            leftIndent=10 # Indent roles under company
        ))

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
        
        # Normal text style
        normal_style = self.styles['Normal']
        normal_style.fontSize = 10
        normal_style.spaceAfter = 6

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

"""Styling and templates for CV PDFs.

This module provides different styling options for CV PDFs.
"""

from typing import Dict, Any
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT


class CVStyle:
    """Base class for CV styling."""
    
    def __init__(self):
        """Initialize the style."""
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup the styles. Should be implemented by subclasses."""
        pass
    
    def get_styles(self):
        """Get the styles dictionary."""
        return self.styles


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
        
        # Normal text style
        normal_style = self.styles['Normal']
        normal_style.fontSize = 10
        normal_style.spaceAfter = 6
        # No need to add it again, just modify
        # self.styles.add(ParagraphStyle(
        #     name='Normal',
        #     parent=self.styles['Normal'],
        #     fontSize=10,
        #     spaceAfter=6
        # ))


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
        # No need to add it again, just modify
        # self.styles.add(ParagraphStyle(
        #     name='Normal',
        #     parent=self.styles['Normal'],
        #     fontSize=10,
        #     spaceAfter=6,
        #     fontName='Times-Roman'
        # ))


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
        
        # Normal text style
        normal_style = self.styles['Normal']
        normal_style.fontSize = 9
        normal_style.spaceAfter = 6
        # No need to add it again, just modify
        # self.styles.add(ParagraphStyle(
        #     name='Normal',
        #     parent=self.styles['Normal'],
        #     fontSize=9,
        #     spaceAfter=6
        # ))


def get_style(style_name: str) -> CVStyle:
    """Get a CV style by name.
    
    Args:
        style_name: Name of the style
        
    Returns:
        CVStyle object
        
    Raises:
        ValueError: If the style name is not valid
    """
    styles = {
        'modern': ModernStyle,
        'classic': ClassicStyle,
        'minimal': MinimalStyle
    }
    
    if style_name.lower() not in styles:
        valid_styles = ', '.join(styles.keys())
        raise ValueError(f"Invalid style name: {style_name}. Valid styles are: {valid_styles}")
    
    return styles[style_name.lower()]()

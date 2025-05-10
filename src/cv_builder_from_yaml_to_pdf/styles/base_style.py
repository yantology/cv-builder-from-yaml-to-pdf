"""Base CVStyle class."""

from reportlab.lib.styles import getSampleStyleSheet

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

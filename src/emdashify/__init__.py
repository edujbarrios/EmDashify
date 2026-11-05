"""EmDashify: small, predictable em dash conversion."""
from .core import EM_DASH, check, convert, convert_file
from .word import check_docx, convert_docx

__version__ = "0.3.0"

__all__ = ["EM_DASH", "check", "convert", "convert_file", "check_docx", "convert_docx", "__version__"]

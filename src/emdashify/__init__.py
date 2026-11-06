"""EmDashify: small, predictable em dash conversion."""
from .core import EM_DASH, check, convert, convert_file
from .inplace import convert_in_place
from .word import check_docx, convert_docx

__version__ = "0.4.0"

__all__ = ["EM_DASH", "check", "convert", "convert_file", "convert_in_place", "check_docx", "convert_docx", "__version__"]

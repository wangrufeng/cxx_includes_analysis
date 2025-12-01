"""
C++ 依赖关系分析工具库
"""

__version__ = "2.0.0"
__author__ = "rufeng"

from .config import DEFAULT_INCLUDE_PATHS, INCLUDE_PATTERN
from .analyzer import DependencyAnalyzer
from .dot_visualizer import DotVisualizer
from .html_visualizer import HtmlVisualizer
from .utils import get_file_size, format_size, simplify_path

__all__ = [
    'DEFAULT_INCLUDE_PATHS',
    'INCLUDE_PATTERN',
    'DependencyAnalyzer',
    'DotVisualizer',
    'HtmlVisualizer',
    'get_file_size',
    'format_size',
    'simplify_path',
]


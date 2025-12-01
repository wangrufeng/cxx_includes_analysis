#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script for C++ Dependency Analyzer
"""
from setuptools import setup, find_packages
import os

# Read the long description from README
def read_long_description():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()

# Read version from __init__.py
def read_version():
    with open("analyze_includes_lib/__init__.py", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    return "2.0.0"

setup(
    name="cxx-dependency-analyzer",
    version=read_version(),
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for analyzing and visualizing C++ module dependencies",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cxx_includes_analysis",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # No external dependencies required
    ],
    entry_points={
        "console_scripts": [
            "cxx-analyze=analyze_includes:main",
            "cxx-analyze-i=analyze_i_file:analyze_i_file",
        ],
    },
    include_package_data=True,
    keywords="c++ cpp dependency analysis visualization include headers",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/cxx_includes_analysis/issues",
        "Source": "https://github.com/yourusername/cxx_includes_analysis",
        "Documentation": "https://github.com/yourusername/cxx_includes_analysis/blob/main/docs/",
    },
)


"""
ArXiv Search Package Setup
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="arxiv-search-sdk",
    version="1.0.0",
    author="li-xiu-qi",
    author_email="lixiuqixiaoke@qq.com",
    description="A comprehensive Python SDK for searching and retrieving arXiv papers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/arxiv-search-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": ["pytest", "pytest-asyncio", "black", "flake8", "mypy"],
        "docs": ["sphinx", "sphinx-rtd-theme"],
    },
    entry_points={
        "console_scripts": [
            "arxiv-search=arxiv_search.cli:main",
        ],
    },
)

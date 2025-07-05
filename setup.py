"""
ArXiv Search Package Setup
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


requirements = [
    "aiohttp>=3.8.0",
    "feedparser>=6.0.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "python-dotenv>=1.0.0",
    "loguru>=0.7.0",
    "click>=8.0.0",
    "build>=1.0.0",
    "twine>=4.0.0"
]

setup(
    name="arxiv-search-sdk",
    version="1.0.0",
    author="li-xiu-qi",
    author_email="lixiuqixiaoke@qq.com",
    description="A comprehensive Python SDK for searching and retrieving arXiv papers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/li-xiu-qi/arxiv-search-sdk",
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

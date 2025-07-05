"""
ArXiv Search SDK

一个功能强大的 Python SDK，用于搜索和获取 arXiv 论文。
"""

from .client import ArxivClient
from .models import Paper, SearchQuery, SearchFieldQuery, SearchResult
from .categories import (
    ARXIV_CATEGORIES,
    CATEGORY_GROUPS,
    POPULAR_CS_CATEGORIES,
    validate_category,
    get_category_description,
    search_categories_by_keyword,
    get_categories_by_group
)

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# 导出主要类和函数
__all__ = [
    # 客户端
    "ArxivClient",
    
    # 数据模型
    "Paper",
    "SearchQuery", 
    "SearchFieldQuery",
    "SearchResult",
    
    # 分类相关
    "ARXIV_CATEGORIES",
    "CATEGORY_GROUPS",
    "POPULAR_CS_CATEGORIES",
    "validate_category",
    "get_category_description",
    "search_categories_by_keyword",
    "get_categories_by_group",
    
    # 版本信息
    "__version__",
    "__author__",
    "__email__",
]

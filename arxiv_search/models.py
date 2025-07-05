"""
数据模型定义
"""
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from pydantic import BaseModel, Field, validator

class Paper(BaseModel):
    """
    论文数据模型
    
    这个模型表示从 arXiv 获取到的论文信息
    """
    title: str                              # 论文标题
    authors: List[str]                      # 作者列表，每个元素是一个作者姓名
    abstract: str                           # 论文摘要/简介
    arxiv_id: str                          # arXiv 唯一标识符，如 "2023.12345"
    published: datetime                     # 论文首次提交日期
    updated: Optional[datetime] = None      # 论文最后更新日期（如果有的话）
    categories: List[str] = []             # 学科分类列表，如 ["cs.AI", "cs.LG"]
    pdf_url: str                           # PDF 下载链接
    entry_id: str                          # arXiv 条目完整ID，如 "http://arxiv.org/abs/2023.12345v1"
    summary: Optional[str] = None           # 论文总结（可能由AI生成）
    links: List[Dict[str, str]] = []       # 相关链接列表，包含 href, rel, type 等信息
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()  # 将日期转换为 ISO 格式字符串
        }

class SearchFieldQuery(BaseModel):
    """
    特定字段搜索查询
    
    用于在 arXiv 的特定字段中搜索内容
    """
    # arXiv API 支持的搜索字段：
    # ti  - 标题 (Title)
    # au  - 作者 (Author) 
    # abs - 摘要 (Abstract)
    # co  - 评论 (Comment)
    # jr  - 期刊引用 (Journal Reference)
    # cat - 学科分类 (Subject Category) - 必须使用 arXiv 官方分类代码
    # rn  - 报告号 (Report Number)
    # all - 主要内容字段 (Title + Abstract + Author + Comment，不包括分类等元数据)
    field: Literal["ti", "au", "abs", "co", "jr", "cat", "rn", "all"] = "all"
    terms: List[str]                        # 要搜索的关键词列表
    
    @validator('terms')
    def validate_category_terms(cls, v, values):
        """验证分类字段的搜索词必须是有效的 arXiv 分类代码"""
        field = values.get('field')
        if field == 'cat':
            from .categories import validate_category
            invalid_cats = [term for term in v if not validate_category(term)]
            if invalid_cats:
                raise ValueError(f"Invalid arXiv categories: {invalid_cats}. Must use official category codes like 'cs.AI', 'cs.LG', etc.")
        return v

class SearchQuery(BaseModel):
    """
    搜索查询模型
    
    包含所有搜索相关的参数和配置
    """
    original_query: str                     # 用户原始输入的查询字符串
    english_queries: List[str] = []         # 翻译后的英文查询列表（用于多语言支持）
    search_terms: List[str] = []           # 提取的搜索关键词列表
    
    # 特定字段搜索配置
    field_queries: List[SearchFieldQuery] = []  # 字段特定查询列表
    
    # 日期范围过滤
    submitted_date_start: Optional[str] = None   # 开始日期，格式：YYYYMMDDHHMM（如：202301010000）
    submitted_date_end: Optional[str] = None     # 结束日期，格式：YYYYMMDDHHMM（如：202312312359）
    
    # 搜索控制参数
    max_results: int = 10                   # 最大返回结果数量
    sort_by: str = "relevance"             # 排序方式：relevance(相关性), lastUpdatedDate(最后更新), submittedDate(提交日期)
    sort_order: str = "descending"         # 排序顺序：ascending(升序), descending(降序)
    recommendation_priority: str = "relevance"  # 推荐排序优先级：relevance(相关性优先), time(时间优先)

class SearchResult(BaseModel):
    """
    搜索结果模型
    
    封装完整的搜索结果信息
    """
    query: SearchQuery                     # 执行的搜索查询
    papers: List[Paper]                   # 搜索到的论文列表
    total_found: int                      # 总共找到的论文数量
    search_time: float                    # 搜索耗时（秒）

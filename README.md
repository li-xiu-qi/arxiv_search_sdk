# ArXiv Search SDK

一个功能强大的 Python SDK，用于搜索和获取 arXiv 论文。

## 功能特性

- 🔍 **多字段搜索**: 支持按标题、作者、摘要、分类等字段搜索
- 🎯 **智能查询**: 自动优化搜索查询以提高结果相关性
- 📚 **分类浏览**: 支持按学科分类浏览论文
- 🌐 **异步支持**: 使用 asyncio 提供高性能的异步搜索
- 📊 **数据模型**: 使用 Pydantic 提供类型安全的数据模型


## 安装

```bash
pip install arxiv-search-sdk
```

## 快速开始

### 基本搜索

```python
import asyncio
from arxiv_search import ArxivClient

async def main():
    async with ArxivClient() as client:
        # 搜索机器学习相关论文
        papers = await client.search_ml_papers(max_results=10)
        
        for paper in papers:
            print(f"Title: {paper.title}")
            print(f"Authors: {', '.join(paper.authors)}")
            print(f"Abstract: {paper.abstract[:200]}...")
            print(f"PDF: {paper.pdf_url}")
            print("-" * 50)

# 运行异步函数
asyncio.run(main())
```

### 高级搜索

```python
import asyncio
from arxiv_search import ArxivClient

async def main():
    async with ArxivClient() as client:
        # 组合搜索：标题包含"transformer"，作者包含"attention"
        papers = await client.advanced_search(
            title_terms=["transformer"],
            abstract_terms=["attention"],
            categories=["cs.AI", "cs.LG"],
            max_results=20,
            sort_by="submittedDate"
        )
        
        for paper in papers:
            print(f"Title: {paper.title}")
            print(f"Categories: {', '.join(paper.categories)}")
            print(f"Published: {paper.published}")
            print()

asyncio.run(main())
```

### 分类搜索

```python
import asyncio
from arxiv_search import ArxivClient

async def main():
    async with ArxivClient() as client:
        # 搜索人工智能论文
        ai_papers = await client.search_ai_papers(max_results=10)
        
        # 搜索计算机视觉论文
        cv_papers = await client.search_cv_papers(max_results=10)
        
        # 搜索自然语言处理论文
        nlp_papers = await client.search_nlp_papers(max_results=10)
        
        print(f"Found {len(ai_papers)} AI papers")
        print(f"Found {len(cv_papers)} CV papers")
        print(f"Found {len(nlp_papers)} NLP papers")

asyncio.run(main())
```

### 使用查询对象

```python
import asyncio
from arxiv_search import ArxivClient, SearchQuery, SearchFieldQuery

async def main():
    async with ArxivClient() as client:
        # 创建复杂查询
        query = SearchQuery(
            original_query="deep learning transformers",
            field_queries=[
                SearchFieldQuery(field="ti", terms=["deep learning"]),
                SearchFieldQuery(field="abs", terms=["transformer", "attention"]),
                SearchFieldQuery(field="cat", terms=["cs.AI", "cs.LG"])
            ],
            max_results=15,
            sort_by="relevance"
        )
        
        papers = await client.search_papers(query)
        
        for paper in papers:
            print(f"Title: {paper.title}")
            print(f"ArXiv ID: {paper.arxiv_id}")
            print()

asyncio.run(main())
```

## API 文档

### ArxivClient 类

主要的客户端类，提供所有搜索功能。

#### 方法

- `search_papers(query: SearchQuery) -> List[Paper]`: 执行搜索查询
- `search_by_title(title_terms: List[str]) -> List[Paper]`: 按标题搜索
- `search_by_author(author_names: List[str]) -> List[Paper]`: 按作者搜索
- `search_by_abstract(abstract_terms: List[str]) -> List[Paper]`: 按摘要搜索
- `search_by_category(categories: List[str]) -> List[Paper]`: 按分类搜索
- `advanced_search(...)`: 高级组合搜索
- `search_ai_papers()`: 搜索人工智能论文
- `search_ml_papers()`: 搜索机器学习论文
- `search_cv_papers()`: 搜索计算机视觉论文
- `search_nlp_papers()`: 搜索自然语言处理论文

### 数据模型

#### Paper 类

表示 arXiv 论文的数据模型。

```python
class Paper(BaseModel):
    title: str                              # 论文标题
    authors: List[str]                      # 作者列表
    abstract: str                           # 论文摘要
    arxiv_id: str                          # arXiv ID
    published: datetime                     # 发表日期
    updated: Optional[datetime]             # 更新日期
    categories: List[str]                  # 学科分类
    pdf_url: str                           # PDF链接
    entry_id: str                          # 完整条目ID
    summary: Optional[str]                 # 论文总结
    links: List[Dict[str, str]]            # 相关链接
```

#### SearchQuery 类

搜索查询配置。

```python
class SearchQuery(BaseModel):
    original_query: str                     # 原始查询
    field_queries: List[SearchFieldQuery]   # 字段查询
    max_results: int                        # 最大结果数
    sort_by: str                           # 排序方式
    sort_order: str                        # 排序顺序
    # ... 其他字段
```



## 支持的 arXiv 分类

### 计算机科学 (cs.*)
- cs.AI - 人工智能
- cs.LG - 机器学习
- cs.CV - 计算机视觉
- cs.CL - 计算语言学
- cs.RO - 机器人学
- 更多...

### 数学 (math.*)
- math.ST - 统计理论
- math.OC - 优化与控制
- math.PR - 概率论
- 更多...

### 物理 (physics.*)
- physics.comp-ph - 计算物理
- physics.data-an - 数据分析
- 更多...

### 统计学 (stat.*)
- stat.ML - 机器学习
- stat.ME - 统计方法
- 更多...

## 贡献

欢迎贡献代码！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 许可证

本项目采用 MIT 许可证。详情请见 [LICENSE](LICENSE) 文件。

## 更新日志

### 1.0.0 (2025-07-06)
- 初始版本发布
- 基本搜索功能
- 多字段搜索支持
- 异步 API
- 命令行工具

# ArXiv Search SDK API 文档

## 概述

ArXiv Search SDK 是一个功能强大的 Python 库，专门用于搜索和获取 arXiv 论文。它提供了简单易用的异步API，支持多种搜索方式，包括按标题、作者、摘要、分类等字段进行搜索。

## 核心特性

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
            print(f"PDF: {paper.pdf_url}")
            print("-" * 50)

asyncio.run(main())
```

## 核心类和方法

### ArxivClient 类

`ArxivClient` 是主要的客户端类，提供所有搜索功能。

#### 初始化

```python
from arxiv_search import ArxivClient

# 创建客户端实例
client = ArxivClient(timeout=30)  # 可选：设置超时时间（秒）

# 推荐使用异步上下文管理器
async with ArxivClient() as client:
    # 在这里进行搜索操作
    pass
```

#### 基本搜索方法

##### `search_papers(query: SearchQuery) -> SearchResult`

执行搜索查询，返回完整的搜索结果对象。

```python
from arxiv_search import ArxivClient, SearchQuery, SearchFieldQuery

async with ArxivClient() as client:
    query = SearchQuery(
        original_query="machine learning",
        field_queries=[
            SearchFieldQuery(field="ti", terms=["machine learning"]),
            SearchFieldQuery(field="abs", terms=["neural network"])
        ],
        max_results=10,
        sort_by="relevance"
    )
    
    result = await client.search_papers(query)
    print(f"找到 {result.total_found} 篇论文")
    for paper in result.papers:
        print(paper.title)
```

##### `search_by_title(title_terms: List[str], max_results: int = 10) -> List[Paper]`

按标题搜索论文。

```python
async with ArxivClient() as client:
    papers = await client.search_by_title(
        title_terms=["transformer", "attention"],
        max_results=5
    )
    
    for paper in papers:
        print(f"Title: {paper.title}")
        print(f"ArXiv ID: {paper.arxiv_id}")
```

##### `search_by_author(author_names: List[str], max_results: int = 10) -> List[Paper]`

按作者搜索论文。

```python
async with ArxivClient() as client:
    papers = await client.search_by_author(
        author_names=["Geoffrey Hinton"],
        max_results=5
    )
    
    for paper in papers:
        print(f"Title: {paper.title}")
        print(f"Authors: {', '.join(paper.authors)}")
```

##### `search_by_abstract(abstract_terms: List[str], max_results: int = 10) -> List[Paper]`

按摘要关键词搜索论文。

```python
async with ArxivClient() as client:
    papers = await client.search_by_abstract(
        abstract_terms=["deep learning", "neural network"],
        max_results=5
    )
    
    for paper in papers:
        print(f"Title: {paper.title}")
        print(f"Abstract: {paper.abstract[:100]}...")
```

##### `search_by_category(categories: List[str], max_results: int = 10) -> List[Paper]`

按学科分类搜索论文。

```python
async with ArxivClient() as client:
    papers = await client.search_by_category(
        categories=["cs.AI", "cs.LG"],
        max_results=10
    )
    
    for paper in papers:
        print(f"Title: {paper.title}")
        print(f"Categories: {', '.join(paper.categories)}")
```

#### 高级搜索方法

##### `advanced_search(**kwargs) -> List[Paper]`

执行高级组合搜索。

```python
async with ArxivClient() as client:
    papers = await client.advanced_search(
        title_terms=["transformer"],
        abstract_terms=["attention"],
        categories=["cs.AI", "cs.LG"],
        date_start="202301010000",  # 2023年1月1日
        date_end="202312312359",    # 2023年12月31日
        max_results=20,
        sort_by="submittedDate"
    )
    
    for paper in papers:
        print(f"Title: {paper.title}")
        print(f"Published: {paper.published}")
```

**参数说明:**

- `title_terms`: 标题关键词列表
- `author_names`: 作者姓名列表
- `abstract_terms`: 摘要关键词列表
- `categories`: 学科分类列表
- `date_start`: 开始日期 (格式: YYYYMMDDHHMM)
- `date_end`: 结束日期 (格式: YYYYMMDDHHMM)
- `max_results`: 最大结果数
- `sort_by`: 排序方式 ("relevance", "submittedDate", "lastUpdatedDate")

#### 便捷的学科分类搜索方法

##### `search_ai_papers(max_results: int = 10) -> List[Paper]`

搜索人工智能相关论文。

```python
async with ArxivClient() as client:
    papers = await client.search_ai_papers(max_results=10)
```

##### `search_ml_papers(max_results: int = 10) -> List[Paper]`

搜索机器学习相关论文。

```python
async with ArxivClient() as client:
    papers = await client.search_ml_papers(max_results=10)
```

##### `search_cv_papers(max_results: int = 10) -> List[Paper]`

搜索计算机视觉相关论文。

```python
async with ArxivClient() as client:
    papers = await client.search_cv_papers(max_results=10)
```

##### `search_nlp_papers(max_results: int = 10) -> List[Paper]`

搜索自然语言处理相关论文。

```python
async with ArxivClient() as client:
    papers = await client.search_nlp_papers(max_results=10)
```

##### `search_robotics_papers(max_results: int = 10) -> List[Paper]`

搜索机器人学相关论文。

```python
async with ArxivClient() as client:
    papers = await client.search_robotics_papers(max_results=10)
```

#### 其他实用方法

##### `search_multiple_queries(search_queries: List[SearchQuery]) -> List[Paper]`

并行搜索多个查询并合并结果。

```python
async with ArxivClient() as client:
    queries = [
        SearchQuery(original_query="machine learning", max_results=5),
        SearchQuery(original_query="deep learning", max_results=5)
    ]
    
    papers = await client.search_multiple_queries(queries)
    print(f"总共找到 {len(papers)} 篇论文")
```

##### `search_by_category_keyword(keyword: str, max_results: int = 10) -> List[Paper]`

根据关键词搜索相关学科分类的论文。

```python
async with ArxivClient() as client:
    papers = await client.search_by_category_keyword("machine learning", max_results=10)
```

## 数据模型

### Paper 类

表示 arXiv 论文的数据模型。

```python
from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel

class Paper(BaseModel):
    title: str                              # 论文标题
    authors: List[str]                      # 作者列表
    abstract: str                           # 论文摘要
    arxiv_id: str                          # arXiv ID
    published: datetime                     # 发表日期
    updated: Optional[datetime] = None      # 更新日期
    categories: List[str] = []             # 学科分类
    pdf_url: str                           # PDF链接
    entry_id: str                          # 完整条目ID
    summary: Optional[str] = None           # 论文总结
    links: List[Dict[str, str]] = []       # 相关链接
```

**属性说明:**

- `title`: 论文标题
- `authors`: 作者姓名列表
- `abstract`: 论文摘要或简介
- `arxiv_id`: arXiv 唯一标识符 (如 "2023.12345")
- `published`: 论文首次提交日期
- `updated`: 论文最后更新日期 (如果有)
- `categories`: 学科分类列表 (如 ["cs.AI", "cs.LG"])
- `pdf_url`: PDF 下载链接
- `entry_id`: arXiv 条目完整ID
- `summary`: 论文总结 (可选)
- `links`: 相关链接列表

### SearchQuery 类

搜索查询配置模型。

```python
class SearchQuery(BaseModel):
    original_query: str                     # 原始查询
    english_queries: List[str] = []         # 英文查询列表
    search_terms: List[str] = []           # 搜索关键词
    field_queries: List[SearchFieldQuery] = []  # 字段查询
    submitted_date_start: Optional[str] = None   # 开始日期
    submitted_date_end: Optional[str] = None     # 结束日期
    max_results: int = 10                   # 最大结果数
    sort_by: str = "relevance"             # 排序方式
    sort_order: str = "descending"         # 排序顺序
    recommendation_priority: str = "relevance"  # 推荐优先级
```

### SearchFieldQuery 类

特定字段搜索查询模型。

```python
class SearchFieldQuery(BaseModel):
    field: Literal["ti", "au", "abs", "co", "jr", "cat", "rn", "all"] = "all"
    terms: List[str]                        # 搜索关键词
```

**支持的字段:**

- `ti`: 标题 (Title)
- `au`: 作者 (Author)
- `abs`: 摘要 (Abstract)
- `co`: 评论 (Comment)
- `jr`: 期刊引用 (Journal Reference)
- `cat`: 学科分类 (Category) - 必须使用 arXiv 官方分类代码
- `rn`: 报告号 (Report Number)
- `all`: 主要内容字段 (Title + Abstract + Author + Comment)

### SearchResult 类

搜索结果封装模型。

```python
class SearchResult(BaseModel):
    query: SearchQuery                     # 执行的查询
    papers: List[Paper]                   # 搜索结果
    total_found: int                      # 总找到数量
    search_time: float                    # 搜索耗时
```

## 支持的 arXiv 分类

### 计算机科学 (cs.*)

- `cs.AI` - 人工智能
- `cs.LG` - 机器学习
- `cs.CV` - 计算机视觉与模式识别
- `cs.CL` - 计算与语言
- `cs.RO` - 机器人学
- `cs.IR` - 信息检索
- `cs.DB` - 数据库
- `cs.DS` - 数据结构与算法
- `cs.SE` - 软件工程
- `cs.NI` - 网络与互联网架构
- `cs.CR` - 密码学与安全
- `cs.HC` - 人机交互
- `cs.DC` - 分布式、并行和集群计算
- `cs.GT` - 计算机科学与博弈论
- `cs.GR` - 图形学

### 数学 (math.*)

- `math.ST` - 统计理论
- `math.OC` - 优化与控制
- `math.PR` - 概率论
- `math.NA` - 数值分析
- `math.CO` - 组合数学
- `math.AG` - 代数几何
- `math.AP` - 偏微分方程分析
- `math.NT` - 数论
- `math.DG` - 微分几何
- `math.FA` - 泛函分析

### 物理 (physics.*)

- `physics.comp-ph` - 计算物理
- `physics.data-an` - 数据分析、统计与概率
- `physics.app-ph` - 应用物理
- `physics.optics` - 光学
- `physics.bio-ph` - 生物物理
- `physics.chem-ph` - 化学物理
- `physics.med-ph` - 医学物理
- `physics.flu-dyn` - 流体动力学

### 统计学 (stat.*)

- `stat.ML` - 机器学习
- `stat.ME` - 统计方法
- `stat.AP` - 应用统计
- `stat.CO` - 计算统计
- `stat.TH` - 统计理论

### 电气工程 (eess.*)

- `eess.AS` - 音频与语音处理
- `eess.IV` - 图像与视频处理
- `eess.SP` - 信号处理
- `eess.SY` - 系统与控制

### 定量生物学 (q-bio.*)

- `q-bio.NC` - 神经与认知
- `q-bio.BM` - 生物大分子
- `q-bio.GN` - 基因组学
- `q-bio.QM` - 定量方法

### 定量金融 (q-fin.*)

- `q-fin.CP` - 计算金融
- `q-fin.MF` - 数学金融
- `q-fin.RM` - 风险管理
- `q-fin.ST` - 统计金融

## 错误处理

### 常见错误

### 1. 无效的分类代码

   ```python
   # 错误示例
   papers = await client.search_by_category(["invalid_category"])
   # 会抛出: ValueError: Invalid arXiv categories: ['invalid_category']
   ```

### 2. 网络超时

   ```python
   # 设置更长的超时时间
   client = ArxivClient(timeout=60)
   ```

### 3. 查询结果为空

   ```python
   result = await client.search_papers(query)
   if not result.papers:
       print("未找到相关论文")
   ```

### 最佳实践

### 1. 使用异步上下文管理器

   ```python
   async with ArxivClient() as client:
       # 搜索操作
       pass
   ```

### 2. 合理设置结果数量

   ```python
   # 避免请求过多结果
   papers = await client.search_ml_papers(max_results=50)  # 合理范围
   ```

### 3. 异常处理

   ```python
   try:
       papers = await client.search_by_category(["cs.AI"])
   except ValueError as e:
       print(f"分类错误: {e}")
   except Exception as e:
       print(f"搜索失败: {e}")
   ```

## 性能优化

### 并行搜索

```python
# 并行搜索多个查询
queries = [
    SearchQuery(original_query="machine learning", max_results=10),
    SearchQuery(original_query="deep learning", max_results=10),
    SearchQuery(original_query="neural network", max_results=10)
]

papers = await client.search_multiple_queries(queries)
```

### 缓存结果

```python
# 缓存热门查询结果
cache = {}

async def cached_search(query_str):
    if query_str in cache:
        return cache[query_str]
    
    async with ArxivClient() as client:
        papers = await client.search_ml_papers(max_results=10)
        cache[query_str] = papers
        return papers
```

## 示例和用例

### 1. 文献综述助手

```python
async def literature_review(topic: str, max_papers: int = 50):
    """文献综述助手"""
    async with ArxivClient() as client:
        # 搜索相关论文
        papers = await client.search_by_category_keyword(topic, max_papers)
        
        # 按年份分组
        by_year = {}
        for paper in papers:
            year = paper.published.year
            if year not in by_year:
                by_year[year] = []
            by_year[year].append(paper)
        
        # 输出统计信息
        print(f"找到 {len(papers)} 篇关于 '{topic}' 的论文")
        for year in sorted(by_year.keys(), reverse=True):
            print(f"{year}: {len(by_year[year])} 篇")
        
        return papers
```

### 2. 作者研究追踪

```python
async def track_author_research(author_name: str):
    """追踪作者研究"""
    async with ArxivClient() as client:
        papers = await client.search_by_author([author_name], max_results=100)
        
        # 按分类统计
        categories = {}
        for paper in papers:
            for cat in paper.categories:
                categories[cat] = categories.get(cat, 0) + 1
        
        print(f"{author_name} 的研究领域分布:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count} 篇")
        
        return papers
```

### 3. 趋势分析

```python
async def analyze_trends(keywords: List[str], years: int = 5):
    """分析研究趋势"""
    from datetime import datetime, timedelta
    
    async with ArxivClient() as client:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365 * years)
        
        results = {}
        for keyword in keywords:
            papers = await client.advanced_search(
                abstract_terms=[keyword],
                date_start=start_date.strftime("%Y%m%d0000"),
                date_end=end_date.strftime("%Y%m%d2359"),
                max_results=1000
            )
            
            # 按年份统计
            yearly_count = {}
            for paper in papers:
                year = paper.published.year
                yearly_count[year] = yearly_count.get(year, 0) + 1
            
            results[keyword] = yearly_count
        
        return results
```

## 更新日志

### 1.0.0 (2025-07-06)

- 初始版本发布
- 基本搜索功能
- 多字段搜索支持
- 异步 API
- 命令行工具
- 完整的数据模型
- 支持所有 arXiv 分类

## 许可证

本项目采用 MIT 许可证。详情请见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎贡献代码！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 联系方式

如有问题或建议，请通过以下方式联系：

- GitHub Issues: [项目地址](https://github.com/your-username/arxiv-search-sdk)
- 邮箱: `your-email@example.com`

---

© 2025 ArXiv Search SDK. All rights reserved.

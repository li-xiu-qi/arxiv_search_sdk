"""
arXiv API客户端
"""
import asyncio
import aiohttp
import feedparser
import time
from typing import List, Optional
from datetime import datetime
from loguru import logger

from .models import Paper, SearchQuery, SearchFieldQuery, SearchResult

class ArxivClient:
    """arXiv API客户端"""
    
    BASE_URL = "http://export.arxiv.org/api/query"
    DEFAULT_TIMEOUT = 30
    
    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        """
        初始化客户端
        
        Args:
            timeout: 请求超时时间（秒）
        """
        self.timeout = timeout
        self.session = None
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
    
    def _build_search_query(self, search_query: SearchQuery) -> str:
        """构建arXiv搜索查询"""
        query_parts = []
        
        # 处理特定字段查询
        if search_query.field_queries:
            for field_query in search_query.field_queries:
                field_parts = []
                for term in field_query.terms:
                    if ' ' in term:  # 如果包含空格，用引号包围
                        field_parts.append(f'{field_query.field}:"{term}"')
                    else:
                        field_parts.append(f'{field_query.field}:{term}')
                
                if len(field_parts) > 1:
                    # 同一字段的多个词用 OR 连接
                    query_parts.append(f"({' OR '.join(field_parts)})")
                else:
                    query_parts.append(field_parts[0])
        
        # 处理传统的搜索词（智能搜索策略）
        elif search_query.search_terms:
            # 使用智能多字段搜索策略
            smart_query_parts = self._build_smart_search(search_query.search_terms)
            query_parts.extend(smart_query_parts)
        
        # 添加日期范围过滤
        if search_query.submitted_date_start and search_query.submitted_date_end:
            date_filter = f"submittedDate:[{search_query.submitted_date_start}+TO+{search_query.submitted_date_end}]"
            query_parts.append(date_filter)
        
        # 用 AND 连接不同类型的查询
        final_query = " AND ".join(query_parts) if query_parts else "all:*"
        
        return final_query
    
    def _build_smart_search(self, search_terms: List[str]) -> List[str]:
        """
        构建智能搜索查询
        
        策略：
        1. 对于每个搜索词，同时搜索标题、摘要和所有字段
        2. 给予标题更高的权重（通过OR连接多个字段）
        3. 使用括号确保正确的逻辑分组
        """
        if not search_terms:
            return ["all:*"]
        
        query_parts = []
        
        for term in search_terms:
            # 为每个搜索词构建多字段查询
            if ' ' in term:  # 短语搜索
                term_query = f'(ti:"{term}" OR abs:"{term}" OR all:"{term}")'
            else:  # 单词搜索
                term_query = f'(ti:{term} OR abs:{term} OR all:{term})'
            
            query_parts.append(term_query)
        
        # 如果有多个搜索词，用AND连接（所有词都要匹配）
        if len(query_parts) > 1:
            return [f"({' AND '.join(query_parts)})"]
        else:
            return query_parts
    
    def _parse_entry(self, entry) -> Paper:
        """解析arXiv条目为Paper对象"""
        # 提取arXiv ID
        arxiv_id = entry.id.split('/')[-1]
        if 'v' in arxiv_id:
            arxiv_id = arxiv_id.split('v')[0]
        
        # 解析作者
        authors = []
        if hasattr(entry, 'authors'):
            authors = [author.name for author in entry.authors]
        elif hasattr(entry, 'author'):
            authors = [entry.author]
        
        # 解析分类
        categories = []
        if hasattr(entry, 'tags'):
            categories = [tag.term for tag in entry.tags]
        
        # 解析链接
        links = []
        if hasattr(entry, 'links'):
            links = [{"href": link.href, "rel": link.rel, "type": getattr(link, 'type', '')} 
                    for link in entry.links]
        
        # 找到PDF链接
        pdf_url = ""
        for link in entry.links:
            if hasattr(link, 'type') and link.type == 'application/pdf':
                pdf_url = link.href
                break
        if not pdf_url and hasattr(entry, 'link'):
            pdf_url = entry.link.replace('/abs/', '/pdf/') + '.pdf'
        
        # 解析日期
        published = datetime.strptime(entry.published, '%Y-%m-%dT%H:%M:%SZ')
        updated = None
        if hasattr(entry, 'updated'):
            updated = datetime.strptime(entry.updated, '%Y-%m-%dT%H:%M:%SZ')
        
        return Paper(
            title=entry.title.replace('\n', ' ').strip(),
            authors=authors,
            abstract=entry.summary.replace('\n', ' ').strip(),
            arxiv_id=arxiv_id,
            published=published,
            updated=updated,
            categories=categories,
            pdf_url=pdf_url,
            entry_id=entry.id,
            links=links
        )
    
    async def search_papers(self, search_query: SearchQuery) -> SearchResult:
        """
        搜索arXiv论文
        
        Args:
            search_query: 搜索查询对象
            
        Returns:
            搜索结果对象
        """
        if not self.session:
            raise RuntimeError("Client not initialized. Use async context manager.")
        
        start_time = time.time()
        
        # 构建查询字符串
        query_str = self._build_search_query(search_query)
        
        # 构建请求参数
        params = {
            'search_query': query_str,
            'start': 0,
            'max_results': search_query.max_results,
            'sortBy': search_query.sort_by,
            'sortOrder': search_query.sort_order
        }
        
        logger.info(f"Searching arXiv with query: {query_str}")
        
        try:
            async with self.session.get(self.BASE_URL, params=params) as response:
                if response.status != 200:
                    logger.error(f"arXiv API error: {response.status}")
                    return SearchResult(
                        query=search_query,
                        papers=[],
                        total_found=0,
                        search_time=time.time() - start_time
                    )
                
                content = await response.text()
                
                # 解析RSS feed
                feed = feedparser.parse(content)
                
                if not feed.entries:
                    logger.warning("No papers found for query")
                    return SearchResult(
                        query=search_query,
                        papers=[],
                        total_found=0,
                        search_time=time.time() - start_time
                    )
                
                papers = []
                for entry in feed.entries:
                    try:
                        paper = self._parse_entry(entry)
                        papers.append(paper)
                    except Exception as e:
                        logger.warning(f"Failed to parse entry: {e}")
                        continue
                
                # 从feed中获取总数（如果可用）
                total_found = len(papers)
                if hasattr(feed, 'feed') and hasattr(feed.feed, 'opensearch_totalresults'):
                    total_found = int(feed.feed.opensearch_totalresults)
                
                search_time = time.time() - start_time
                logger.info(f"Found {len(papers)} papers in {search_time:.2f} seconds")
                
                return SearchResult(
                    query=search_query,
                    papers=papers,
                    total_found=total_found,
                    search_time=search_time
                )
                
        except Exception as e:
            logger.error(f"Error searching arXiv: {e}")
            return SearchResult(
                query=search_query,
                papers=[],
                total_found=0,
                search_time=time.time() - start_time
            )
    
    async def search_multiple_queries(self, search_queries: List[SearchQuery]) -> List[Paper]:
        """
        并行搜索多个查询
        
        Args:
            search_queries: 搜索查询列表
            
        Returns:
            所有论文的合并列表（去重）
        """
        tasks = [self.search_papers(query) for query in search_queries]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_papers = []
        seen_ids = set()
        
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Search task failed: {result}")
                continue
            
            for paper in result.papers:
                if paper.arxiv_id not in seen_ids:
                    all_papers.append(paper)
                    seen_ids.add(paper.arxiv_id)
        
        logger.info(f"Total unique papers found: {len(all_papers)}")
        return all_papers
    
    # 便捷搜索方法
    async def search_by_title(self, title_terms: List[str], max_results: int = 10) -> List[Paper]:
        """按标题搜索"""
        search_query = SearchQuery(
            original_query=" ".join(title_terms),
            field_queries=[SearchFieldQuery(field="ti", terms=title_terms)],
            max_results=max_results
        )
        result = await self.search_papers(search_query)
        return result.papers
    
    async def search_by_author(self, author_names: List[str], max_results: int = 10) -> List[Paper]:
        """按作者搜索"""
        search_query = SearchQuery(
            original_query=" ".join(author_names),
            field_queries=[SearchFieldQuery(field="au", terms=author_names)],
            max_results=max_results
        )
        result = await self.search_papers(search_query)
        return result.papers
    
    async def search_by_abstract(self, abstract_terms: List[str], max_results: int = 10) -> List[Paper]:
        """按摘要关键词搜索"""
        search_query = SearchQuery(
            original_query=" ".join(abstract_terms),
            field_queries=[SearchFieldQuery(field="abs", terms=abstract_terms)],
            max_results=max_results
        )
        result = await self.search_papers(search_query)
        return result.papers
    
    async def search_by_category(self, categories: List[str], max_results: int = 10) -> List[Paper]:
        """
        按学科分类搜索
        
        Args:
            categories: arXiv 官方分类代码列表，如 ["cs.AI", "cs.LG"]
            max_results: 最大结果数
            
        Returns:
            论文列表
            
        Raises:
            ValueError: 如果提供的分类代码无效
        """
        from .categories import validate_category
        
        # 验证所有分类代码
        invalid_cats = [cat for cat in categories if not validate_category(cat)]
        if invalid_cats:
            available_examples = ["cs.AI", "cs.LG", "cs.CV", "cs.CL", "math.ST", "physics.comp-ph"]
            raise ValueError(f"Invalid arXiv categories: {invalid_cats}. "
                           f"Must use official category codes. Examples: {available_examples}")
        
        search_query = SearchQuery(
            original_query=f"categories: {', '.join(categories)}",
            field_queries=[SearchFieldQuery(field="cat", terms=categories)],
            max_results=max_results
        )
        result = await self.search_papers(search_query)
        return result.papers
    
    async def advanced_search(
        self,
        title_terms: Optional[List[str]] = None,
        author_names: Optional[List[str]] = None,
        abstract_terms: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
        date_start: Optional[str] = None,
        date_end: Optional[str] = None,
        max_results: int = 10,
        sort_by: str = "relevance"
    ) -> List[Paper]:
        """高级组合搜索"""
        field_queries = []
        query_parts = []
        
        if title_terms:
            field_queries.append(SearchFieldQuery(field="ti", terms=title_terms))
            query_parts.append(f"title:{' '.join(title_terms)}")
        
        if author_names:
            field_queries.append(SearchFieldQuery(field="au", terms=author_names))
            query_parts.append(f"author:{' '.join(author_names)}")
        
        if abstract_terms:
            field_queries.append(SearchFieldQuery(field="abs", terms=abstract_terms))
            query_parts.append(f"abstract:{' '.join(abstract_terms)}")
        
        if categories:
            field_queries.append(SearchFieldQuery(field="cat", terms=categories))
            query_parts.append(f"category:{' '.join(categories)}")
        
        search_query = SearchQuery(
            original_query=" | ".join(query_parts),
            field_queries=field_queries,
            submitted_date_start=date_start,
            submitted_date_end=date_end,
            max_results=max_results,
            sort_by=sort_by
        )
        
        result = await self.search_papers(search_query)
        return result.papers
    
    # 便捷的学科分类搜索方法
    async def search_ai_papers(self, max_results: int = 10) -> List[Paper]:
        """搜索人工智能相关论文"""
        return await self.search_by_category(["cs.AI"], max_results)
    
    async def search_ml_papers(self, max_results: int = 10) -> List[Paper]:
        """搜索机器学习相关论文"""
        return await self.search_by_category(["cs.LG", "stat.ML"], max_results)
    
    async def search_cv_papers(self, max_results: int = 10) -> List[Paper]:
        """搜索计算机视觉相关论文"""
        return await self.search_by_category(["cs.CV"], max_results)
    
    async def search_nlp_papers(self, max_results: int = 10) -> List[Paper]:
        """搜索自然语言处理相关论文"""
        return await self.search_by_category(["cs.CL"], max_results)
    
    async def search_robotics_papers(self, max_results: int = 10) -> List[Paper]:
        """搜索机器人学相关论文"""
        return await self.search_by_category(["cs.RO"], max_results)
    
    async def search_by_category_keyword(self, keyword: str, max_results: int = 10) -> List[Paper]:
        """
        根据关键词搜索相关学科分类的论文
        
        Args:
            keyword: 关键词，如 "machine learning", "computer vision"
            max_results: 最大结果数
            
        Returns:
            论文列表
        """
        from .categories import search_categories_by_keyword
        
        # 根据关键词找到相关分类
        categories = search_categories_by_keyword(keyword)
        if not categories:
            logger.warning(f"No categories found for keyword: {keyword}")
            return []
        
        logger.info(f"Found categories for '{keyword}': {categories}")
        return await self.search_by_category(categories, max_results)


# 便捷函数
async def search_arxiv_papers(search_queries: List[SearchQuery]) -> List[Paper]:
    """搜索arXiv论文的便捷函数"""
    async with ArxivClient() as client:
        return await client.search_multiple_queries(search_queries)

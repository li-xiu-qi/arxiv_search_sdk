"""
测试arXiv客户端
"""
import pytest
import asyncio
from datetime import datetime
from arxiv_search import ArxivClient, SearchQuery, SearchFieldQuery

class TestArxivClient:
    """测试ArxivClient类"""
    
    @pytest.mark.asyncio
    async def test_basic_search(self):
        """测试基本搜索功能"""
        async with ArxivClient() as client:
            papers = await client.search_ml_papers(max_results=3)
            
            assert len(papers) <= 3
            assert len(papers) > 0
            
            # 检查第一篇论文的基本属性
            paper = papers[0]
            assert paper.title is not None
            assert paper.arxiv_id is not None
            assert paper.authors is not None
            assert paper.abstract is not None
            assert isinstance(paper.published, datetime)
            assert paper.pdf_url is not None
    
    @pytest.mark.asyncio
    async def test_search_by_title(self):
        """测试按标题搜索"""
        async with ArxivClient() as client:
            papers = await client.search_by_title(["transformer"], max_results=2)
            
            assert len(papers) <= 2
            for paper in papers:
                # 标题应该包含"transformer"（不区分大小写）
                assert "transformer" in paper.title.lower()
    
    @pytest.mark.asyncio
    async def test_search_by_category(self):
        """测试按分类搜索"""
        async with ArxivClient() as client:
            papers = await client.search_by_category(["cs.AI"], max_results=3)
            
            assert len(papers) <= 3
            for paper in papers:
                # 论文应该包含cs.AI分类
                assert "cs.AI" in paper.categories
    
    @pytest.mark.asyncio
    async def test_invalid_category(self):
        """测试无效分类"""
        async with ArxivClient() as client:
            with pytest.raises(ValueError):
                await client.search_by_category(["invalid.category"], max_results=1)
    
    @pytest.mark.asyncio
    async def test_advanced_search(self):
        """测试高级搜索"""
        async with ArxivClient() as client:
            papers = await client.advanced_search(
                title_terms=["neural"],
                categories=["cs.LG"],
                max_results=2
            )
            
            assert len(papers) <= 2
            for paper in papers:
                # 标题应该包含"neural"
                assert "neural" in paper.title.lower()
                # 应该包含机器学习分类
                assert any("cs.LG" in cat or "stat.ML" in cat for cat in paper.categories)
    
    @pytest.mark.asyncio
    async def test_custom_search_query(self):
        """测试自定义搜索查询"""
        async with ArxivClient() as client:
            query = SearchQuery(
                original_query="test query",
                field_queries=[
                    SearchFieldQuery(field="cat", terms=["cs.AI"])
                ],
                max_results=2
            )
            
            result = await client.search_papers(query)
            
            assert len(result.papers) <= 2
            assert result.total_found >= 0
            assert result.search_time > 0
            
            for paper in result.papers:
                assert "cs.AI" in paper.categories
    
    @pytest.mark.asyncio
    async def test_specialized_search_methods(self):
        """测试专门的搜索方法"""
        async with ArxivClient() as client:
            # 测试AI论文搜索
            ai_papers = await client.search_ai_papers(max_results=1)
            assert len(ai_papers) <= 1
            if ai_papers:
                assert "cs.AI" in ai_papers[0].categories
            
            # 测试CV论文搜索
            cv_papers = await client.search_cv_papers(max_results=1)
            assert len(cv_papers) <= 1
            if cv_papers:
                assert "cs.CV" in cv_papers[0].categories
            
            # 测试NLP论文搜索
            nlp_papers = await client.search_nlp_papers(max_results=1)
            assert len(nlp_papers) <= 1
            if nlp_papers:
                assert "cs.CL" in nlp_papers[0].categories
    
    @pytest.mark.asyncio
    async def test_multiple_queries(self):
        """测试多查询搜索"""
        async with ArxivClient() as client:
            queries = [
                SearchQuery(
                    original_query="AI papers",
                    field_queries=[SearchFieldQuery(field="cat", terms=["cs.AI"])],
                    max_results=1
                ),
                SearchQuery(
                    original_query="ML papers", 
                    field_queries=[SearchFieldQuery(field="cat", terms=["cs.LG"])],
                    max_results=1
                )
            ]
            
            papers = await client.search_multiple_queries(queries)
            
            # 应该返回去重后的论文
            assert len(papers) <= 2
            
            # 检查是否有重复的论文ID
            paper_ids = [paper.arxiv_id for paper in papers]
            assert len(paper_ids) == len(set(paper_ids))  # 无重复
    
    def test_client_context_manager(self):
        """测试客户端上下文管理器"""
        async def test_async():
            async with ArxivClient() as client:
                assert client.session is not None
            # 上下文管理器退出后，session应该被关闭
            assert client.session.closed
        
        asyncio.run(test_async())

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
测试数据模型
"""
import pytest
from datetime import datetime
from arxiv_search import Paper, SearchQuery, SearchFieldQuery

class TestPaper:
    """测试Paper数据模型"""
    
    def test_paper_creation(self):
        """测试创建Paper对象"""
        paper = Paper(
            title="Test Paper",
            authors=["Author One", "Author Two"],
            abstract="This is a test abstract",
            arxiv_id="2023.12345",
            published=datetime(2023, 1, 1),
            categories=["cs.AI", "cs.LG"],
            pdf_url="https://arxiv.org/pdf/2023.12345.pdf",
            entry_id="http://arxiv.org/abs/2023.12345v1"
        )
        
        assert paper.title == "Test Paper"
        assert len(paper.authors) == 2
        assert paper.authors[0] == "Author One"
        assert paper.arxiv_id == "2023.12345"
        assert paper.published.year == 2023
        assert "cs.AI" in paper.categories
        assert "cs.LG" in paper.categories
    
    def test_paper_json_serialization(self):
        """测试Paper对象JSON序列化"""
        paper = Paper(
            title="Test Paper",
            authors=["Author One"],
            abstract="Test abstract",
            arxiv_id="2023.12345",
            published=datetime(2023, 1, 1),
            categories=["cs.AI"],
            pdf_url="https://arxiv.org/pdf/2023.12345.pdf",
            entry_id="http://arxiv.org/abs/2023.12345v1"
        )
        
        paper_dict = paper.dict()
        assert "title" in paper_dict
        assert "authors" in paper_dict
        assert "published" in paper_dict
        
        # 检查日期序列化
        assert isinstance(paper_dict["published"], datetime)

class TestSearchFieldQuery:
    """测试SearchFieldQuery数据模型"""
    
    def test_search_field_query_creation(self):
        """测试创建SearchFieldQuery对象"""
        query = SearchFieldQuery(
            field="ti",
            terms=["machine learning", "deep learning"]
        )
        
        assert query.field == "ti"
        assert len(query.terms) == 2
        assert "machine learning" in query.terms
    
    def test_category_validation(self):
        """测试分类字段验证"""
        # 有效分类应该通过验证
        query = SearchFieldQuery(
            field="cat",
            terms=["cs.AI", "cs.LG"]
        )
        assert query.field == "cat"
        assert len(query.terms) == 2
        
        # 无效分类应该抛出错误
        with pytest.raises(ValueError):
            SearchFieldQuery(
                field="cat",
                terms=["invalid.category"]
            )
    
    def test_non_category_field(self):
        """测试非分类字段不需要验证"""
        query = SearchFieldQuery(
            field="ti",
            terms=["any term"]  # 标题字段不需要验证分类代码
        )
        assert query.field == "ti"
        assert "any term" in query.terms

class TestSearchQuery:
    """测试SearchQuery数据模型"""
    
    def test_search_query_creation(self):
        """测试创建SearchQuery对象"""
        query = SearchQuery(
            original_query="machine learning papers",
            search_terms=["machine", "learning"],
            max_results=20,
            sort_by="submittedDate"
        )
        
        assert query.original_query == "machine learning papers"
        assert len(query.search_terms) == 2
        assert query.max_results == 20
        assert query.sort_by == "submittedDate"
    
    def test_search_query_with_field_queries(self):
        """测试包含字段查询的SearchQuery"""
        field_query = SearchFieldQuery(field="ti", terms=["transformer"])
        
        query = SearchQuery(
            original_query="transformer papers",
            field_queries=[field_query],
            max_results=10
        )
        
        assert len(query.field_queries) == 1
        assert query.field_queries[0].field == "ti"
        assert "transformer" in query.field_queries[0].terms
    
    def test_search_query_defaults(self):
        """测试SearchQuery的默认值"""
        query = SearchQuery(original_query="test")
        
        assert query.max_results == 10
        assert query.sort_by == "relevance"
        assert query.sort_order == "descending"
        assert query.recommendation_priority == "relevance"
        assert len(query.field_queries) == 0
        assert len(query.search_terms) == 0
    
    def test_date_range_query(self):
        """测试日期范围查询"""
        query = SearchQuery(
            original_query="2023 papers",
            submitted_date_start="202301010000",
            submitted_date_end="202312312359"
        )
        
        assert query.submitted_date_start == "202301010000"
        assert query.submitted_date_end == "202312312359"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

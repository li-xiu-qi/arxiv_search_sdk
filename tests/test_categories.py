"""
测试分类功能
"""
import pytest
from arxiv_search import (
    ARXIV_CATEGORIES, 
    CATEGORY_GROUPS, 
    POPULAR_CS_CATEGORIES,
    validate_category,
    get_category_description,
    search_categories_by_keyword,
    get_categories_by_group
)

class TestArxivCategories:
    """测试arXiv分类相关功能"""
    
    def test_category_constants(self):
        """测试分类常量"""
        # 检查主要分类字典不为空
        assert len(ARXIV_CATEGORIES) > 0
        assert len(CATEGORY_GROUPS) > 0
        assert len(POPULAR_CS_CATEGORIES) > 0
        
        # 检查常见分类是否存在
        assert "cs.AI" in ARXIV_CATEGORIES
        assert "cs.LG" in ARXIV_CATEGORIES
        assert "cs.CV" in ARXIV_CATEGORIES
        assert "cs.CL" in ARXIV_CATEGORIES
        
        # 检查分类组
        assert "Computer Science" in CATEGORY_GROUPS
        assert "Mathematics" in CATEGORY_GROUPS
        assert "Physics" in CATEGORY_GROUPS
    
    def test_validate_category(self):
        """测试分类验证"""
        # 有效分类
        assert validate_category("cs.AI") == True
        assert validate_category("cs.LG") == True
        assert validate_category("math.ST") == True
        assert validate_category("physics.comp-ph") == True
        
        # 无效分类
        assert validate_category("invalid.category") == False
        assert validate_category("cs.INVALID") == False
        assert validate_category("") == False
    
    def test_get_category_description(self):
        """测试获取分类描述"""
        # 有效分类
        desc = get_category_description("cs.AI")
        assert "人工智能" in desc or "Artificial Intelligence" in desc
        
        desc = get_category_description("cs.LG")
        assert "机器学习" in desc or "Machine Learning" in desc
        
        # 无效分类
        desc = get_category_description("invalid.category")
        assert "Unknown category" in desc
    
    def test_search_categories_by_keyword(self):
        """测试按关键词搜索分类"""
        # 搜索机器学习相关
        ml_categories = search_categories_by_keyword("machine learning")
        assert len(ml_categories) > 0
        assert "cs.LG" in ml_categories
        assert "stat.ML" in ml_categories
        
        # 搜索人工智能相关
        ai_categories = search_categories_by_keyword("artificial intelligence")
        assert len(ai_categories) > 0
        assert "cs.AI" in ai_categories
        
        # 搜索计算机视觉相关
        cv_categories = search_categories_by_keyword("computer vision")
        assert len(cv_categories) > 0
        assert "cs.CV" in cv_categories
        
        # 搜索不存在的关键词
        empty_categories = search_categories_by_keyword("nonexistent keyword")
        assert len(empty_categories) == 0
    
    def test_get_categories_by_group(self):
        """测试按组获取分类"""
        # 计算机科学组
        cs_categories = get_categories_by_group("Computer Science")
        assert len(cs_categories) > 0
        assert "cs.AI" in cs_categories
        assert "cs.LG" in cs_categories
        assert "cs.CV" in cs_categories
        
        # 数学组
        math_categories = get_categories_by_group("Mathematics")
        assert len(math_categories) > 0
        assert "math.ST" in math_categories
        assert "math.PR" in math_categories
        
        # 物理组
        physics_categories = get_categories_by_group("Physics")
        assert len(physics_categories) > 0
        assert "physics.comp-ph" in physics_categories
        
        # 不存在的组
        empty_categories = get_categories_by_group("Nonexistent Group")
        assert len(empty_categories) == 0
    
    def test_popular_cs_categories(self):
        """测试热门计算机科学分类"""
        # 检查热门分类都是有效的
        for category in POPULAR_CS_CATEGORIES:
            assert validate_category(category) == True
            assert category.startswith("cs.")
        
        # 检查包含常见的AI相关分类
        assert "cs.AI" in POPULAR_CS_CATEGORIES
        assert "cs.LG" in POPULAR_CS_CATEGORIES
        assert "cs.CV" in POPULAR_CS_CATEGORIES
        assert "cs.CL" in POPULAR_CS_CATEGORIES
    
    def test_category_groups_completeness(self):
        """测试分类组的完整性"""
        # 收集所有组中的分类
        all_grouped_categories = set()
        for group_categories in CATEGORY_GROUPS.values():
            all_grouped_categories.update(group_categories)
        
        # 检查主要分类是否都在某个组中
        main_prefixes = ["cs.", "math.", "physics.", "stat.", "econ.", "eess.", "q-bio.", "q-fin."]
        for category in ARXIV_CATEGORIES.keys():
            if any(category.startswith(prefix) for prefix in main_prefixes):
                assert category in all_grouped_categories, f"Category {category} not in any group"
    
    def test_case_insensitive_keyword_search(self):
        """测试关键词搜索的大小写不敏感性"""
        # 大写搜索
        upper_results = search_categories_by_keyword("MACHINE LEARNING")
        # 小写搜索
        lower_results = search_categories_by_keyword("machine learning")
        # 混合大小写搜索
        mixed_results = search_categories_by_keyword("Machine Learning")
        
        # 结果应该相同
        assert set(upper_results) == set(lower_results)
        assert set(lower_results) == set(mixed_results)
        
        # 都应该包含机器学习相关分类
        assert "cs.LG" in upper_results
        assert "stat.ML" in lower_results

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

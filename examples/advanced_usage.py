"""
高级搜索示例
"""
import asyncio
from arxiv_search import ArxivClient, SearchQuery, SearchFieldQuery

async def advanced_search_example():
    """高级组合搜索示例"""
    print("=== 高级组合搜索示例 ===")
    
    async with ArxivClient() as client:
        # 组合搜索：标题包含"deep learning"，摘要包含"neural network"
        papers = await client.advanced_search(
            title_terms=["deep learning"],
            abstract_terms=["neural network"],
            categories=["cs.AI", "cs.LG"],
            max_results=5,
            sort_by="submittedDate"
        )
        
        print(f"找到 {len(papers)} 篇论文:")
        for i, paper in enumerate(papers, 1):
            print(f"\n{i}. {paper.title}")
            print(f"   分类: {', '.join(paper.categories)}")
            print(f"   发表时间: {paper.published.strftime('%Y-%m-%d')}")

async def custom_query_example():
    """自定义查询示例"""
    print("\n=== 自定义查询示例 ===")
    
    async with ArxivClient() as client:
        # 创建复杂的自定义查询
        query = SearchQuery(
            original_query="transformer attention mechanism",
            field_queries=[
                SearchFieldQuery(field="ti", terms=["transformer"]),
                SearchFieldQuery(field="abs", terms=["attention", "mechanism"]),
                SearchFieldQuery(field="cat", terms=["cs.AI", "cs.CL"])
            ],
            max_results=5,
            sort_by="relevance"
        )
        
        result = await client.search_papers(query)
        
        print(f"找到 {len(result.papers)} 篇论文 (共 {result.total_found} 篇, 耗时 {result.search_time:.2f}s):")
        for i, paper in enumerate(result.papers, 1):
            print(f"\n{i}. {paper.title}")
            print(f"   ArXiv ID: {paper.arxiv_id}")
            print(f"   分类: {', '.join(paper.categories)}")

async def date_range_search_example():
    """日期范围搜索示例"""
    print("\n=== 日期范围搜索示例 ===")
    
    async with ArxivClient() as client:
        # 搜索2023年的机器学习论文
        papers = await client.advanced_search(
            categories=["cs.LG"],
            date_start="202301010000",  # 2023年1月1日
            date_end="202312312359",    # 2023年12月31日
            max_results=3,
            sort_by="submittedDate"
        )
        
        print(f"找到 {len(papers)} 篇2023年的机器学习论文:")
        for i, paper in enumerate(papers, 1):
            print(f"\n{i}. {paper.title}")
            print(f"   发表时间: {paper.published.strftime('%Y-%m-%d')}")

async def multiple_categories_example():
    """多分类搜索示例"""
    print("\n=== 多分类搜索示例 ===")
    
    async with ArxivClient() as client:
        # 搜索多个相关分类
        papers = await client.search_by_category([
            "cs.AI",      # 人工智能
            "cs.LG",      # 机器学习
            "cs.CV",      # 计算机视觉
            "cs.CL"       # 计算语言学
        ], max_results=5)
        
        print(f"找到 {len(papers)} 篇AI相关论文:")
        for i, paper in enumerate(papers, 1):
            print(f"\n{i}. {paper.title}")
            print(f"   分类: {', '.join(paper.categories)}")

async def main():
    """主函数"""
    await advanced_search_example()
    await custom_query_example()
    await date_range_search_example()
    await multiple_categories_example()

if __name__ == "__main__":
    asyncio.run(main())

"""
分类搜索示例
"""
import asyncio
from arxiv_search import ArxivClient, ARXIV_CATEGORIES, search_categories_by_keyword

async def popular_categories_example():
    """热门分类搜索示例"""
    print("=== 热门分类搜索示例 ===")
    
    async with ArxivClient() as client:
        # 搜索不同领域的论文
        categories = {
            "人工智能": "cs.AI",
            "机器学习": "cs.LG", 
            "计算机视觉": "cs.CV",
            "自然语言处理": "cs.CL",
            "机器人学": "cs.RO"
        }
        
        for field_name, category in categories.items():
            papers = await client.search_by_category([category], max_results=2)
            print(f"\n{field_name} ({category}) - 找到 {len(papers)} 篇论文:")
            
            for i, paper in enumerate(papers, 1):
                print(f"  {i}. {paper.title}")
                print(f"     ArXiv ID: {paper.arxiv_id}")

async def search_by_keyword_example():
    """按关键词搜索相关分类示例"""
    print("\n=== 按关键词搜索相关分类示例 ===")
    
    keywords = ["machine learning", "computer vision", "neural network"]
    
    for keyword in keywords:
        categories = search_categories_by_keyword(keyword)
        print(f"\n关键词 '{keyword}' 相关分类:")
        for cat in categories[:3]:  # 只显示前3个
            description = ARXIV_CATEGORIES[cat]
            print(f"  {cat} - {description}")

async def math_physics_example():
    """数学和物理分类示例"""
    print("\n=== 数学和物理分类示例 ===")
    
    async with ArxivClient() as client:
        # 搜索统计学相关论文
        stat_papers = await client.search_by_category(["stat.ML", "math.ST"], max_results=2)
        print(f"统计学/数学相关论文 - 找到 {len(stat_papers)} 篇:")
        
        for i, paper in enumerate(stat_papers, 1):
            print(f"  {i}. {paper.title}")
            print(f"     分类: {', '.join(paper.categories)}")
        
        # 搜索计算物理论文
        physics_papers = await client.search_by_category(["physics.comp-ph"], max_results=2)
        print(f"\n计算物理论文 - 找到 {len(physics_papers)} 篇:")
        
        for i, paper in enumerate(physics_papers, 1):
            print(f"  {i}. {paper.title}")
            print(f"     分类: {', '.join(paper.categories)}")

async def interdisciplinary_example():
    """跨学科搜索示例"""
    print("\n=== 跨学科搜索示例 ===")
    
    async with ArxivClient() as client:
        # 搜索AI在生物学中的应用
        bio_ai_papers = await client.search_by_category([
            "cs.AI",      # 人工智能
            "cs.LG",      # 机器学习
            "q-bio.QM",   # 定量生物学方法
            "q-bio.GN"    # 基因组学
        ], max_results=3)
        
        print(f"AI + 生物学交叉领域论文 - 找到 {len(bio_ai_papers)} 篇:")
        for i, paper in enumerate(bio_ai_papers, 1):
            print(f"  {i}. {paper.title}")
            print(f"     分类: {', '.join(paper.categories)}")

async def explore_categories_example():
    """探索分类示例"""
    print("\n=== 探索分类示例 ===")
    
    from arxiv_search import CATEGORY_GROUPS
    
    print("支持的学科分类组:")
    for group_name, categories in CATEGORY_GROUPS.items():
        print(f"  {group_name}: {len(categories)} 个分类")
        # 显示前几个分类作为示例
        for cat in categories[:3]:
            description = ARXIV_CATEGORIES[cat]
            print(f"    {cat} - {description}")
        if len(categories) > 3:
            print(f"    ... 还有 {len(categories) - 3} 个分类")

async def main():
    """主函数"""
    await popular_categories_example()
    await search_by_keyword_example()
    await math_physics_example()
    await interdisciplinary_example()
    await explore_categories_example()

if __name__ == "__main__":
    asyncio.run(main())

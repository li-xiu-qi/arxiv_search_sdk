"""
基本使用示例
"""
import asyncio
from arxiv_search import ArxivClient

async def basic_search_example():
    """基本搜索示例"""
    print("=== 基本搜索示例 ===")
    
    async with ArxivClient() as client:
        # 搜索机器学习相关论文
        papers = await client.search_ml_papers(max_results=5)
        
        print(f"找到 {len(papers)} 篇机器学习论文:")
        for i, paper in enumerate(papers, 1):
            print(f"\n{i}. {paper.title}")
            print(f"   作者: {', '.join(paper.authors[:3])}{'...' if len(paper.authors) > 3 else ''}")
            print(f"   分类: {', '.join(paper.categories)}")
            print(f"   发表时间: {paper.published.strftime('%Y-%m-%d')}")
            print(f"   ArXiv ID: {paper.arxiv_id}")

async def search_by_title_example():
    """按标题搜索示例"""
    print("\n=== 按标题搜索示例 ===")
    
    async with ArxivClient() as client:
        # 搜索标题包含"transformer"的论文
        papers = await client.search_by_title(["transformer"], max_results=3)
        
        print(f"找到 {len(papers)} 篇标题包含'transformer'的论文:")
        for i, paper in enumerate(papers, 1):
            print(f"\n{i}. {paper.title}")
            print(f"   ArXiv ID: {paper.arxiv_id}")

async def search_by_author_example():
    """按作者搜索示例"""
    print("\n=== 按作者搜索示例 ===")
    
    async with ArxivClient() as client:
        # 搜索作者包含"Geoffrey Hinton"的论文
        papers = await client.search_by_author(["Geoffrey Hinton"], max_results=3)
        
        print(f"找到 {len(papers)} 篇Geoffrey Hinton的论文:")
        for i, paper in enumerate(papers, 1):
            print(f"\n{i}. {paper.title}")
            print(f"   作者: {', '.join(paper.authors)}")
            print(f"   发表时间: {paper.published.strftime('%Y-%m-%d')}")

async def search_by_category_example():
    """按分类搜索示例"""
    print("\n=== 按分类搜索示例 ===")
    
    async with ArxivClient() as client:
        # 搜索人工智能论文
        ai_papers = await client.search_ai_papers(max_results=3)
        
        print(f"找到 {len(ai_papers)} 篇人工智能论文:")
        for i, paper in enumerate(ai_papers, 1):
            print(f"\n{i}. {paper.title}")
            print(f"   分类: {', '.join(paper.categories)}")

async def main():
    """主函数"""
    await basic_search_example()
    await search_by_title_example()
    await search_by_author_example()
    await search_by_category_example()

if __name__ == "__main__":
    asyncio.run(main())

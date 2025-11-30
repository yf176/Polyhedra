"""Polyhedra Feature Demo - Search Transformer Papers"""

import asyncio
from pathlib import Path
from polyhedra.services.semantic_scholar import SemanticScholarService


async def demo_search():
    """Demonstrate search functionality"""
    print("\n" + "="*80)
    print("🎓 Polyhedra Paper Search Demo")
    print("="*80 + "\n")
    
    # Initialize service
    service = SemanticScholarService()
    
    # Search for transformer papers
    query = "transformer architecture"
    print(f"🔍 Search topic: {query}")
    print(f"📅 Year range: 2017-2024")
    print(f"📊 Result limit: 10 papers\n")
    
    papers = await service.search(
        query=query,
        limit=10,
        year_start=2017,
        year_end=2024
    )
    
    print(f"✅ Found {len(papers)} papers:\n")
    print("-"*80 + "\n")
    
    for i, paper in enumerate(papers, 1):
        print(f"📄 [{i}] {paper['title']}")
        
        # Authors
        authors = paper.get('authors', [])
        if authors:
            author_str = ', '.join(authors[:3])
            if len(authors) > 3:
                author_str += f" et al. ({len(authors)} total)"
            print(f"    👥 Authors: {author_str}")
        
        # Year and citation count
        print(f"    📅 Year: {paper.get('year', 'N/A')}")
        print(f"    📊 Citations: {paper.get('citationCount', 0):,}")
        
        # Paper ID
        if paper.get('paperId'):
            print(f"    🔗 ID: {paper['paperId']}")
        
        # Abstract (truncated)
        if paper.get('abstract'):
            abstract = paper['abstract']
            if len(abstract) > 150:
                abstract = abstract[:150] + "..."
            print(f"    📝 Abstract: {abstract}")
        
        print()
        print("-"*80 + "\n")
    
    print("\n✨ Demo complete!\n")
    print("💡 Tip: This is the capability Polyhedra provides to AI assistants via MCP tools")
    print("   When properly configured, you can simply say in chat:")
    print('   "Search for transformer papers" → AI will automatically call these features\n')


if __name__ == "__main__":
    asyncio.run(demo_search())

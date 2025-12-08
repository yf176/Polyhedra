"""Literature Review Service for generating structured academic literature reviews."""

import json
import logging
import re
from typing import Literal, Optional

from polyhedra.services.llm_service import LLMService

logger = logging.getLogger(__name__)


class LiteratureReviewService:
    """Service for generating structured literature reviews from academic papers."""
    
    # Depth configurations (word counts)
    DEPTH_CONFIG = {
        "brief": {"min": 500, "max": 800, "target": 650},
        "standard": {"min": 1500, "max": 2500, "target": 2000},
        "comprehensive": {"min": 2000, "max": 3000, "target": 2500},
    }
    
    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
        provider: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize literature review service.
        
        Args:
            llm_service: Existing LLMService instance (preferred)
            provider: LLM provider if creating new service
            api_key: API key if creating new service
        """
        if llm_service:
            self.llm = llm_service
        else:
            self.llm = LLMService(provider=provider, api_key=api_key)
        
        logger.info("Literature review service initialized")
    
    def _prepare_papers_summary(self, papers: list[dict]) -> str:
        """
        Prepare concise summary of papers for prompt.
        
        Args:
            papers: List of paper dictionaries
            
        Returns:
            Formatted JSON string with paper summaries
        """
        summaries = []
        for i, paper in enumerate(papers, 1):
            summary = {
                "index": i,
                "title": paper.get("title", "Unknown"),
                "authors": self._format_authors(paper.get("authors", [])),
                "year": paper.get("year"),
                "venue": paper.get("venue", "Unknown venue"),
                "abstract": paper.get("abstract", "No abstract available"),
                "citations": paper.get("citationCount", 0),
                "fields": paper.get("fieldsOfStudy", []),
            }
            summaries.append(summary)
        
        return json.dumps(summaries, indent=2)
    
    def _format_authors(self, authors: list) -> str:
        """Format author list for citation."""
        if not authors:
            return "Unknown"
        
        if isinstance(authors[0], dict):
            author_names = [a.get("name", "Unknown") for a in authors]
        else:
            author_names = authors
        
        if len(author_names) == 1:
            return author_names[0]
        elif len(author_names) == 2:
            return f"{author_names[0]} and {author_names[1]}"
        else:
            first_author = author_names[0].split()[-1]  # Last name
            return f"{first_author} et al."
    
    def _build_prompt(
        self,
        papers: list[dict],
        focus: Optional[str],
        structure: str,
        depth: str,
        include_gaps: bool
    ) -> str:
        """
        Build prompt for literature review generation.
        
        Args:
            papers: List of paper dictionaries
            focus: Optional focus area
            structure: Review structure type
            depth: Depth level
            include_gaps: Whether to identify gaps
            
        Returns:
            Formatted prompt string
        """
        papers_json = self._prepare_papers_summary(papers)
        depth_config = self.DEPTH_CONFIG[depth]
        target_words = depth_config["target"]
        
        topic = focus or "the research area covered by these papers"
        
        prompt = f"""You are an expert academic researcher tasked with writing a structured literature review.

INPUT:
{len(papers)} academic papers on the topic: "{topic}"

PAPERS DATA:
{papers_json}

TASK:
Write a comprehensive literature review with approximately {target_words} words using the following structure:

1. **Overview** (1-2 paragraphs, ~150 words)
   - Summarize the research area and its significance
   - State the scope of this review
   - Preview the main findings and themes

2. **Taxonomy of Approaches** (main section, ~{int(target_words * 0.5)} words)
   - Organize papers into 3-5 thematic categories based on their methodology or focus
   - For each category:
     * Define the approach clearly
     * Discuss 3-5 key papers with proper citations [Author et al., Year]
     * Compare and contrast methods within the category
     * Note trends and recent developments

3. **Critical Analysis** (~{int(target_words * 0.25)} words)
   - Analyze strengths and limitations of different approaches
   - Identify patterns across categories
   - Discuss trade-offs between different methods
   - Highlight breakthrough innovations or paradigm shifts

"""
        
        if include_gaps:
            prompt += f"""4. **Research Gaps** (~{int(target_words * 0.15)} words)
   - Identify 3-5 underexplored areas or open problems
   - For each gap:
     * Clearly state the gap
     * Explain why it matters
     * Suggest potential research directions

"""
        
        prompt += f"""{"5" if include_gaps else "4"}. **Conclusion** (1 paragraph, ~100 words)
   - Synthesize key insights
   - State the current state of the field
   - Provide forward-looking perspective

CITATION FORMAT:
- Use format: [Author et al., Year] for in-text citations
- Example: "Vision Transformers [Dosovitskiy et al., 2021] introduced..."
- Cite papers by referring to their authors and year from the PAPERS DATA above
- Aim to cite at least 80% of the provided papers

STRUCTURE: {structure.capitalize()}
{"- Organize by themes and methodologies" if structure == "thematic" else ""}
{"- Organize by publication timeline and evolution" if structure == "chronological" else ""}
{"- Organize by research methods and techniques" if structure == "methodological" else ""}

QUALITY REQUIREMENTS:
- Academic tone and formal language
- Balanced coverage across papers
- Critical thinking and synthesis (not just summarization)
- Proper attribution for all claims
- Coherent narrative flow between sections
- No hallucinated papers or citations

Generate the literature review now:"""
        
        return prompt
    
    def _extract_metadata(
        self,
        review_text: str,
        papers: list[dict],
        include_gaps: bool
    ) -> dict:
        """
        Extract metadata from generated review.
        
        Args:
            review_text: Generated review text
            papers: Original paper list
            include_gaps: Whether gaps were requested
            
        Returns:
            Metadata dictionary
        """
        # Count words
        word_count = len(review_text.split())
        
        # Extract sections (headers starting with ##)
        sections = re.findall(r'^#+\s+(.+)$', review_text, re.MULTILINE)
        
        # Extract research gaps if present
        research_gaps = []
        if include_gaps and ("Research Gaps" in review_text or "research gaps" in review_text.lower()):
            # Try to extract gap bullet points or numbered lists
            gaps_section = re.search(
                r'##\s*Research\s+Gaps[^\n]*\n(.+)(?:\n##|\Z)',
                review_text,
                re.DOTALL | re.IGNORECASE
            )
            if gaps_section:
                gap_text = gaps_section.group(1)
                # Extract bullet points with bold titles
                gap_items = re.findall(r'[-*]\s+\*\*([^*]+)\*\*[:\s]*([^\n-*]+)', gap_text)
                for title, description in gap_items[:5]:  # Max 5 gaps
                    research_gaps.append({
                        "title": title.strip(),
                        "description": description.strip()[:200]  # Limit description
                    })
        
        # Count citations (rough estimate) - match both formats
        citations = re.findall(r'\[([A-Z][a-z]+(?:\s+et\s+al\.)?(?:\s+and\s+[A-Z][a-z]+)?),?\s*(\d{4})\]', review_text)
        cited_count = len(set(citations))  # Unique citations
        
        return {
            "paper_count": len(papers),
            "word_count": word_count,
            "sections": sections,
            "research_gaps": research_gaps,
            "citations_found": cited_count,
            "citation_coverage": round(cited_count / len(papers) * 100, 1) if papers else 0
        }
    
    async def generate_review(
        self,
        papers: list[dict],
        focus: Optional[str] = None,
        structure: Literal["thematic", "chronological", "methodological"] = "thematic",
        depth: Literal["brief", "standard", "comprehensive"] = "standard",
        include_gaps: bool = True,
        model: Optional[str] = None
    ) -> dict:
        """
        Generate structured literature review from papers.
        
        Args:
            papers: List of paper dictionaries (from Semantic Scholar API)
            focus: Optional focus area (e.g., "sparse attention mechanisms")
            structure: Organization structure ("thematic", "chronological", "methodological")
            depth: Review depth ("brief", "standard", "comprehensive")
            include_gaps: Whether to identify research gaps
            model: Optional LLM model override
            
        Returns:
            Dictionary with:
                - review: Generated review text (markdown)
                - metadata: Statistics and extracted information
                - cost: Token usage and USD cost
                
        Raises:
            ValueError: If parameters are invalid
            RuntimeError: If LLM service is not configured
        """
        # Validate inputs
        if not papers:
            raise ValueError("Papers list cannot be empty")
        
        if depth not in self.DEPTH_CONFIG:
            raise ValueError(f"Depth must be one of: {list(self.DEPTH_CONFIG.keys())}")
        
        if structure not in ["thematic", "chronological", "methodological"]:
            raise ValueError("Structure must be 'thematic', 'chronological', or 'methodological'")
        
        if not self.llm.is_configured:
            raise RuntimeError(
                "LLM service is not configured. Set ANTHROPIC_API_KEY or OPENAI_API_KEY."
            )
        
        logger.info(
            f"Generating {depth} literature review for {len(papers)} papers "
            f"(structure={structure}, gaps={include_gaps})"
        )
        
        # Build prompt
        prompt = self._build_prompt(papers, focus, structure, depth, include_gaps)
        
        # Estimate cost before generation
        estimated_input_tokens = self.llm.estimate_tokens(prompt)
        estimated_output_tokens = self.DEPTH_CONFIG[depth]["target"]  # Rough estimate
        estimated_cost = self.llm.calculate_cost(
            estimated_input_tokens,
            estimated_output_tokens,
            model
        )
        
        logger.info(
            f"Estimated cost: ${estimated_cost:.4f} "
            f"({estimated_input_tokens} + {estimated_output_tokens} tokens)"
        )
        
        # Generate review
        result = await self.llm.complete(prompt, model)
        
        if result is None:
            raise RuntimeError("LLM service returned no result")
        
        review_text, input_tokens, output_tokens = result
        
        # Calculate actual cost
        actual_cost = self.llm.calculate_cost(input_tokens, output_tokens, model)
        
        # Extract metadata
        metadata = self._extract_metadata(review_text, papers, include_gaps)
        
        logger.info(
            f"Generated review: {metadata['word_count']} words, "
            f"{metadata['citations_found']} citations, "
            f"cost: ${actual_cost:.4f}"
        )
        
        return {
            "review": review_text,
            "metadata": metadata,
            "cost": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
                "total_usd": actual_cost
            }
        }
    
    def estimate_cost(
        self,
        paper_count: int,
        depth: Literal["brief", "standard", "comprehensive"] = "standard",
        model: Optional[str] = None
    ) -> dict:
        """
        Estimate cost for generating a review.
        
        Args:
            paper_count: Number of papers to review
            depth: Review depth level
            model: Optional model override
            
        Returns:
            Dictionary with cost estimate
        """
        # Rough estimates
        chars_per_paper = 1000  # Average abstract + metadata
        estimated_input_chars = paper_count * chars_per_paper + 2000  # + prompt overhead
        estimated_input_tokens = estimated_input_chars // 4
        
        estimated_output_tokens = self.DEPTH_CONFIG[depth]["target"]
        
        estimated_cost = self.llm.calculate_cost(
            estimated_input_tokens,
            estimated_output_tokens,
            model
        )
        
        return {
            "estimated_input_tokens": estimated_input_tokens,
            "estimated_output_tokens": estimated_output_tokens,
            "estimated_total_tokens": estimated_input_tokens + estimated_output_tokens,
            "estimated_usd": estimated_cost,
            "paper_count": paper_count,
            "depth": depth
        }
    
    async def close(self) -> None:
        """Close service and cleanup resources."""
        await self.llm.close()

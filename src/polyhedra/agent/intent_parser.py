"""Parse natural language commands into structured intents."""

import re
import logging
from typing import Optional, Dict, Any
from polyhedra.services.llm_service import LLMService
from polyhedra.agent.models import Intent, IntentType


class IntentParser:
    """
    Parse natural language commands into structured intents.
    
    Uses a combination of:
    1. Pattern matching for common commands
    2. LLM-based parsing for complex/ambiguous commands
    """
    
    def __init__(self, llm_service: Optional[LLMService] = None):
        """
        Initialize intent parser.
        
        Args:
            llm_service: Optional LLM service for complex parsing
        """
        self.llm_service = llm_service
        self.logger = logging.getLogger(__name__)
        
        # Command patterns
        self.patterns = {
            IntentType.RESEARCH_SURVEY: [
                r"(?:research|survey|review)\s+(?:papers?\s+)?(?:on|about)?\s*(.+)",
                r"find\s+(?:papers?\s+)?(?:on|about)\s+(.+)",
                r"(?:what|show me)\s+(?:papers?\s+)?(?:on|about)\s+(.+)",
            ],
            IntentType.PAPER_COMPARISON: [
                r"compare\s+(.+?)\s+(?:vs|versus|and)\s+(.+)",
                r"(?:what|how)\s+(?:is|are)\s+(?:the\s+)?(?:difference|differences)\s+between\s+(.+?)\s+and\s+(.+)",
            ],
            IntentType.GAP_ANALYSIS: [
                r"(?:find|identify|analyze)\s+(?:research\s+)?gaps?\s+in\s+(.+)",
                r"what(?:'\''s|\s+is)\s+missing\s+in\s+(.+)",
            ],
            IntentType.CITATION_FINDING: [
                r"(?:find|get)\s+citations?\s+for\s+(.+)",
                r"cite\s+(.+)",
            ],
        }
    
    async def parse(self, command: str) -> Intent:
        """
        Parse command into intent.
        
        Args:
            command: Natural language command
            
        Returns:
            Parsed Intent object
        """
        command = command.strip()
        
        # Try pattern matching first (fast)
        intent = self._pattern_match(command)
        
        if intent.type != IntentType.UNKNOWN or not self.llm_service:
            return intent
        
        # Fall back to LLM parsing for complex commands
        try:
            intent = await self._llm_parse(command)
        except Exception as e:
            self.logger.warning(f"LLM parsing failed: {e}")
        
        return intent
    
    def _pattern_match(self, command: str) -> Intent:
        """
        Match command against patterns.
        
        Args:
            command: Command text
            
        Returns:
            Intent (may be UNKNOWN)
        """
        command_lower = command.lower()
        
        for intent_type, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.match(pattern, command_lower, re.IGNORECASE)
                if match:
                    # Extract topic and parameters
                    topic = match.group(1).strip()
                    params = self._extract_parameters(command_lower)
                    
                    return Intent(
                        type=intent_type,
                        topic=topic,
                        parameters=params,
                        confidence=0.9,
                        raw_command=command
                    )
        
        # No match
        return Intent(
            type=IntentType.UNKNOWN,
            topic="",
            parameters={},
            confidence=0.0,
            raw_command=command
        )
    
    def _extract_parameters(self, command: str) -> Dict[str, Any]:
        """
        Extract additional parameters from command.
        
        Args:
            command: Command text
            
        Returns:
            Dictionary of parameters
        """
        params = {}
        
        # Extract paper limit
        limit_match = re.search(r'(\d+)\s+papers?', command)
        if limit_match:
            params['limit'] = int(limit_match.group(1))
        
        # Extract depth
        if any(word in command for word in ['brief', 'quick', 'short']):
            params['depth'] = 'brief'
        elif any(word in command for word in ['comprehensive', 'detailed', 'thorough']):
            params['depth'] = 'comprehensive'
        else:
            params['depth'] = 'standard'
        
        # Extract structure
        if 'chronological' in command or 'timeline' in command:
            params['structure'] = 'chronological'
        elif 'methodological' in command or 'methods' in command:
            params['structure'] = 'methodological'
        else:
            params['structure'] = 'thematic'
        
        # Extract year range
        year_match = re.search(r'(?:from|since|after)\s+(\d{4})', command)
        if year_match:
            params['year_from'] = int(year_match.group(1))
        
        year_match = re.search(r'(?:to|until|before)\s+(\d{4})', command)
        if year_match:
            params['year_to'] = int(year_match.group(1))
        
        return params
    
    async def _llm_parse(self, command: str) -> Intent:
        """
        Use LLM to parse complex command.
        
        Args:
            command: Command text
            
        Returns:
            Parsed Intent
        """
        prompt = f"""Parse this research command into structured intent.

Command: "{command}"

Extract:
1. Intent type (research_survey, paper_comparison, gap_analysis, citation_finding, or unknown)
2. Main research topic
3. Parameters: limit (number), depth (brief/standard/comprehensive), structure (thematic/chronological/methodological), year_from, year_to

Respond in JSON format:
{{
  "type": "research_survey",
  "topic": "extracted topic",
  "parameters": {{"limit": 50, "depth": "standard"}}
}}"""

        response, _, _ = await self.llm_service.complete(prompt, model=None)
        
        # Parse JSON response
        import json
        try:
            data = json.loads(response.strip())
            return Intent(
                type=IntentType(data['type']),
                topic=data['topic'],
                parameters=data.get('parameters', {}),
                confidence=0.8,
                raw_command=command
            )
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            self.logger.error(f"Failed to parse LLM response: {e}")
            return Intent(
                type=IntentType.UNKNOWN,
                topic="",
                parameters={},
                confidence=0.0,
                raw_command=command
            )

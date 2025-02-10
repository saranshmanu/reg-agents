from .base import BaseClient

class RegulationAgent(BaseClient):
    """
    Specialized agent for handling regulation-related queries
    Provides detailed analysis of regulatory questions and compliance matters
    """
    
    def analyze_regulation(self, question: str) -> str:
        """
        Analyzes regulation-specific questions
        Args:
            question: User's regulation-related query
        Returns:
            Detailed analysis focused on regulatory aspects
        """
        prompt = """
        You are a regulations expert. Please analyze this regulation-related question:
        {question}
        
        Provide a detailed analysis focused on regulatory aspects:
        1. Relevant regulations
        2. Compliance requirements
        3. Key considerations
        """
        return self.invoke(prompt.format(question=question))

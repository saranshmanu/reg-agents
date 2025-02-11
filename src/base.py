import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


class BaseClient:
    """
    Base client for all agents
    Handles OpenAI API initialization and common interaction patterns
    """
    
    def __init__(self):
        """
        Initialize OpenAI client with configuration from environment variables
        - OPENAI_MODEL: Model to be used (default: gpt-4o-mini)
        - OPENAI_MAX_TOKENS: Maximum tokens for response (default: 1500)
        - OPENAI_API_KEY: API key for authentication
        """
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", 1500))
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def invoke(self, prompt: str, max_tokens = 0) -> str:
        """
        Invokes OpenAI API with the given prompt
        Args:
            prompt: Input prompt for the model
            max_tokens: Maximum tokens for response (0 uses default)
        Returns:
            Generated response from the model
        """
        max_tokens = self.max_tokens if max_tokens == 0 else max_tokens
        response = self.client.chat.completions.create(
            model=self.model, 
            messages=[{"role": "user", "content": prompt}], 
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

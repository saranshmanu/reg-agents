from typing import Dict
from .base import BaseClient

class RouterAgent(BaseClient):
    def classify_question(self, question: str) -> Dict:
        prompt = """Classify the question into one of these categories:
        REGULATION_QUESTION - Questions about regulations
        OTHER - Any other type of question
        
        Question: {question}
        Format: Please only return "TYPE" (e.g., "REGULATION_QUESTION" or "OTHER")
        """
        response = self.invoke(prompt.format(question=question))
        qtype = response.strip()

        return {
            "type": qtype
        }

from typing import Dict
from ..base import BaseClient

class RouterAgent(BaseClient):
    def classify_question(self, question: str) -> Dict:
        prompt = """Classify the question into one of these categories:

        REGULATION_QUESTION - Questions that involve:
        - Regulatory compliance requirements
        - Legal obligations and standards
        - Industry-specific regulations
        - Regulatory bodies and their guidelines
        - Compliance procedures and documentation
        - Regulatory updates and changes
        Examples:
        - "What are the compliance requirements for financial institutions?"
        - "How does GDPR affect data handling?"
        - "What are the regulatory reporting deadlines?"

        OTHER - Questions that are:
        - General inquiries not related to regulations
        - Technical or operational questions
        - Business strategy questions
        Examples:
        - "How to improve business efficiency?"
        - "What are the current market trends?"
        - "How to handle customer complaints?"

        Question: {question}
        Format: Return only "REGULATION_QUESTION" or "OTHER"
        """
        response = self.invoke(prompt.format(question=question))
        qtype = response.strip()

        return {
            "type": qtype
        }

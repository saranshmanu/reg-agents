from ..base import BaseClient

class GeneralAgent(BaseClient):
    def answer(self, question: str) -> str:
        prompt = """
        You are a regulations assistant. Please answer this question:
        {question}
        
        Provide a clear and concise response.
        """

        return self.invoke(prompt.format(question=question))

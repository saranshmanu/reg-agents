from ..base import BaseClient

ACTOR_IDENTIFICATION_PROMPT = '''You are an expert AI agent specialized in analysing legal regulations.

Key Definitions:
Act: Describes what an agent can do, the conditions under which the act is valid, and the results of the act. Only by acting can you change something.
Action: Action that causes the transition of an object
Actor: Agent role that is allowed to perform the action

Task:
Find the 'Actor' from the context with clear distinction between other definitions.
Note: An 'Act' can never be an 'Actor' and an 'Action' can never be an 'Actor'.

Regulation to analyze:
{text}

Rules:
1. If an actor is present, return exactly "Yes"
2. If no actor is found, return exactly "This is not a valid regulation"
3. Must only return one of these two responses'''


class ActorIdentificationAgent(BaseClient):
    def identify(self, text: str) -> str:
        # return "This is not a valid regulation"
        return self.invoke(ACTOR_IDENTIFICATION_PROMPT.format(text=text))

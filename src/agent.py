import json
from abc import ABC, abstractmethod
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from pydantic import BaseModel

from llm_client import GeminiClient


@dataclass
class Context:
    user_input: str
    knowledge: list[str]
    answer: str


class ActionResponse(BaseModel):
    thinking_process: str
    action: str
    action_input: str
    reason: str


class Action(ABC):
    @abstractmethod
    def description(self) -> str:
        pass

    def name(self) -> str:
        return type(self).__name__[:-6].lower()

    def execute(self, context: Context, input: str) -> ActionResponse | None:
        """
        Execute the action and return the next action to take.

        Return `None` if this should be the last action.
        """
        pass


class Agent:
    def __init__(self, actions: list[Action], llm_client: GeminiClient):
        self.context = Context(user_input="", knowledge=[], answer="")
        self.actions = {action.name(): action for action in actions}
        self.llm_client = llm_client

    def execute(self, user_input: str) -> str:
        self.context.user_input = user_input

        next_action: str = "decide"
        next_action_input: str = ""
        while next_action:
            print("---")
            action_response = self.actions[next_action].execute(
                self.context,
                next_action_input,
            )
            if action_response is None:
                return ""

            next_action = action_response.action
            next_action_input = action_response.action_input

        return self.context.answer


class DecideAction(Action):
    def __init__(self, llm_client: GeminiClient, actions: list[Action]):
        self.llm_client = llm_client
        self.actions = {action.name(): action for action in actions}

    def description(self) -> str:
        return f"""
        {self.name()}
        - description: decide on the next action to answer the user's input.
        - No input required.
        """.strip()

    def execute(self, context: Context, input: str) -> ActionResponse | None:
        if input:
            raise ValueError("Decide action does not take input")

        actions = "\n".join(
            f"[{i}] {action.description()}"
            for i, action in enumerate(self.actions.values())
        )

        schema = json.dumps(ActionResponse.model_json_schema(), indent=2)

        prompt = f"""
You are a principal researcher with the ability to perform actions to answer the following question:
Question: {context.user_input}
Previous Research: {context.knowledge}

# Available Actions
{actions}

# Instructions
Decide the next action based on the context and available actions.
Return your response in json format following this schema:
{schema}
        """.strip()

        raw_response = self.llm_client.execute(
            prompt=prompt,
            response_schema=ActionResponse,
        )

        if raw_response is None:
            raise ValueError("No response from LLM")

        response = ActionResponse.model_validate_json(raw_response)
        print(f"DecideAction: {response=}")
        return response


class DdgSearchResult(BaseModel):
    title: str
    href: str
    body: str


class SearchAction(Action):
    def __init__(self):
        self.ddg_client = DDGS()

    def description(self) -> str:
        return f"""
        {self.name()}
        - description: search the web for additional information
        - input (str): The query to search for.
        """.strip()

    def execute(self, context: Context, input: str) -> ActionResponse | None:
        if not input:
            raise ValueError("No input provided for search action")

        results = self.ddg_client.text(input, max_results=1)
        for entry in results:
            result = DdgSearchResult.model_validate(entry)
            knowledge = f"{result.title}\n{result.href}\n{result.body}"
            print(f"SearchAction: {knowledge=}")
            context.knowledge.append(knowledge)

        return ActionResponse(
            thinking_process="",
            action="decide",
            action_input="",
            reason="",
        )


class DeepSearchAction(Action):
    def description(self) -> str:
        return f"""
        {self.name()}
        - description: visit a given website and extract information from it. This is useful when the search action does not provide enough information.
        - input (str): The URL of the website to visit.
        """.strip()

    def execute(self, context: Context, input: str) -> ActionResponse | None:
        if not input:
            raise ValueError("No input provided for deep search action")

        response = requests.get(input)
        if response.status_code != 200:
            raise ValueError(f"Failed to retrieve the website: {input}")

        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        print(f"DeepSearchAction: {text=}")

        context.knowledge.append(text)

        return ActionResponse(
            thinking_process="",
            action="decide",
            action_input="",
            reason="",
        )


class AnswerAction(Action):
    def __init__(self, llm_client: GeminiClient):
        self.llm_client = llm_client

    def description(self) -> str:
        return f"""
        {self.name()}
        - description: answer the user's input based on the current knowledge.
        - input (str): The answer.
        """.strip()

    def execute(self, context: Context, input: str) -> ActionResponse | None:
        if not input:
            raise ValueError("No input provided for answer action")

        print(f"AnswerAction: {input=}")
        context.answer = input
        return None

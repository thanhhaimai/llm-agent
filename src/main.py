import os

import click

from agent import Agent, AnswerAction, DecideAction, SearchAction
from llm_client import GeminiClient


@click.command()
@click.argument("user_input")
def main(user_input):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    print(f"User input: {user_input}")
    llm_client = GeminiClient(api_key=api_key)

    search_action = SearchAction()
    answer_action = AnswerAction(llm_client=llm_client)
    decide_action = DecideAction(
        llm_client=llm_client,
        actions=[search_action, answer_action],
    )
    agent = Agent(
        llm_client=llm_client,
        actions=[search_action, answer_action, decide_action],
    )

    print(agent.execute(user_input))


if __name__ == "__main__":
    main()

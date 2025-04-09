import json
from typing import Optional
import typer
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.storage.agent.sqlite import SqliteAgentStorage
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print

console = Console()

def create_chat_agent(user: str = "user"):
    session_id: Optional[str] = None

    # Ask if user wants to start new session or continue existing one
    new = False

    # Get existing session if user doesn't want a new one
    agent_storage = SqliteAgentStorage(
        table_name="agent_sessions", db_file="tmp/agents.db"
    )

    if not new:
        existing_sessions = agent_storage.get_all_session_ids(user)
        if len(existing_sessions) > 0:
            session_id = existing_sessions[0]

    agent = Agent(
        user_id=user,
        # Set the session_id on the agent to resume the conversation
        session_id=session_id,
        model=Ollama(id="llama3.2"),
        storage=agent_storage,
        tools=[GoogleSearchTools(fixed_max_results=100000), DuckDuckGoTools(fixed_max_results=100000)],
        # Add chat history to messages
        add_history_to_messages=True,
        num_history_responses=5,
        markdown=True,
        description="You have to help the user for movies recommendation.",
        instructions=[
            "You are a chat agent. Initially you will be given some information about the user like user's profile, preferred genres, and user's history.",
            "You will use the tools provided to you to search for information.",
            "You have to provide the user with recommendations based on the user's profile and history.",
            "You have to ask the user for more information if you need it.",
            "You have to provide the user with the best possible answer.",
            "If user is asking for latest movies (beyond your knowledge cutoff i.e. Dec 2023), then use web search to fetch the latest movies.",
        ],
    )

    if session_id is None:
        session_id = agent.session_id
        if session_id is not None:
            print(f"Started Session: {session_id}\n")
        else:
            print("Started Session\n")
    else:
        print(f"Continuing Session: {session_id}\n")

    return agent


def create_prompt_generator_agent(user: str = "user"):
    session_id: Optional[str] = None

    # Ask if user wants to start new session or continue existing one
    new = False

    # Get existing session if user doesn't want a new one
    agent_storage = SqliteAgentStorage(
        table_name="agent_sessions", db_file="tmp/agents.db"
    )

    if not new:
        existing_sessions = agent_storage.get_all_session_ids(user)
        if len(existing_sessions) > 0:
            session_id = existing_sessions[0]

    agent = Agent(
        user_id=user,
        # Set the session_id on the agent to resume the conversation
        session_id=session_id,
        model=Ollama(id="llama3.2"),
        storage=agent_storage,
        # Add chat history to messages
        add_history_to_messages=True,
        num_history_responses=5,
        markdown=False,
        description="You have to collect the user's requirement for product recommendation and generate a prompt for web search agent.",
        instructions=[
            "You don't have to ask any questions to the user or provide any recommendations.",
            "You have to fetch necessary information from the user's query and previous conversation history to understand the user's requirement.",
            "You have to generate a prompt (Simplest possible form) for the web search agent to fetch the product recommendations.",
            "Output should only contain the prompt for the web search agent in one line.",
        ],
    )

    return agent


def print_messages(agent):
    """Print the current chat history in a formatted panel"""
    console.print(
        Panel(
            JSON(
                json.dumps(
                    [
                        m.model_dump(include={"role", "content"})
                        for m in agent.memory.messages
                    ]
                ),
                indent=4,
            ),
            title=f"Chat History for session_id: {agent.session_id}",
            expand=True,
        )
    )


def main(user: str = "user"):
    agent = create_chat_agent(user)

    print("Chat with an Ollama agent!")
    exit_on = ["exit", "quit", "bye"]
    while True:
        message = Prompt.ask(f"[bold] :sunglasses: {user} [/bold]")
        if message in exit_on:
            break

        agent.print_response(message=message, stream=True, markdown=True)
        print_messages(agent)


if __name__ == "__main__":
    typer.run(main)
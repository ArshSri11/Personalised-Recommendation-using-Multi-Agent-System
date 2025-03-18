import json
from typing import Optional
import typer
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.storage.agent.sqlite import SqliteAgentStorage
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print

console = Console()

def create_agent(user: str = "user"):
    session_id: Optional[str] = None

    # Ask if user wants to start new session or continue existing one
    new = typer.confirm("Do you want to start a new session?")

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
        num_history_responses=3,
        markdown=True,
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
    agent = create_agent(user)

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
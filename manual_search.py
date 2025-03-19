from agno.agent import Agent
from agno.tools.website import WebsiteTools
from agno.models.ollama import Ollama

agent = Agent(
    model=Ollama(id="llama3.2"),
    tools=[WebsiteTools()], show_tool_calls=True)
agent.print_response(
    "Search web page and give recommendations for Mobile phones: 'https://www.amazon.in/'", markdown=True
)
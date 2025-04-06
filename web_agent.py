from agno.agent import Agent
from agno.tools.googlesearch import GoogleSearchTools
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools
from pydantic import BaseModel, Field

class Product(BaseModel):
    title: str = Field(..., title="Title")
    description: str = Field(..., title="Description")
    url: str = Field(..., title="URL")

class WebSearchResults(BaseModel):
    products: list[str]

Web_Agent = Agent(
    model=Ollama(id = "llama3.2"),
    tools=[GoogleSearchTools(fixed_max_results=100000), DuckDuckGoTools(fixed_max_results=100000)],
    show_tool_calls=True,
    description="You are an web search agent to help find information on the web.",
    response_model=WebSearchResults,
    instructions=[
        "You are a web search agent. You will be given a query and you need to search for information related to that query.",
        "You will use the tools provided to you to search for information.",
        # "You will return the results in a simplified text format.",
    ],
    structured_outputs=False,
    markdown=True,
    stream=True,
)

Summerizer = Agent(
    model=Ollama(id = "llama3.2"),
    description="You are a summerizer agent to help summerize the information from web agent.",
    response_model=WebSearchResults,
    instructions=[
        "You will be given results from the web agent which contains information related to a movie.",
        "You need to summerize the information in a simplified text format.",
        "You will only return the results in a single text format."
    ],
    structured_outputs=False,
    markdown=True,
    stream=True,
)

# response = web_agent.run("Cup")
# print(response.content)
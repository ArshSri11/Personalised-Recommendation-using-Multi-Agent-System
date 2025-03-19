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
    description="You are an web search agent to help user for product recommendation.",
    response_model=WebSearchResults,
    instructions=[
        "You will be provides with an query from user about which type of product he/she wants to buy.",
        "Carefully read the query and provide the user with the top 5 products (latest trending and most relevant) that match the query.",
        "Make sure to provide the product name, description and URL of the product.",
        "Give it as a list of products.",
    ],
    structured_outputs=False,
    markdown=True,
    stream=True,
)

# response = web_agent.run("Cup")
# print(response.content)
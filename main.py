from agno.workflow import Workflow
from agno.agent import Agent, RunResponse
from agno.tools.googlesearch import GoogleSearchTools
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools
from pydantic import BaseModel

class WebSearchResults(BaseModel):
    products: list[str]

class SearchWorkflow(Workflow):
    
    # Define chat agent
    chat_agent: Agent = Agent(
        model=Ollama(id="llama3.2"),
        markdown=False,
        description="You have to help the user for product recommendation.",
        instructions=[
            "You will be provided with a 5 product recommendations based from web search agent.",
            "You have to present these recommendations to the user along with URL in a friendly manner.",
            "Summarize the recommendations from the web search agent and communicate them to the user.",
            "You have to ask the user appropriate questions to understand the user's requirement.",
        ],
    )

    # Define web search agent
    web_agent: Agent = Agent(
            model=Ollama(id = "llama3.2"),
            tools=[GoogleSearchTools(fixed_max_results=100000), DuckDuckGoTools(fixed_max_results=100000)],
            show_tool_calls=True,
            description="You are an web search agent to help user for product recommendation.",
            response_model=WebSearchResults,
            instructions=[
                "You will be provides with an query from user about which type of product he/she wants to buy.",
                "Carefully read the query and provide the user with the top 5 products that match the query.",
                "Make sure to provide the product name, description and URL of the product.",
                "Give it as a list of products.",
            ],
            structured_outputs=False,
            markdown=True,
            stream=True,
        )

    # Define workflow steps
    def run(self, query: str = "") -> RunResponse:
        
        # Get web search response
        web_response = self.web_agent.run(query)
        web_content = web_response.content

        # Get chat response
        chat_response = self.chat_agent.run(web_content)
        chat_content = chat_response.content

        # Combine chat and web search responses
        content = f"{chat_content} \n\n {web_content}"
        return RunResponse(content=content)
    
# Initialize the workflow
workflow = SearchWorkflow()

# Run the workflow
response = workflow.run(query="Laptop")

# Print the response
print(response.content)
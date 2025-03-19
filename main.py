from agno.workflow import Workflow
from agno.agent import Agent
from rich.prompt import Prompt
from rich import print

from web_agent import Web_Agent
from user_memory import create_chat_agent, create_prompt_generator_agent

class SearchWorkflow(Workflow):
    
    # Define chat agent
    chat_agent: Agent = create_chat_agent()

    # Define web search agent
    web_agent: Agent = Web_Agent

    # Define query generator agent
    prompt_generator_agent: Agent = create_prompt_generator_agent()

    # Define workflow steps
    def run(self) -> None:

        exit_on = ["exit", "quit", "bye"]

        # Start chat with user
        while True:
            message = Prompt.ask(f"[bold] User [/bold]")
            if message in exit_on:
                break

            # Get query from user
            query = self.prompt_generator_agent.run(message).content

            print("Query: ", query) 
            
            # Get web response
            web_response = self.web_agent.run(query)
            web_content = web_response.content

            # Get chat response
            self.chat_agent.print_response(message=web_content, stream=True, markdown=True)
    
def main():
    # Create workflow
    workflow = SearchWorkflow()

    # Run workflow
    workflow.run()

if __name__ == "__main__":
    main()
from agno.workflow import Workflow
from agno.agent import Agent
from rich.prompt import Prompt
from rich import print

from web_agent import Web_Agent, Summerizer
from user_memory import create_chat_agent
from user_item_analyst import UserAnalystAgent

class SearchWorkflow(Workflow):
    
    # Define chat agent
    chat_agent: Agent = create_chat_agent()

    # Define web search agent
    web_agent: Agent = Web_Agent

    # Define summerizer agent
    summerizer_agent: Agent = Summerizer

    # Define workflow steps
    def run(self) -> None:

        exit_on = ["exit", "quit", "bye"]

        user_id = Prompt.ask("[bold] Enter user id [/bold]")
        if user_id == "":
            user_id = "1"

        # Define user analyst agent
        user_analyst_agent: UserAnalystAgent = UserAnalystAgent(user_id)

        user_history = user_analyst_agent.analyze_user_preferences()
        print("User history: ", user_history)
        
        query = str(user_history["user_profile"]) + "\n" + "highest rated movies by user: " + str(user_history['highest_rated_movies_by_user']) + "\n" + "recent movies: " + str(user_history['recent_movies']) + "\n" + "Genre count from user's history: " + str(user_history['top_genres'])
        self.chat_agent.print_response(message=query, stream=True, markdown=True)

        words_to_search = ["latest", "new", "recent", "2023", "2024", "2025"]

        # Start chat with user
        while True:
            message = Prompt.ask(f"[bold] User [/bold]")
            if message in exit_on:
                break

            if any(word in message.lower() for word in words_to_search):
                # Run web search agent
                print("Running web search agent...")
                response = self.web_agent.run(message)
                self.summerizer_agent.print_response(message=response, stream=True, markdown=True)
            else:
                self.chat_agent.print_response(message=message, stream=True, markdown=True)
    
def main():
    # Create workflow
    workflow = SearchWorkflow()

    # Run workflow
    workflow.run()

if __name__ == "__main__":
    main()
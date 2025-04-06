from agno.workflow import Workflow
from agno.agent import Agent
from rich.prompt import Prompt
from rich import print

from web_agent import Web_Agent, Summerizer
from user_memory import create_chat_agent, create_prompt_generator_agent
from user_item_analyst import UserAnalystAgent

class SearchWorkflow(Workflow):
    
    # Define chat agent
    chat_agent: Agent = create_chat_agent()

    # Define web search agent
    web_agent: Agent = Web_Agent

    # Define summerizer agent
    summerizer_agent: Agent = Summerizer

    # Define query generator agent
    prompt_generator_agent: Agent = create_prompt_generator_agent()

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

        highest_rated_movies = {}
        recent_movies = {}

        # for movie in user_history['highest_rated_movies_by_user']:
        #     title = movie 
        #     web_response = self.web_agent.run("Search for information of movie:" + title + " and return the information in text format")
        #     web_content = web_response.content
        #     web_content = self.summerizer_agent.run(web_content)
        #     web_content = web_content.content
        #     highest_rated_movies[title] = web_content
        #     print("info : "+ web_content)
        
        # for movie in user_history['recent_movies']:
        #     title = movie 
        #     web_response = self.web_agent.run("Search for information of movie:" + title)
        #     web_content = web_response.content
        #     recent_movies[title] = web_content
        
        query = str(user_history["user_profile"]) + "\n" + "highest rated movies by user: " + str(user_history['highest_rated_movies_by_user']) + "\n" + "recent movies: " + str(user_history['recent_movies']) + "\n" + "Genre count: " + str(user_history['top_genres'])
        self.chat_agent.print_response(message=query, stream=True, markdown=True)

        # Start chat with user
        while True:
            message = Prompt.ask(f"[bold] User [/bold]")
            if message in exit_on:
                break

            # # Get query from user
            # query = self.prompt_generator_agent.run(message).content

            # print("Query: ", query) 
            
            # # Get web response
            # web_response = self.web_agent.run(query)
            # web_content = web_response.content

            # # Get chat response
            # self.chat_agent.print_response(message=web_content, stream=True, markdown=True)
    
def main():
    # Create workflow
    workflow = SearchWorkflow()

    # Run workflow
    workflow.run()

if __name__ == "__main__":
    main()
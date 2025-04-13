from agno.agent import Agent
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.hackernews import HackerNewsTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.models.ollama import Ollama
from user_item_db import UserItemDB
from agno.storage.sqlite import SqliteStorage
from rich.prompt import Prompt
# from rich import print

Web_Agent = Agent(
    name="Web Agent",
    model=Ollama(id = "llama3.2"),
    tools=[GoogleSearchTools(fixed_max_results=100000), DuckDuckGoTools(fixed_max_results=100000), HackerNewsTools()],
    show_tool_calls=True,
    role="Web search agent to find information on the web.",
    instructions=[
        "You are a web search agent. You will be given a query and you need to search for information related to that query.",
        "You will use the tools provided to you to search for information.",
    ],
    structured_outputs=False,
    markdown=True,
    stream=True,
)

class UserAnalystAgent(Agent):
    def __init__(self, user_id):
        super().__init__(
            name="User Analyst Agent",
            model=Ollama(id="llama3.2"),
            role="Analyzes a user's movie preferences based on their history.",
            instructions=[
                "You analyze user preferences based on their watch history and ratings.",
                "Use this information to identify favorite genres, top-rated movies, and recent activity.",
            ],
        )
        self.user_item_db = UserItemDB("movies_database.db")
        self.user_id = user_id

    def analyze_user_preferences(self):
        """Returns a summary of the user's preferences."""
        history = self.user_item_db.get_user_item_history(self.user_id)
        profile = self.user_item_db.get_user_profile(self.user_id)

        if not history:
            return {"error": "No user history found."}

        genre_score = {}
        titles = []

        for idx, (item_id, rating) in enumerate(zip(history['history_item_ids'], history['history_ratings'])):
            item = self.user_item_db.get_item_attributes(item_id)
            if not item:
                continue

            # Aggregate genre scores
            for genre in item['genres']:
                genre_score[genre] = genre_score.get(genre, 0) + rating

            titles.append({
                "title": item['title'],
                "rating": rating,
                "order": idx
            })

        # Sort results
        top_genres = sorted(genre_score.items(), key=lambda x: x[1], reverse=True)
        top_rated = sorted(titles, key=lambda x: x["rating"], reverse=True)[:5]
        recent = sorted(titles, key=lambda x: x["order"], reverse=True)[:5]

        return {
            "user_profile": profile,
            "top_genres": [g[0] for g in top_genres],
            "highest_rated_movies": [m["title"] for m in top_rated],
            "recent_movies": [m["title"] for m in recent],
        }

    
# user_id = Prompt.ask(f"[bold] Enter User ID: [/bold]")

user_analyst_agent = UserAnalystAgent(user_id="703")
# user_history = user_analyst_agent.analyze_user_preferences()
# print("User history: ", user_history)
# query = str(user_history["user_profile"]) + "\n" + "highest rated movies by user: " + str(user_history['highest_rated_movies_by_user']) + "\n" + "recent movies: " + str(user_history['recent_movies']) + "\n" + "Genre count from user's history: " + str(user_history['top_genres'])


orchastrator = Team(
    name="Orchastrator",
    model=Ollama(id="llama3.2"),
    mode="coordinate",
    members=[Web_Agent, user_analyst_agent],
    instructions = [
        "You are an orchestrator agent responsible for generating personalized movie recommendations for the user.",
        "You coordinate two specialized agents:",
        "  • `UserAnalystAgent`: Analyzes the user's viewing history and preferences.",
        "  • `Web_Agent`: Searches the internet for relevant movie information, reviews, and trends.",

        "Follow these steps to assist the user effectively:",
        "1. Use the `UserAnalystAgent` to retrieve the user's profile, viewing history, favorite genres, and top-rated or recent movies.",
        "2. Analyze the results to understand the user's taste (e.g., preferred genres, highly rated films, watching patterns).",
        "3. If additional movie suggestions are needed or context is missing (e.g., mood, current interests), ask the user specific follow-up questions.",
        "4. Use the `Web_Agent` to search for new or trending movies that align with the user's preferences or criteria.",
        "5. Combine insights from the user data and web search to recommend 3-5 personalized movie suggestions.",
        "6. For each recommendation, briefly explain why it was chosen (e.g., 'Matches your top genre: Sci-Fi' or 'Similar to Inception, which you rated highly').",
        "7. Format the final response clearly using markdown for readability (e.g., bullet points, headers).",
        
        "Your goal is to be helpful, accurate, and user-focused. Always provide concise and thoughtful recommendations.",
    ],

    storage=SqliteStorage(
        table_name="team_sessions", db_file="tmp/data.db", auto_upgrade_schema=True
    ),
    num_of_interactions_from_history=5,
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
    show_members_responses=True,
)


# orchastrator.print_response(message=query, stream=True, markdown=True)

while True:

    message = Prompt.ask(f"[bold] User [/bold]")
    if message.lower() in ["exit", "quit", "bye"]:
        break

    # Run the orchestrator agent
    orchastrator.print_response(message=message, stream=True, markdown=True)
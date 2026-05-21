import os

from tavily import TavilyClient

from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

def search_web(query):

    try:

        response = client.search(
            query=query,
            max_results=3
        )

        return response["results"]

    except Exception as e:

        print("Web Search Error:", e)

        return []
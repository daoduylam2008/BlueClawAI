import os
import requests
import re
import models

from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper

from dotenv import load_dotenv


load_dotenv() 
# Set up USER_AGENT for web scraping, which prevents program from websites blocking
os.environ["USER_AGENT"] = 'myagent'


@tool(description="Get the weather data for a specific city or location (these are not Latitude and Longitude). Only use this when user wants to know about weather.", args_schema=models.WeatherInput)
def get_location_weather(location):
    """Get weather data for a given location or city"""
    url = "http://api.openweathermap.org/data/2.5/weather?"
    params = {
        'q': location,
        'appid': os.getenv("OPENWEATHER_KEY_API"),
        'units': 'metric',
        'lang': 'en'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    answer = {
        'weather': response.json()['weather'],
        'main': response.json()['main'],
        'wind': response.json()['wind']
    }

    return answer


@tool(description="Searches the web using DuckDuckGo for the given query and attempts to load the content from the first search result. If content loading fails, it returns the search snippets.")
def websearch(query: str):
    search_model = DuckDuckGoSearchRun()
    search_results = search_model.run(query)

    if not search_results:
        return "No relevant search results found."

    first_link = None
    link_match = re.search(r"link: (https?://[^\s,\]]+)", search_results)

    if link_match:
        first_link = link_match.group(1)

    if first_link:
        try:
            loader = WebBaseLoader(first_link)
            docs = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=200)
            splits = text_splitter.split_documents(docs)

            combined_content = "\n\n".join([split.page_content for split in splits[:2]]) # Take first 2 chunks
            return combined_content if combined_content else "No content could be extracted from the link."
        
        except Exception as e:
            return f"Could not load full content from link. Search results: {search_results}"

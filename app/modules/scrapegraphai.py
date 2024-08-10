from scrapegraphai.graphs import SmartScraperGraph, SearchGraph
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()

import nest_asyncio

async def run_blocking_code_in_thread(blocking_func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, blocking_func, *args)


class ScrapeGraphAiEngine:
    """
    You can find the model_provider by langchain website:
    https://api.python.langchain.com/en/latest/chat_models/langchain.chat_models.base.init_chat_model.html
    """
    def __init__(
            self,
            model_provider: str,
            model_name: str,
            temperature: float = 0
    ):
        self.model_provider = model_provider
        self.model_name = model_name
        self.temperature = temperature

        self.model_tokens = 128000
        self.graph_config = self.create_model_instance_config()

    async def crawl(
            self,
            prompt: str,
            source: str
    ):
        smart_scraper_graph = SmartScraperGraph(
            prompt=prompt,
            source=source,
            config=self.graph_config
        )

        result = await run_blocking_code_in_thread(smart_scraper_graph.run)
        return result

    async def search(
            self,
            prompt: str,
    ):
        nest_asyncio.apply()

        search_graph = SearchGraph(
            prompt=prompt,
            config=self.graph_config
        )

        result = search_graph.run()
        return result

    def create_model_instance_config(
            self
    ):
        graph_config = {
            "llm": {},
            "verbose": True,
        }

        if self.model_provider == "google_genai":
            graph_config["llm"] = {
                "model": self.model_name,
                "api_key": os.environ["GOOGLE_API_KEY"]
            }
            if os.getenv("GOOGLE_API_ENDPOINT"):
                graph_config["llm"]["transport"] = "rest"
                graph_config["llm"]["client_options"] = {"api_endpoint": os.environ['GOOGLE_API_ENDPOINT']}

        else:
            graph_config["llm"] = {
                "model": self.model_name,
                "api_key": os.getenv("API_KEY")
            }
            if os.getenv("API_BASE_URL"):
                graph_config["llm"]["base_url"] = os.getenv("API_BASE_URL")

        return graph_config



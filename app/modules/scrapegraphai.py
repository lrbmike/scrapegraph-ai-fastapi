from scrapegraphai.graphs import SmartScraperGraph, SearchGraph
from scrapegraphai.helpers import models_tokens
from langchain.chat_models import init_chat_model
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
            temperature: float = 0,
            model_instance: bool = False
    ):
        self.model_provider = model_provider
        self.model_name = model_name
        self.temperature = temperature
        self.model_instance = model_instance

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

    def create_llm(
            self
    ):
        # special treatment of Gemini models
        if self.model_provider == "google_genai":
            if models_tokens["gemini"][self.model_name]:
                self.model_tokens = models_tokens["gemini"][self.model_name]

            # use api endpoint
            if os.getenv("GOOGLE_API_ENDPOINT"):

                return init_chat_model(
                    self.model_name, model_provider=self.model_provider, temperature=self.temperature,
                    api_key=os.environ["GOOGLE_API_KEY"], transport="rest",
                    client_options={"api_endpoint": os.environ['GOOGLE_API_ENDPOINT']}
                )

            return init_chat_model(
                self.model_name, model_provider=self.model_provider, temperature=self.temperature,
                api_key=os.environ["GOOGLE_API_KEY"]
            )

        else:
            if models_tokens[self.model_provider][self.model_name]:
                self.model_tokens = models_tokens[self.model_provider][self.model_name]

            return init_chat_model(
                self.model_name, model_provider=self.model_provider, temperature=self.temperature,
                api_key=os.environ["API_KEY"], base_url=os.environ["API_BASE_URL"]
            )

    def create_model_instance_config(
            self
    ):
        graph_config = {
            "llm": {},
            "verbose": True,
        }

        if self.model_instance:
            llm = self.create_llm()

            graph_config["llm"] = {
                "model_instance": llm,
                "model_tokens": self.model_tokens,
            }

        else:

            # special treatment of Gemini models
            if self.model_provider == "google_genai":
                # use api endpoint
                if os.getenv("GOOGLE_API_ENDPOINT"):
                    graph_config["llm"] = {
                        "model": self.model_name,
                        "api_key": os.environ["GOOGLE_API_KEY"],
                        "transport": "rest",
                        "client_options": {"api_endpoint": os.environ['GOOGLE_API_ENDPOINT']}
                    }
                else:
                    graph_config["llm"] = {
                        "model": self.model_name,
                        "api_key": os.environ["GOOGLE_API_KEY"]
                    }
            # special treatment of local models
            elif self.model_provider == "ollama":
                graph_config["llm"] = {
                    "model": self.model_name,
                    "format": "json", # Ollama needs the format to be specified explicitly
                    # "base_url": "http://localhost:11434",
                }
            else:
                graph_config["llm"] = {
                    "model": self.model_name,
                    "api_key": os.getenv("API_KEY"),
                    "base_url": os.getenv("API_BASE_URL")
                }

            return graph_config

from scrapegraphai.graphs import SmartScraperGraph, SearchGraph
from scrapegraphai.helpers import models_tokens
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()


async def run_blocking_code_in_thread(blocking_func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, blocking_func, *args)


class ScrapeGraphAiEngine:

    def __init__(
            self,
            llm_name: str,
            model_name: str,
            embeddings_name: str,
            temperature: float = 0,
            model_instance: bool = False
    ):
        self.llm_name = llm_name
        self.model_name = model_name
        self.embeddings_name = embeddings_name
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
        search_graph = SearchGraph(
            prompt=prompt,
            config=self.graph_config
        )

        result = await run_blocking_code_in_thread(search_graph.run)
        return result

    def create_llm(
            self
    ):
        if self.llm_name == "Gemini":
            if models_tokens["gemini"][self.model_name]:
                self.model_tokens = models_tokens["gemini"][self.model_name]

            return ChatGoogleGenerativeAI(model=self.model_name, temperature=self.temperature,
                                          google_api_key=os.getenv('GOOGLE_API_KEY'))

        elif self.llm_name == "OpenAI":
            if models_tokens["openai"][self.model_name]:
                self.model_tokens = models_tokens["openai"][self.model_name]

            return ChatOpenAI(model=self.model_name, temperature=self.temperature,
                              api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_API_BASE"))

    def create_embeddings(
            self
    ):
        if self.llm_name == "Gemini":
            return GoogleGenerativeAIEmbeddings(model=self.embeddings_name,
                                                google_api_key=os.environ['GOOGLE_API_KEY'])

        elif self.llm_name == "OpenAI":
            return OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_API_BASE"))

    def create_model_instance_config(
            self
    ):

        if self.model_instance:
            llm = self.create_llm()
            embeddings = self.create_embeddings()

            graph_config = {
                "llm": {
                    "model_instance": llm,
                    "model_tokens": self.model_tokens,
                },
                "embeddings": {
                    "model_instance": embeddings,
                },
                "verbose": True,
            }

            return graph_config

        else:

            graph_config = {
                "llm": {
                    "model": self.model_name,
                    "api_key": os.getenv("OPENAI_API_KEY"),
                    "base_url": os.getenv("OPENAI_API_BASE")
                },
                "embeddings": {
                    "model": self.embeddings_name,
                },
                "verbose": True,
            }

            return graph_config

from scrapegraphai.graphs import SmartScraperGraph
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import os
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()


async def run_blocking_code_in_thread(blocking_func, *args):
    loop = asyncio.get_event_loop()
    # loop = asyncio.ProactorEventLoop()
    return await loop.run_in_executor(executor, blocking_func, *args)


class ScrapeGraphAiEngine:

    def __init__(
            self,
            llm_name: str,
            model_name: str,
            embeddings_name: str,
    ):
        self.llm_name = llm_name
        self.model_name = model_name
        self.embeddings_name = embeddings_name

        self.llm_model_tokens = 128000
        self.embeddings_model_tokens = 2048

    async def crawl(
            self,
            prompt: str,
            source: str
    ):
        llm = self.create_llm()
        embeddings = self.create_embeddings()

        graph_config = {
            "llm": {
                "model_instance": llm,
                "model_tokens": self.llm_model_tokens,
            },
            "embeddings": {
                "model_instance": embeddings,
                "model_tokens": self.embeddings_model_tokens,
            },
            "verbose": True,
        }

        smart_scraper_graph = SmartScraperGraph(
            prompt=prompt,
            source=source,
            config=graph_config
        )

        result = await run_blocking_code_in_thread(smart_scraper_graph.run)
        return json.dumps(result, indent=4)

    def create_llm(
            self
    ):
        if self.llm_name == "gemini":
            self.llm_model_tokens = 128000

            return ChatGoogleGenerativeAI(model=self.model_name, temperature=0.3,
                                          google_api_key=os.environ['GOOGLE_API_KEY'])

    def create_embeddings(
            self
    ):
        if self.llm_name == "gemini":
            self.embeddings_model_tokens = 2048

            return GoogleGenerativeAIEmbeddings(model=self.embeddings_name,
                                                google_api_key=os.environ['GOOGLE_API_KEY'])

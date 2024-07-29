from fastapi import APIRouter, Body
from app.modules import ScrapeGraphAiEngine

router = APIRouter(
    prefix="/crawl"
)


@router.post("/smart_scraper_graph")
async def smartScraperGraph(
        prompt: str = Body(embed=True),
        url: str = Body(embed=True),
        llm_name: str = Body(embed=True),
        model_name: str = Body(embed=True),
        embeddings_name: str = Body(embed=True),
):
    engine = ScrapeGraphAiEngine(llm_name=llm_name, model_name=model_name,
                                 embeddings_name=embeddings_name)

    return await engine.crawl(prompt=prompt, source=url)

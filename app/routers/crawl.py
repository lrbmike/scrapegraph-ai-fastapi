from fastapi import APIRouter, Body
from typing import Optional
from app.modules import ScrapeGraphAiEngine

router = APIRouter(
    prefix="/crawl"
)


@router.post("/scraper_graph")
async def scraper_graph(
        prompt: str = Body(embed=True),
        url: str = Body(embed=True),
        model_provider: str = Body(embed=True),
        model_name: str = Body(embed=True),
        temperature: Optional[float] = Body(embed=False)
):
    engine = ScrapeGraphAiEngine(model_provider=model_provider, model_name=model_name,
                                 temperature=temperature)

    return await engine.crawl(prompt=prompt, source=url)


@router.post("/search_graph")
async def search_graph(
        prompt: str = Body(embed=True),
        model_provider: str = Body(embed=True),
        model_name: str = Body(embed=True),
        temperature: float = Body(embed=False)
):
    engine = ScrapeGraphAiEngine(model_provider=model_provider, model_name=model_name,
                                 temperature=temperature)

    return await engine.search(prompt=prompt)

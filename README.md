# ScrapeGraphAI FastAPI Framework

Project base on [ScrapeGraphAI](https://github.com/ScrapeGraphAI/Scrapegraph-ai.git), and use FastAPI to provide interface services externally.

## Install

```shell
pip install -r requirements.txt
# Browser driver install
playwright install
```

## Environment
Currently, only Gemini and OpenAI models are available. Edit `.env` file

## Run
It's important to note that you can't start in `dev` mode, as playwright will fail in `dev` mode, Otherwise, it will be reported as a "NotImplementedError" error.
```shell
fastapi run app/main.py
```

## Use
scraper graph 
```shell
curl -X POST https://your-domain/crawl/scraper_graph \
-H "Content-Type: application/json" \
-d '{
    "prompt": "List me all the projects with their title、description、url、published",
    "url": "https://techcrunch.com/category/artificial-intelligence/",
    "llm_name": "Gemini",
    "model_name": "gemini-1.5-flash-latest",
    "embeddings_name": "models/text-embedding-004",
    "temperature": 0,
    "model_instance": true
}'

```

search graph 
```shell
curl -X POST https://your-domain/crawl/search_graph \
-H "Content-Type: application/json" \
-d '{
    "prompt": "List me all the traditional recipes from Chioggia",
    "llm_name": "Gemini",
    "model_name": "gemini-1.5-flash-latest",
    "embeddings_name": "models/text-embedding-004",
    "temperature": 0,
    "model_instance": true
}'
```

## Docker
`Dockerfile` introduce `mcr.microsoft.com/playwright/python:v1.45.1-jammy` provide a `playwright` environment. So we don't need to install any more.

Or you can publish to [Render](https://render.com/)

## Known issues
The current support for models is not perfect, and there are quite a few such problems in [Scrapegraph-ai](https://github.com/ScrapeGraphAI/Scrapegraph-ai/issues).
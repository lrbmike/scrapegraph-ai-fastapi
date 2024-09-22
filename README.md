# ScrapeGraphAI FastAPI Framework

Project base on [ScrapeGraphAI](https://github.com/ScrapeGraphAI/Scrapegraph-ai.git), and use FastAPI to provide interface services externally.

## Install

```shell
pip install -r requirements.txt
# Browser driver install
playwright install
# If prompted "ImportError: burr package is not installed. Please install it with 'pip install scrapegraphai[burr]'"
pip install scrapegraphai[burr]
# If prompted RuntimeError: To use the fastapi command, please install "fastapi[standard]"
pip install "fastapi[standard]"
```

## Environment
Edit `.env` file, Due to the special nature of the Gemini model, it is configured separately. Other models are configurable via `API_KEY` and `API_BASE_URL`

```
GOOGLE_API_KEY=
GOOGLE_API_ENDPOINT=
API_KEY=
API_BASE_URL=
```

## Run
It's important to note that you can't start in `dev` mode, as playwright will fail in `dev` mode, Otherwise, it will be reported as a "NotImplementedError" error.
```shell
fastapi run app/main.py
```

## Use

> The project use langchain init_chat_model function to initialize a ChatModel from the model name and provider, you can find them by langchain website [init_chat_model](https://api.python.langchain.com/en/latest/chat_models/langchain.chat_models.base.init_chat_model.html)

### Gemini Model

You need to set  `GOOGLE_API_KEY` or `GOOGLE_API_ENDPOINT`  in `.env` file first. If you set `GOOGLE_API_ENDPOINT` , it will be configured into the Gemini model.

#### scraper graph

```shell
curl -X POST https://your-domain/crawl/scraper_graph \
-H "Content-Type: application/json" \
-d '{
    "prompt": "List me all the articles with their title、description、link、published",
    "url": "https://techcrunch.com/category/artificial-intelligence/",
    "model_provider": "google_genai",
    "model_name": "google_genai/gemini-1.5-flash-latest",
    "temperature": 0
}'

```

#### search graph

```shell
curl -X POST https://your-domain/crawl/search_graph \
-H "Content-Type: application/json" \
-d '{
    "prompt": "List me all the traditional recipes from Chioggia",
    "model_provider": "google_genai",
    "model_name": "google_genai/gemini-1.5-flash-latest",
    "temperature": 0
}'
```

### OpenAI Model

You need to set  `API_KEY` or `API_BASE_URL`  in `.env` file first. If you set `API_BASE_URL` , it will be configured into the OpenAI model.

#### scraper graph

```shell
curl -X POST https://your-domain/crawl/scraper_graph \
-H "Content-Type: application/json" \
-d '{
    "prompt": "List me all the articles with their title、description、link、published",
    "url": "https://techcrunch.com/category/artificial-intelligence/",
    "model_provider": "openai",
    "model_name": "gpt-4o-mini",
    "temperature": 0
}'
```

#### search graph

```shell
curl -X POST https://your-domain/crawl/search_graph \
-H "Content-Type: application/json" \
-d '{
    "prompt": "List me all the traditional recipes from Chioggia",
    "model_provider": "openai",
    "model_name": "gpt-4o-mini",
    "temperature": 0
}'
```

### Ollama

#### scraper graph

```shell
curl -X POST https://your-domain/crawl/scraper_graph \
-H "Content-Type: application/json" \
-d '{
    "prompt": "List me all the articles with their title、description、link、published",
    "url": "https://next.ithome.com/",
    "model_provider": "ollama",
    "model_name": "ollama/llama3.1",
    "temperature": 0
}'
```

#### search graph

```shell
curl -X POST https://your-domain/crawl/search_graph \
-H "Content-Type: application/json" \
-d '{
    "prompt": "List me all the traditional recipes from Chioggia",
    "model_provider": "ollama",
    "model_name": "ollama/llama3.1",
    "temperature": 0
}'
```

## Docker

`Dockerfile` introduce `mcr.microsoft.com/playwright/python:v1.45.1-jammy` provide a `playwright` environment. So we don't need to install any more.

Or you can publish to [Render](https://render.com/)

## Known issues
> The current support for models is not perfect, and there are quite a few such problems in [Scrapegraph-ai](https://github.com/ScrapeGraphAI/Scrapegraph-ai/issues).


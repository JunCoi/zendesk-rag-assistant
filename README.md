# Zendesk RAG Assistant

RAG assistant for OptiSigns support documentation.

## Features

* Fetches articles from the OptiSigns Zendesk API
* Converts HTML articles to Markdown
* Uploads Markdown files to an OpenAI Vector Store
* Uses OpenAI Assistant + File Search for retrieval
* Performs daily delta sync using SHA256 content hashes
* Uploads only new or updated articles

## Setup

Create `.env`:

```bash
OPENAI_API_KEY=...
ZENDESK_SUBDOMAIN=support.optisigns.com
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Locally

Run the complete sync pipeline:

```bash
python -m src.main
```

Run tests:

```bash
python -m pytest
```

## Docker

Build:

```bash
docker build -t zendesk-rag-assistant .
```

Run:

```bash
docker run --env-file .env zendesk-rag-assistant
```

## Delta Sync Strategy

This project stores SHA256 hashes of generated Markdown files in `data/article_hashes.json`.

During each run:

* New files → added
* Changed files → updated
* Unchanged files → skipped

Only added and updated files are uploaded to OpenAI.

## Daily Job

DigitalOcean Scheduled Job:

```
<ADD_JOB_URL_HERE>
```

## Screenshot

Assistant answering:

> How do I add a YouTube video?

with source citations from uploaded documentation.

![Assistant Answer](screenshots/how-to-add-youtube-video-answer.png)

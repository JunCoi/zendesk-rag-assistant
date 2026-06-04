# Zendesk RAG Assistant

A support knowledge assistant that fetches Zendesk articles, converts them to Markdown, uploads them to OpenAI Vector Store, and answers questions using retrieved documentation.

## Step 1 – Scrape and Convert Articles to Markdown

### Objective

The goal of this step is to ingest support documentation from OptiSigns and normalize it into a format suitable for retrieval-augmented generation (RAG).

Requirements:

* Fetch at least 30 articles from `support.optisigns.com`
* Convert articles into clean Markdown
* Preserve headings, links, and code blocks
* Remove navigation, layout, and other non-content elements
* Store each article as an individual Markdown document

---

### Data Source

Articles are retrieved from the Zendesk Help Center API used by OptiSigns support documentation.

Example endpoint:

```text
https://support.optisigns.com/api/v2/help_center/articles.json
```

Using the API provides structured article content and avoids the complexity and instability of HTML scraping.

---

### Ingestion Pipeline

```text
Zendesk API
↓
Fetch Articles
↓
Save Raw JSON
↓
Convert HTML Body → Markdown
↓
Generate Slug Filename
↓
Save to data/markdown
```

---

### Markdown Conversion

Each Zendesk article contains HTML content in its body field.

The conversion process:

1. Extract article title, URL, and HTML body.
2. Convert HTML into Markdown.
3. Preserve:

   * Headings
   * Lists
   * Tables (where supported)
   * Links
   * Code blocks
4. Remove:

   * Navigation elements
   * Layout wrappers
   * Styling information
   * Advertisement or portal-specific content

Each generated document begins with metadata:

```md
# Article Title

Article URL: https://support.optisigns.com/...

---
```

Including the source URL directly in the document improves retrieval quality and enables citation generation during question answering.

---

### File Naming

Each article is saved using a slugified version of its title:

```text
How to Use the YouTube Dashboard App
↓
how-to-use-the-youtube-dashboard-app.md
```

Benefits:

* Human readable
* Stable filenames
* Easy debugging and validation

---

### Output Structure

```text
data/
├── raw/
│   ├── articles.json
│   └── ...
└── markdown/
    ├── how-to-use-the-youtube-dashboard-app.md
    ├── optisigns-getting-started-guide.md
    ├── split-screen-app.md
    └── ...
```

---

### Results

| Metric                   | Value |
| ------------------------ | ----- |
| Articles Retrieved       | XX    |
| Markdown Files Generated | XX    |
| Conversion Failures      | 0     |

All generated Markdown files were successfully prepared for ingestion into the OpenAI Vector Store used in Step 2.

---

### Testing

The ingestion pipeline is covered by automated unit tests.

Test coverage includes:

* Article retrieval
* Article limit handling
* File saving
* Slug generation
* HTML-to-Markdown conversion
* Article-to-Markdown transformation

These tests verify that content is correctly normalized before being uploaded to the vector store.


## Step 2 – Build Assistant & Load Vector Store

### Assistant Configuration

An OpenAI Assistant named **OptiBot** was created and configured with the following system prompt:

```text
You are OptiBot, the customer-support bot for OptiSigns.com.
• Tone: helpful, factual, concise.
• Only answer using the uploaded docs.
• Max 5 bullet points; else link to the doc.
• Cite up to 3 "Article URL:" lines per reply.
```

The assistant is configured with the `file_search` tool and connected to a Vector Store containing the processed OptiSigns support articles.

---

### Uploading Documents

All Markdown documents generated during the ingestion step are uploaded programmatically using the OpenAI Python SDK.

Process:

```text
Markdown Files
↓
Upload to OpenAI Files API
↓
Attach to Vector Store
↓
OpenAI performs chunking and embedding
↓
Assistant retrieves relevant chunks at runtime
```

No files were uploaded manually through the OpenAI UI.

---

### Chunking Strategy

This project uses OpenAI's built-in Vector Store chunking and embedding pipeline.

Rationale:

* Keeps implementation simple and maintainable.
* Leverages OpenAI's retrieval optimizations.
* Suitable for the relatively small document set (~30 support articles).
* Eliminates the need to manage custom chunk boundaries or embedding generation.

Metadata such as:

```text
Article URL: https://support.optisigns.com/...
```

is included near the beginning of each Markdown document to improve retrieval quality and citation generation.

---

### Embedding Statistics

| Metric                  | Value     |
| ----------------------- | --------- |
| Articles Processed      | XX        |
| Markdown Files Uploaded | XX        |
| Failed Uploads          | 0         |
| Vector Store Status     | Completed |

> The exact values are logged during execution and can be seen in the script output.

---

### Sanity Check

A fresh thread was created and queried with:

```text
How do I add a YouTube video?
```

The assistant successfully:

* Retrieved the correct OptiSigns documentation.
* Generated a concise answer.
* Included source citations using `Article URL`.
* Avoided hallucinated information.

Example citation:

```text
Article URL: https://support.optisigns.com/hc/en-us/articles/48626115821459-How-to-Use-the-YouTube-Dashboard-App
```

A screenshot of the successful response is included in the repository.


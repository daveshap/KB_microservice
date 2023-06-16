# KB Microservice

The KB Microservice is a Python-based application that provides a simple and efficient way to manage a knowledge base
(KB) of articles. It allows users to create, search, and update KB articles through a RESTful API. The service uses
OpenAI's GPT model to process and generate the content of the articles.


| Endpoint | Method | Description | Parameters | Example Request |
| --- | --- | --- | --- | --- |
| `/create` | POST | Creates a new KB article | `input`: The text for the new KB article | `{ "input": "This is the text for the new KB article." }` |
| `/search` | POST | Searches for KB articles | `query`: The search query | `{ "query": "search query" }` |
| `/update` | POST | Updates an existing KB article | `title`: The title of the KB article to update<br>`input`: The new text for the KB article | `{ "title": "Article 1", "input": "This is the updated text for the KB article." }` |

## Setup

1. Create `key_openai.txt` and place your API key within.
2. Create `kb/` directory for your KB articles.
3. Install all requirements in `requirements.txt`.

## Usage

1. Run `kb_microservice.py` - this is a Flask app that runs on 999 by default.
2. Test it using `test_kb_service.py` to create, search, and update KB articles.

# How It Works

The KB Microservice uses Flask, a lightweight web framework for Python, to expose endpoints for creating, searching, and
updating KB articles. The service uses YAML files to store the articles, and a directory text file to keep track of all
the articles in the knowledge base.

The service uses OpenAI's GPT model to process user inputs and generate the content of the articles. The GPT model
is a powerful language model that can generate human-like text based on the input it receives.

## Creating KB Articles

To create a KB article, a POST request is made to the `/create` endpoint with a JSON payload containing the text for the
article. The service then uses the GPT model to process the text and generate a JSON object containing the title,
description, keywords, and body of the article. The article is then saved as a YAML file in the knowledge base
directory.

## Searching KB Articles

To search for KB articles, a POST request is made to the `/search` endpoint with a JSON payload containing the search
query. The service first updates the directory of articles, then uses the GPT model to process the query and return a
list of relevant article filenames. The service then opens each file, converts the YAML content to JSON, and returns the
list of articles as a JSON response.

## Updating KB Articles

To update a KB article, a POST request is made to the `/update` endpoint with a JSON payload containing the title of the
article to update and the new text for the article. The service first opens the existing article, then uses the GPT
model to process the new text and generate an updated JSON object for the article. The updated article is then saved
back to the knowledge base directory.

# Future Work

1. Daily Journal (episodic memory)
   - Prioritize based on relevance, or temporal proximity
2. Tasks (like internal Jira or Trello)
   - Prioritize based on ROI or heuristic imperatives (e.g. which tasks will reduce suffering the most, increase prosperity the most, and increase understanding the most)
3. Dossiers (basically KB article on users)
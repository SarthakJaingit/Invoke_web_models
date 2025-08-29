from firecrawl import Firecrawl
import os
import requests
import json
import time
from typing import List, Optional
from pydantic import BaseModel, Field
import schemas


# Then see if we (given a page) make a list of Q and A data, Instruct Tuning Data, Multi-Dialogue, Fill in the blank data 
# Make a function for when there is a lot on a docs page vs less on a docs page

# To do:
# Compare the output of both data schemas. Choose 1 for VBO tickets
# Then go from page extracting to crawling
# Form the dataset and (then train finetuned model that can output good context)


# Does putting in the prompt (5-10 sentences or saying I want to make a large LLM dataset in future

API_KEY = os.environ.get("FIRECRAWL_API_KEY")

FIRECRAWL_API = "https://api.firecrawl.dev/v2/scrape"

url_to_scrape = "https://vbotickets.helpdocsite.com/crm/how-to-use-account-credit"
# url_to_scrape = "https://vbotickets.helpdocsite.com/crm"
# url_to_scrape = "https://www.vbotickets.com/pricing/"

Pageqa_schema = schemas.PageQA.model_json_schema()
print(f"JSON Schema: {Pageqa_schema}")
payload_prompt = """
    You are looking at a company's documentation or product webpage.

    Extract as many useful Q&A pairs as possible, imagining what a customer or support rep might ask about this page.

    For each question:
    - Provide a clear, specific answer grounded in the page content.
    - Optionally, add 1–3 paraphrases (alternative phrasings).
    - If possible, assign a category: usage, pricing, limitations, setup, policy, integrations, etc.
    - If possible, include the sentence or paragraph from the page that supports your answer.

    Be diverse:
    - Include “what”, “how”, “can”, “when”, and “why” style questions.
    - If possible, Include **questions about workflows** — how to perform specific actions or navigate the UI 
    - If possible, Include **questions about use cases and applications** (how a feature might be used in real scenarios)
    - If possible, Include **questions about limitations or caveats** (what can’t be done, restrictions, edge cases)
    - If possible, Include **Vague or high-level user questions** (e.g., "How can this help me?" or "Why is this useful?")
    - It's okay to have overlapping questions if phrased differently or with distinct intent.

    **Important:**
    - Return **as many Q&A pairs as possible** — aim for at least 40 if the content allows it.
    - If the page is long, extract more. Long pages should have up to 100-200 Q&A.
    - Prefer variety: "what", "how", "when", "can", "why", etc.
"""

payload = { 
    "url": url_to_scrape,
    "formats": ["markdown", { 
            "type": "json", 
            "prompt": payload_prompt, 
            "schema": Pageqa_schema}],
    "onlyMainContent": True,
    "blockAds": True, 
    "removeBase64Images": True,
    "excludeTags": ["nav", "header", "footer", "aside", ".sidebar", "#menu", "script", "style"]
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


resp = requests.post(FIRECRAWL_API, headers=headers, json=payload)
resp.raise_for_status()

# Parse the response
response = resp.json()
print(json.dumps(response, indent=2))

# Save the result
with open("firecrawl_ft_3_scrape_result.json", "w", encoding="utf-8") as f:
    json.dump(response, f, indent=2, ensure_ascii=False)





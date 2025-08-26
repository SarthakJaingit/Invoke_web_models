from firecrawl import Firecrawl
import os
import requests
import json
import time
from typing import List, Optional
from pydantic import BaseModel, Field
import schemas

# See if we can make a true or false of if a feature is in a page
# See if we can create feature descrption on a page
# Then see if we (given a page) make a list of Q and A data, Instruct Tuning Data, Multi-Dialogue, Fill in the blank data 

API_KEY = os.environ.get("FIRECRAWL_API_KEY")

FIRECRAWL_API = "https://api.firecrawl.dev/v2/scrape"

url_to_scrape = "https://vbotickets.helpdocsite.com/crm/how-to-use-account-credit"
# url_to_scrape = "https://vbotickets.helpdocsite.com/crm"
utl_to_scrape = "https://www.vbotickets.com/pricing/"

# payload = { 
#     "url": url_to_scrape,
#     "formats": ["markdown"],
#     "onlyMainContent": True,
#     "blockAds": True, 
#     "removeBase64Images": True,
#     "excludeTags": ["nav", "header", "footer", "aside", ".sidebar", "#menu", "script", "style"]
# }

# payload_prompt= """
# You are looking at the webpages of a company.
# Look at the webpage and output a boolean whether this specific page has information on a specific feature of the company.
# """

payload_prompt = """
You are looking at webpages of a company's product or help documentation.
Your task is to determine whether the page provides real, substantive information about a specific feature of the product.

Respond `true` if and only if the page contains:
- Detailed explanations, descriptions, or instructions about what the feature does, how it works, or how to use it.
- Actual written prose describing the feature (not just a list or a link).

Do **not** return true for:
- Pages that merely list feature names without explanation.
- Pages that act as directories or tables of contents (e.g. just list links to other pages).
- Pages that only contain images or diagrams without accompanying text.

Return `true` or `false` based on the actual content present on the page.
"""

json_schema = schemas.PageBools.model_json_schema()
print(f"JSON Schema: {json_schema}")


payload = { 
    "url": url_to_scrape,
    "formats": ["markdown", { 
            "type": "json", 
            "prompt": payload_prompt, 
            "schema": json_schema }],
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
with open("firecrawl_scrape_result.json", "w", encoding="utf-8") as f:
    json.dump(response, f, indent=2, ensure_ascii=False)



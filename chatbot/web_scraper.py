from firecrawl import Firecrawl
import os
import requests
import json
import time
from typing import List, Optional
from pydantic import BaseModel, Field
import schemas

# Full job ran at once
API_KEY = os.environ.get("FIRECRAWL_API_KEY")

FIRECRAWL_API = "https://api.firecrawl.dev/v2/crawl"

# payload = { 
#     "url" : "https://www.vbotickets.com/",
#     "limit": 10,                         
#     "crawlEntireDomain": True,
#     "scrapeOptions": {
#         "formats": ["markdown"],  # Add this - required
#         "onlyMainContent": True,
#         "blockAds": True, 
#         "removeBase64Images": True,
#         "excludeTags": ["nav", "header", "footer", "aside", ".sidebar", "#menu", "script", "style"]
#     }   
# }


coarse_schema = schemas.PageCoarseSummary.model_json_schema()  

payload = {
    "url": "https://vbotickets.helpdocsite.com/",
    "limit": 50,
    "crawlEntireDomain": True,
    "scrapeOptions": {
        # 2) Ask for BOTH markdown and your JSON format
        "formats": [
            "markdown",
            {
                "type": "json",  
                "schema": coarse_schema,
                "prompt": (
                    "Extract a PageCoarseSummary:\n"
                    "- features: distinct product capabilities on this page; "
                    "short name (1–6 words), and one concise evidence_snippet (<=200 chars) "
                    "taken verbatim from headers/bullets/labels.\n"
                    "- page_intent: one of product, docs, solutions, pricing, integration, "
                    "blog, legal, careers, press, other.\n"
                    "De-duplicate near-identical feature names; avoid marketing fluff."
                )
            }
        ],
        "onlyMainContent": True,
        "blockAds": True,
        "removeBase64Images": True,
        "excludeTags": ["nav", "header", "footer", "aside", ".sidebar", "#menu", "script", "style"]
        # tip: set "maxAge": 0 if you need to bypass the default 2-day cache
    }
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 1) start job
response = requests.post(FIRECRAWL_API, json=payload, headers=headers)
response.raise_for_status()
job = response.json()
job_url = job["url"] 
print("Started:", job_url)

# Check the scraping every 2 seconds
while True:
    s = requests.get(job_url, headers=headers, timeout=60)
    s.raise_for_status()
    status = s.json()             
    st = status.get("status", "")
    completed = status.get("completed") or status.get("pagesCrawled") or 0
    total = status.get("total") or status.get("limit") or "?"
    print(f"status={st} progress={completed}/{total}")
    if st.lower() in {"completed", "success", "succeeded", "done"}:
        break
    if st.lower() in {"failed", "error"}:
        raise RuntimeError(f"Crawl failed: {status}")
    time.sleep(2)

res = requests.get(job_url, headers=headers, timeout=120)
res.raise_for_status()
results = res.json()   

with open("vbotickets_crawl.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# quick signal if you likely hit the limit
count = len(results.get("data", [])) if isinstance(results, dict) else len(results)
print(f"Saved {count} pages to vbotickets_crawl.json")



# firecrawl = Firecrawl(api_key=API_KEY)
# docs = firecrawl.crawl(url="https://www.vbotickets.com/", limit=10)
# print(docs)

# Params to change
# limit: Default 10000
# crawlEntireDomain: Default: False


# """

# payload = { 
#     "url": "https://www.vbotickets.com/",
#     "limit": 10,                         
#     "crawlEntireDomain": True,
#     "scrapeOptions": {
#         "formats": [
#             "markdown",  # For markdown output
#             {
#                 "type": "json",
#                 "schema": {
#                     "type": "object",
#                     "properties": {
#                         "features": {
#                             "type": "array",
#                             "items": {
#                                 "type": "object",
#                                 "properties": {
#                                     "name": {"type": "string"},
#                                     "evidence_snippet": {"type": "string"}
#                                 },
#                                 "required": ["name"]
#                             }
#                         },
#                         "page_intent": {"type": "string"}
#                     }
#                 },
#                 "prompt": "Extract distinct capabilities and features mentioned on this page, along with the page intent."
#             }
#         ],
#         "onlyMainContent": True,
#         "blockAds": True, 
#         "removeBase64Images": True,
#         "excludeTags": ["nav", "header", "footer", "aside", ".sidebar", "#menu", "script", "style"]
#     }   
# }

# """
from firecrawl import Firecrawl
import os
import requests
import json
import time
from typing import List, Optional
from pydantic import BaseModel, Field
import schemas

#. See if if I can get all the data via markdown first

# Then run the gpt prompts on this

# Full job ran at once
API_KEY = os.environ.get("FIRECRAWL_API_KEY")

FIRECRAWL_API = "https://api.firecrawl.dev/v2/crawl" 
URLS = {"documentation" : "https://vbotickets.helpdocsite.com/", "home_page" : "https://www.vbotickets.com/"}
LIMIT = 500

# For polling errors for FireCrawl
max_retries = 12
retries = 0
delay = 1.5

for single_url_label, single_url in URLS.items():
    print("Running a full url crawl on: {}".format(single_url))
    # Form the payload for getting link graph
    payload = {
        "url": single_url,
        "limit": 500,
        "crawlEntireDomain": True,
        "scrapeOptions": {
            "formats": ["markdown"], 
            "onlyMainContent": True,
            "blockAds": True, 
            "removeBase64Images": True,
            "excludeTags": ["nav", "header", "footer", "aside", ".sidebar", "#menu", "script", "style"]
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
        try:
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
        except (requests.HTTPError) as e:
            print("Logged some http issue with job url")
            retries += 1
            if retries > max_retries:
                print("Errored")
                raise requests.HTTPError(f"Failed after {max_retries} retries")
            time.sleep(delay)
            delay = min(delay * 1.5, 8.0)
            # Try again
            continue
    # Might be some polling errors here
    tries = 0
    while True:
        res = requests.get(job_url, headers=headers, timeout=120)
        if res.status_code in {502, 503, 504}:
            print("Logged some http issue with job url")
            tries += 1
            if tries > 6:
                res.raise_for_status()  # give up
            time.sleep(0.8 * tries)
            continue
        res.raise_for_status()
        results = res.json()
        break
    # Pagination
    all_data = []
    page = results
    pagination_idx = 0
    while True:
        pagination_idx += 1
        print(f"{pagination_idx} is the pagination_idx")
        all_data.extend(page.get("data", []))
        nxt = page.get("next")
        if not nxt:
            break
        tries_p = 0
        while True:
            r = requests.get(nxt, headers=headers, timeout=120)
            if r.status_code in {502, 503, 504}:
                tries_p += 1
                if tries_p > 6:
                    r.raise_for_status()
                time.sleep(0.8 * tries_p)
                continue
            r.raise_for_status()
            page = r.json()
            break

    combined = {
        "success": results.get("success", True),
        "status": results.get("status"),
        "completed": results.get("completed"),
        "total": results.get("total"),
        "creditsUsed": results.get("creditsUsed"),
        "expiresAt": results.get("expiresAt"),
        "data": all_data,
    }

    with open(f"url_markdown_tree_for_{single_url_label}.json", "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)


    # with open(f"url_markdown_tree_for_{single_url_label}.json", "w", encoding="utf-8") as f:
    #     json.dump(results, f, indent=2, ensure_ascii=False)

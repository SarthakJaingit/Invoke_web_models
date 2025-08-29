from firecrawl import Firecrawl
import os
import requests
import json
import time
from typing import List, Optional
from pydantic import BaseModel, Field
import schemas
import re
import hashlib, unicodedata
from openai import OpenAI
from tqdm import tqdm


JSON_FILES = ["url_markdown_tree_for_home_page.json", "url_markdown_tree_for_documentation.json"]
API_KEY = os.environ.get("OPENAI_KEY")
client = OpenAI(api_key = API_KEY)



class PageBools_Prose(BaseModel):
    is_prose: bool = Field(..., 
        description="""
            Return `true` if the page text has at least some explanatory or descriptive content
            that could support making at least one Q&A pair. Examples include instructions,
            descriptions of features, explanations, or policies.

            Return `false` only if the page has essentially no usable content for Q&A —
            for example if it is only a list of links, bare headings, or pure marketing
            slogans without explanation.

            Answer strictly with a JSON boolean: `{"is_prose": true}` or `{"is_prose": false}`.
        """
        )

pageBool_schema = PageBools_Prose.model_json_schema()
pageBool_schema["additionalProperties"] = False
pageBool_schema["required"] = ["is_prose"] 


def classify(text: str) -> PageBools_Prose:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "PageBools",
                "schema": pageBool_schema,
                "strict": True
            }
        },
        temperature=0,
        max_tokens=120,
        messages=[
            {"role":"system","content":
             "Fill the schema using only information from the text. No extra keys."},
            {"role":"user","content": f"Classify for Q&A-ability.\nTEXT:\n{text}"}
        ],
    )
    raw = resp.choices[0].message.content
    return PageBools_Prose.model_validate_json(raw)

def prose_process(results, save_pth):
    # print(results["data"]["markdown"])
    out = []
    data = results["data"]
    for d in tqdm(data):
        curr_markdown = d["markdown"]
        classif_out = classify(curr_markdown)
        out.append({"markdown": curr_markdown, "is_prose": classif_out.is_prose})
        # Find out if curr_markdown has useful prose
    with open(f"{save_pth}.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    for json_pth in JSON_FILES:
        with open(json_pth, "r", encoding="utf-8") as f:
            results = json.load(f)
            prose_process(results, f"is_prose_{json_pth.split(".")[0]}")
        

    
    




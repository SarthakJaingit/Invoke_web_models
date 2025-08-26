import json
import re
import hashlib, unicodedata

with open("vbotickets_crawl.json", "r", encoding="utf-8") as f:
    results = json.load(f)

IMG_MD      = re.compile(r"!\[[^\]]*\]\([^)]*\)")                # ![alt](url)
LINK_MD     = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")             # [anchor](url)
EMPTY_LINK  = re.compile(r"\[\]\([^)]*\)")                       # [](url)
BARE_URL    = re.compile(r"https?://\S+")
HEADING     = re.compile(r"^\s{0,3}#{1,6}\s+", re.M)             # markdown headings
BULLET_MD   = re.compile(r"^\s*[-*+]\s+", re.M)
H_RULE      = re.compile(r"^\s*[*_]{3,}\s*$", re.M)              # *** or ___
MULTI_NL    = re.compile(r"\n{3,}")
NBSP        = "\xa0"


def normalize_unicode(s: str) -> str:
    s = unicodedata.normalize("NFKC", s.replace(NBSP, " "))
    s = (s.replace("’", "'").replace("“", '"').replace("”", '"')
           .replace("–", "-").replace("—", "-"))
    return s

def clean_markdown(md: str, keep_urls: bool = False) -> str:
    md = normalize_unicode(md or "")
    print(md)
    assert 1 == 2

    md = IMG_MD.sub("", md)
    # keep anchor text; drop URLs (training on prose)
    def _sub_link(m): return f"{m.group(1)} ({m.group(2)})" if keep_urls else m.group(1)
    md = LINK_MD.sub(_sub_link, md)
    md = EMPTY_LINK.sub("", md)
    if not keep_urls:
        md = BARE_URL.sub("", md)
    # strip heading hashes but keep heading text
    md = HEADING.sub("", md)
    # normalize bullets and rules
    md = BULLET_MD.sub("- ", md)
    md = H_RULE.sub("", md)
    # collapse whitespace
    md = MULTI_NL.sub("\n\n", md).strip()
    # dedupe consecutive identical lines (common on homepages)
    out = []
    for ln in md.splitlines():
        ln = ln.strip()
        if not ln:
            if out and out[-1] != "": out.append("")
            continue
        if not out or ln != out[-1]:
            out.append(ln)
    return "\n".join(out).strip()

def preprocess_data(results):
    num_of_queries = len(results["data"])
    for n in range(num_of_queries):
        blob = results["data"][n]["markdown"]
        blob = clean_markdown(blob)
        print(blob)
        assert 1 == 2


if __name__ == "__main__":
    preprocess_data(results)
    
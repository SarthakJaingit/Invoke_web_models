from typing import List, Optional
from pydantic import BaseModel, Field

# Maybe try more simple schemas

class CoarseFeature(BaseModel):
    name: str = Field(
        ...,
        description=(
            "Short, specific feature or capability name (1–6 words). "
            "Examples: 'Usage Analytics', 'SAML SSO', 'Salesforce Sync', 'AI Assistant'. "
            "Avoid marketing phrases and benefits; return the capability label itself."
        )
    )
    evidence_snippet: Optional[str] = Field(
        None,
        description=(
            "A short, verbatim snippet (≤ 200 chars) from the page that supports the feature. "
            "Prefer bullets, H2/H3 lines, or button/label text."
        )
    )

class PageCoarseSummary(BaseModel):
    features: List[CoarseFeature] = Field(
        default_factory=list,
        description=(
            "Distinct capabilities explicitly mentioned on this page. "
            "De-duplicate near-identical names; prefer the most specific phrasing."
        )
    )
    page_intent: Optional[str] = Field(
        None,
        description=(
            "One of: 'product','docs','solutions','pricing','integration','blog','legal','careers','press','other'. "
            "Infer from headings and URL."
        )
    )

class PageBools(BaseModel):
    haveFeature : bool = Field(
        ...,
        description = (
            "Does this page talk about a specific feature you can do with this companies product"
        )
    )
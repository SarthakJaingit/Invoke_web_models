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


# Q and A pydantic structure

class QAPair(BaseModel):
    question: str = Field(..., description="A user-style question about the product or feature described on the page.")
    answer: str = Field(..., description="A direct, grounded answer based on the page content.")
    category: Optional[str] = Field(None, description="Optional tag: e.g. pricing, usage, limitations, setup.")
    source_snippet: Optional[str] = Field(None, description="The exact or summarized snippet the answer is based on.")
    # paraphrases: Optional[List[str]] = Field(None, description="Alternative phrasings of the same question.")

class PageQA(BaseModel):
    url: str = Field(..., description="The URL of the page being processed.")
    title: str = Field(..., description="The title or topic of the page.")
    faqs: List[QAPair] = Field(..., description="List of rich question-answer pairs extracted from this page.")

# Advanced Q and A pydantic structure

# class QAVariant(BaseModel):
#     question: str = Field(..., description="A different but somewhat related version of the main question.")
#     answer: str = Field(..., description="A direct, grounded answer based on the page content.")
#     source_snippet: Optional[str] = Field(None, description="The exact snippet the answer is based on.")

# class QAPair(BaseModel):
#     question: str = Field(..., description="A user-style question about the product or feature described on the page.")
#     answer: str = Field(..., description="A direct, grounded answer based on the page content.")
#     category: Optional[str] = Field(None, description="Optional tag: e.g. pricing, usage, limitations, setup.")
#     source_snippet: Optional[str] = Field(None, description="The exact snippet the answer is based on.")
#     variants: List[QAVariant] = Field(..., description="List of Q&A variants based on the canonical question.")

# class PageQA(BaseModel):
#     url: str = Field(..., description="The URL of the page being processed.")
#     title: str = Field(..., description="The title or topic of the page.")
#     faqs: List[QAPair] = Field(..., description="List of rich question-answer pairs extracted from this page.")

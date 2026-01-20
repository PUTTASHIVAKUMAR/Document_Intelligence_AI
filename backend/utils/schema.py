from pydantic import BaseModel
from typing import List, Optional

class SearchResponse(BaseModel):
    query: str
    answer: str
    sources: Optional[List[str]] = None

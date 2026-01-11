from pydantic import BaseModel
from typing import List, Optional


class ModelStats(BaseModel):
    model: str
    count: int
    avg_electric_range: float


class ModelsByMakeResponse(BaseModel):
    make: str
    models: List[ModelStats]
    most_popular_model: Optional[str]

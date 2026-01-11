from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class ModelYearRange(BaseModel):
    start: int
    end: int


class AnalyzeFilters(BaseModel):
    makes: Optional[List[str]] = None
    model_years: Optional[ModelYearRange] = None
    min_electric_range: Optional[int] = None
    vehicle_type: Optional[Literal["BEV", "PHEV"]] = None


class AnalyzeRequest(BaseModel):
    filters: Optional[AnalyzeFilters] = None
    group_by: Literal["county", "make", "model_year"]


class AnalyzeGroupResult(BaseModel):
    group: str
    count: int
    avg_electric_range: float
    most_common_vehicle: str


class AnalyzeResponse(BaseModel):
    results: List[AnalyzeGroupResult]

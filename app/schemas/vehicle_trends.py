from pydantic import BaseModel
from typing import List


class YearlyTrend(BaseModel):
    model_year: int
    total_count: int
    avg_electric_range: float
    bev_count: int
    phev_count: int


class VehicleTrendsResponse(BaseModel):
    trends: List[YearlyTrend]

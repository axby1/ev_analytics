from pydantic import BaseModel
from typing import Dict, List,Optional


class MakeCount(BaseModel):
    make: str
    count: int


class CAFVEligibility(BaseModel):
    eligible: int
    ineligible: int


class VehicleSummaryResponse(BaseModel):
    total_vehicles: int
    vehicles_by_type: Dict[str, int]
    top_makes: List[MakeCount]
    average_electric_range: float
    cafv_eligibility: CAFVEligibility


class Vehicle(BaseModel):
    vin: Optional[str]
    county: str
    state: str
    make: str
    model: str
    model_year: int
    vehicle_type: str
    electric_range: int
    cafv_eligible: bool


class PaginatedVehiclesResponse(BaseModel):
    total: int
    page: int
    page_size: int
    results: List[Vehicle]
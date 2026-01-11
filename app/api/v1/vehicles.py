from fastapi import APIRouter, Query, Path, HTTPException

from app.schemas.vehicle_summary import VehicleSummaryResponse,PaginatedVehiclesResponse
from app.schemas.models_by_make import ModelsByMakeResponse
from app.schemas.vehicle_trends import VehicleTrendsResponse
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.services.aggregations import (
    total_vehicles,
    vehicles_by_type,
    top_makes,
    average_electric_range,
    cafv_eligibility_counts,
    vehicles_by_county,
    models_by_make,
    vehicle_trends_by_year,
    analyze_vehicles,
)

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("/summary", response_model=VehicleSummaryResponse)
def get_vehicle_summary():
    return {
        "total_vehicles": total_vehicles(),
        "vehicles_by_type": vehicles_by_type(),
        "top_makes": top_makes(),
        "average_electric_range": average_electric_range(),
        "cafv_eligibility": cafv_eligibility_counts(),
    }


@router.get(
    "/county/{county_name}",
    response_model=PaginatedVehiclesResponse
)
def get_vehicles_by_county(
    county_name: str = Path(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    model_year: int | None = Query(None),
    sort_by: str = Query("model_year"),
    sort_order: str = Query("asc"),
):
    try:
        return vehicles_by_county(
            county=county_name,
            page=page,
            page_size=page_size,
            model_year=model_year,
            sort_by=sort_by,
            sort_order=sort_order,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    


@router.get(
    "/make/{make}/models",
    response_model=ModelsByMakeResponse
)
def get_models_by_make(make: str):
    return models_by_make(make)


@router.get(
    "/trends",
    response_model=VehicleTrendsResponse
)
def get_vehicle_trends():
    return {
        "trends": vehicle_trends_by_year()
    }


@router.post(
    "/analyze",
    response_model=AnalyzeResponse
)
def analyze_endpoint(payload: AnalyzeRequest):
    return {
        "results": analyze_vehicles(payload)
    }
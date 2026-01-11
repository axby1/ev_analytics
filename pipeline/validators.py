# row-level CSV validation and normalization.

def normalize_str(value: str|None) -> str|None:
    if not value:
        return None
    
    return value.strip().upper()


def parse_int(value: str | None) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def validate_and_transform(row: dict) -> dict | None:
    vin = normalize_str(row.get("VIN (1-10)"))
    make = normalize_str(row.get("Make"))
    model = normalize_str(row.get("Model"))
    model_year = parse_int(row.get("Model Year"))

    if not vin or not make or not model or not model_year:
        return None

    electric_range = parse_int(row.get("Electric Range"))

    return {
        "vin": vin,
        "county": normalize_str(row.get("County")),
        "state": normalize_str(row.get("State")),
        "make": make,
        "model": model,
        "model_year": model_year,
        "vehicle_type": normalize_str(row.get("Electric Vehicle Type")),
        "electric_range": electric_range,
        "cafv_eligible": normalize_str(
            row.get("Clean Alternative Fuel Vehicle (CAFV) Eligibility")
            ) == "CLEAN ALTERNATIVE FUEL VEHICLE ELIGIBLE"

    }



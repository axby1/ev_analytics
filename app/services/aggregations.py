#API route  →  Service / Aggregation  →  MongoDB
#middle layer


from app.db import vehicle_collection


def total_vehicles() -> int:
    return vehicle_collection.count_documents({})


def vehicles_by_type() -> dict:
    pipeline = [
        {
            "$group": {
                "_id": "$vehicle_type",
                "count": {"$sum": 1}
            }
        }
    ]

    result = vehicle_collection.aggregate(pipeline)

    out = {}
    for doc in result:
        key = doc["_id"] or "UNKNOWN"
        out[key] = doc["count"]

    return out


def top_makes(limit: int = 10) -> list[dict]:
    pipeline = [
        {
            "$group": {
                "_id": "$make",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]

    result = vehicle_collection.aggregate(pipeline)

    return [
        {"make": doc["_id"], "count": doc["count"]}
        for doc in result
    ]


def average_electric_range() -> float:
    pipeline = [
        {
            "$group": {
                "_id": None,
                "avg_range": {"$avg": "$electric_range"}
            }
        }
    ]

    result = list(vehicle_collection.aggregate(pipeline))

    if not result:
        return 0.0

    return round(result[0]["avg_range"], 2)



def average_bev_range() -> float:
    pipeline = [
        {
            "$match": {
                "vehicle_type": "BATTERY ELECTRIC VEHICLE (BEV)"
            }
        },
        {
            "$group": {
                "_id": None,
                "avg_range": {"$avg": "$electric_range"}
            }
        }
    ]

    result = list(vehicle_collection.aggregate(pipeline))

    if not result:
        return 0.0

    return round(result[0]["avg_range"], 2)



def cafv_eligibility_counts() -> dict:
    pipeline = [
        {
            "$group": {
                "_id": "$cafv_eligible",
                "count": {"$sum": 1}
            }
        }
    ]

    result = vehicle_collection.aggregate(pipeline)

    out = {
        "eligible": 0,
        "ineligible": 0
    }

    for doc in result:
        if doc["_id"] is True:
            out["eligible"] = doc["count"]
        else:
            out["ineligible"] = doc["count"]

    return out



def vehicles_by_county(
    county: str,
    page: int = 1,
    page_size: int = 20,
    model_year: int | None = None,
    sort_by: str = "model_year",
    sort_order: str = "asc",
):
    query = {"county": county.upper()}

    if model_year is not None:
        query["model_year"] = model_year

    sort_fields = {
        "model_year": "model_year",
        "make": "make",
        "model": "model",
    }

    if sort_by not in sort_fields:
        raise ValueError("Invalid sort field")

    direction = 1 if sort_order == "asc" else -1

    cursor = (
        vehicle_collection
        .find(query, {"_id": 0})
        .sort(sort_fields[sort_by], direction)
        .skip((page - 1) * page_size)
        .limit(page_size)
    )

    results = list(cursor)
    total = vehicle_collection.count_documents(query)

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "results": results,
    }


def models_by_make(make: str):
    pipeline = [
        {
            "$match": {
                "make": make.upper()
            }
        },
        {
            "$group": {
                "_id": "$model",
                "count": {"$sum": 1},
                "avg_electric_range": {"$avg": "$electric_range"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "model": "$_id",
                "count": 1,
                "avg_electric_range": {"$round": ["$avg_electric_range", 2]}
            }
        },
        {
            "$sort": {
                "count": -1
            }
        }
    ]

    results = list(vehicle_collection.aggregate(pipeline))

    if not results:
        return {
            "make": make.upper(),
            "models": [],
            "most_popular_model": None,
        }

    most_popular = results[0]["model"]

    return {
        "make": make.upper(),
        "models": results,
        "most_popular_model": most_popular,
    }


def vehicle_trends_by_year():
    pipeline = [
        {
            "$group": {
                "_id": "$model_year",
                "total_count": {"$sum": 1},
                "avg_electric_range": {"$avg": "$electric_range"},
                "bev_count": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$vehicle_type", "BATTERY ELECTRIC VEHICLE (BEV)"]},
                            1,
                            0,
                        ]
                    }
                },
                "phev_count": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$vehicle_type", "PLUG-IN HYBRID ELECTRIC VEHICLE (PHEV)"]},
                            1,
                            0,
                        ]
                    }
                },
            }
        },
        {
            "$project": {
                "_id": 0,
                "model_year": "$_id",
                "total_count": 1,
                "avg_electric_range": {"$round": ["$avg_electric_range", 2]},
                "bev_count": 1,
                "phev_count": 1,
            }
        },
        {
            "$sort": {"model_year": 1}
        }
    ]

    return list(vehicle_collection.aggregate(pipeline))



def analyze_vehicles(request):
    match = {}

    filters = request.filters
    if filters:
        if filters.makes:
            match["make"] = {"$in": [m.upper() for m in filters.makes]}

        if filters.model_years:
            match["model_year"] = {
                "$gte": filters.model_years.start,
                "$lte": filters.model_years.end,
            }

        if filters.min_electric_range is not None:
            match["electric_range"] = {"$gte": filters.min_electric_range}

        if filters.vehicle_type:
            if filters.vehicle_type == "BEV":
                match["vehicle_type"] = "BATTERY ELECTRIC VEHICLE (BEV)"
            else:
                match["vehicle_type"] = "PLUG-IN HYBRID ELECTRIC VEHICLE (PHEV)"

    group_field_map = {
        "county": "$county",
        "make": "$make",
        "model_year": "$model_year",
    }

    group_field = group_field_map[request.group_by]

    pipeline = []

    if match:
        pipeline.append({"$match": match})

    pipeline.extend([
        {
            "$group": {
                "_id": {
                    "group": group_field,
                    "model": "$model",
                },
                "count": {"$sum": 1},
                "avg_electric_range": {"$avg": "$electric_range"},
            }
        },
        {
            "$group": {
                "_id": "$_id.group",
                "count": {"$sum": "$count"},
                "avg_electric_range": {"$avg": "$avg_electric_range"},
                "models": {
                    "$push": {
                        "model": "$_id.model",
                        "count": "$count",
                    }
                },
            }
        },
        {
            "$project": {
                "_id": 0,
                "group": "$_id",
                "count": 1,
                "avg_electric_range": {"$round": ["$avg_electric_range", 2]},
                "most_common_vehicle": {
                    "$arrayElemAt": [
                        {
                            "$map": {
                                "input": {
                                    "$slice": [
                                        {
                                            "$sortArray": {
                                                "input": "$models",
                                                "sortBy": {"count": -1},
                                            }
                                        },
                                        1,
                                    ]
                                },
                                "as": "m",
                                "in": "$$m.model",
                            }
                        },
                        0,
                    ]
                },
            }
        },
        {
            "$sort": {"count": -1}
        },
    ])

    return list(vehicle_collection.aggregate(pipeline))

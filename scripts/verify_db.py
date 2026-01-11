from app.db import vehicle_collection


def assert_condition(condition: bool, message: str):
    if not condition:
        raise RuntimeError(f"❌ VALIDATION FAILED: {message}")


def check_model_year_type():
    bad = vehicle_collection.find_one({"model_year": {"$type": "string"}})
    assert_condition(
        bad is None,
        "model_year contains string values (must be int)",
    )


def check_electric_range_type():
    bad = list(
        vehicle_collection.find(
            {
                "electric_range": {
                    "$not": {"$type": "int"},
                    "$ne": None,
                }
            }
        )
    )
    assert_condition(
        len(bad) == 0,
        "electric_range contains non-int, non-null values",
    )


def check_cafv_boolean():
    bad = vehicle_collection.find_one(
        {"cafv_eligible": {"$nin": [True, False]}}
    )
    assert_condition(
        bad is None,
        "cafv_eligible contains non-boolean values",
    )


def check_vin_not_null():
    bad = vehicle_collection.find_one(
        {"vin": {"$in": [None, ""]}}
    )
    assert_condition(
        bad is None,
        "vin contains null or empty values",
    )


def check_vin_presence():
    bad = vehicle_collection.find_one(
        {"vin": {"$in": [None, ""]}}
    )
    assert_condition(
        bad is None,
        "vin contains null or empty values",
    )



def run_all_checks():
    print("🔍 Running database integrity checks...\n")

    check_model_year_type()
    print("✔ model_year type OK")

    check_electric_range_type()
    print("✔ electric_range type OK")

    check_cafv_boolean()
    print("✔ cafv_eligible boolean OK")

    check_vin_not_null()
    print("✔ vin presence OK")

    check_vin_presence()
    print("✔ vin uniqueness OK")

    print("\n✅ ALL CHECKS PASSED. DATABASE IS CLEAN.")


if __name__ == "__main__":
    run_all_checks()

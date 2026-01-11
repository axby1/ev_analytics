# Electric Vehicle Analytics API

A FastAPI-based backend service for ingesting, validating, storing, and analyzing electric vehicle (EV) registration data using MongoDB.
The application exposes multiple analytical APIs to query summaries, trends, and custom aggregations over a large real-world dataset.

---

## Tech Stack

* **Language**: Python 3.11
* **Framework**: FastAPI
* **Database**: MongoDB
* **Driver**: PyMongo
* **Data Processing**: CSV, aggregation pipelines
* **Validation**: Custom row-level validation + Pydantic schemas
* **Server**: Uvicorn

---

## Project Scope

This project covers:

* CSV ingestion with strict validation and normalization
* MongoDB schema design and indexing
* Aggregation-heavy analytics endpoints
* Pagination, filtering, and sorting
* Clean API contracts with OpenAPI documentation

---

## Environment Setup

### Prerequisites

* Python 3.11+
* MongoDB running locally or remotely

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```
MONGO_URI= your mongoDB URL
MONGO_DB=ev_analytics
MONGO_COLLECTION=vehicles
```

---

## Data Ingestion

The dataset is ingested via a standalone pipeline script.

### Validation rules

* Required fields: VIN, Make, Model, Model Year
* String normalization (trim + uppercase)
* Integer parsing with safe fallbacks
* CAFV eligibility mapped to boolean
* Invalid rows are dropped explicitly

### Run ingestion from root

```bash
python -m pipeline.ingest_csv ev_dataset.csv
```

After ingestion:

* All records are normalized
* Indexes are created
* Invalid rows are excluded
* Duplicate VINs are prevented via indexing

---

## Database Integrity Check

A verification script ensures the DB schema is consistent after ingestion.

```bash
python scripts/verify_db.py
```

Checks include:

* Correct data types
* Boolean integrity
* VIN presence and uniqueness
* Expected field structure

---

## Running the API

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```
http://localhost:8000/docs
```

---

## API Endpoints

### 1. Vehicle Summary

```
GET /api/v1/vehicles/summary
```

Returns:

* Total number of vehicles
* Count by vehicle type (BEV / PHEV)
* Top 10 manufacturers
* Average electric range
* CAFV eligible vs ineligible counts

---

### 2. Vehicles by County

```
GET /api/v1/vehicles/county/{county_name}
```

Query params:

* `page` (default: 1)
* `page_size` (default: 20)
* `model_year` (optional)
* `sort_by` (model_year | make | model)

---

### 3. Models by Manufacturer

```
GET /api/v1/vehicles/make/{make}/models
```

Returns:

* Count per model
* Average electric range per model
* Most popular model

---

### 4. Trends Over Time

```
GET /api/v1/vehicles/trends
```

Returns:

* Vehicle count by model year
* Average electric range by year
* BEV vs PHEV ratio per year

---

### 5. Custom Analysis

```
POST /api/v1/vehicles/analyze
```

Example payload:

```json
{
  "filters": {
    "makes": ["TESLA"],
    "model_years": { "start": 2019, "end": 2024 },
    "min_electric_range": 150,
    "vehicle_type": "BEV"
  },
  "group_by": "county"
}
```

Returns:

* Grouped counts
* Average electric range per group
* Most common vehicle per group

---

## Design Decisions

* MongoDB aggregation pipelines are used instead of application-side processing
* Validation is done at ingestion time to keep query logic clean
* API responses are schema-controlled using Pydantic

---

## Limitations & Future Work

* Can add frontend UI for better visualization 
* Bulk ingestion is synchronous (can be offloaded to background jobs)
* Caching and performance profiling can be added for high-traffic scenarios

---




import csv
from pathlib import Path
from tqdm import tqdm

from app.db import vehicle_collection, create_indexes
from pipeline.validators import validate_and_transform


BATCH_SIZE = 2000


def ingest_csv(csv_path: str):
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(csv_path)

    batch = []
    inserted = 0
    dropped = 0

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in tqdm(reader):
            doc = validate_and_transform(row)
            if not doc:
                dropped += 1
                continue

            batch.append(doc)

            if len(batch) >= BATCH_SIZE:
                vehicle_collection.insert_many(batch)
                inserted += len(batch)
                batch.clear()

        if batch:
            vehicle_collection.insert_many(batch)
            inserted += len(batch)

    create_indexes()

    print(f"Inserted: {inserted}")
    print(f"Dropped: {dropped}")


#script to ingest data into mongodb
# run this from root: python -m pipeline.ingest_csv ev_dataset.csv

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m pipeline.ingest_csv <csv_path>")
        sys.exit(1)

    csv_path = sys.argv[1]
    ingest_csv(csv_path)

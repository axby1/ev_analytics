# Mongo connection + indexes only
from pymongo import MongoClient, ASCENDING
from app.config import settings

client = MongoClient(settings.mongo_uri)
db = client[settings.mongo_db]
vehicle_collection = db[settings.mongo_collection]

def create_indexes():
    vehicle_collection.create_index([("county", ASCENDING)])
    vehicle_collection.create_index([("make", ASCENDING)])
    vehicle_collection.create_index([("model", ASCENDING)])
    vehicle_collection.create_index([("model_year", ASCENDING)])
    vehicle_collection.create_index([("vehicle_type", ASCENDING)])
    vehicle_collection.create_index([("electric_range", ASCENDING)])
    vehicle_collection.create_index([("make", ASCENDING),("model",ASCENDING)])
    vehicle_collection.create_index([("model_year", ASCENDING),("vehicle_type",ASCENDING)])
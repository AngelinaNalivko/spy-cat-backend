from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.spycat_db
spycat_collection = db.get_collection("spycats")
mission_collection = db.get_collection("missions")
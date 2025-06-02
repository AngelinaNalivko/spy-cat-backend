from fastapi import APIRouter, HTTPException
from database import spycat_collection
from bson.objectid import ObjectId

from services.spycatapi import breed_validation
from models.spycat import SpycatCreate, SpycatUpdate, SpycatDB

router = APIRouter()

# Create a spy cat
@router.post("/spycats", response_model=SpycatDB)
async def create_spycat(spycat: SpycatCreate):
    if not breed_validation(spycat.breed):
        raise HTTPException(status_code=400, detail="Breed is not valid")
    new_spycat = spycat.model_dump()
    result = await spycat_collection.insert_one(new_spycat)
    new_spycat["id"] = str(result.inserted_id)
    return SpycatDB(**new_spycat)

# Remove a spy cat
@router.delete("/spycats/{id}")
async def delete_spycat(id: str):
    result = await spycat_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Spycat not found")
    return {"message": "Spycat was deleted"}

# Update a spy cat's salary
@router.patch("/spycats/{id}", response_model=SpycatDB)
async def update_salary(id: str, spycat_update: SpycatUpdate):
    result = await spycat_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"salary": spycat_update.salary}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Spycat not found or no changes made")
    spycat = await spycat_collection.find_one({"_id": ObjectId(id)})
    spycat["id"] = str(spycat["_id"])
    return SpycatDB(**spycat)

# List spy cats
@router.get("/spycats", response_model=list[SpycatDB])
async def get_all_spycats():
    spycats = []
    async for spycat in spycat_collection.find():
        spycat["id"] = str(spycat["_id"])
        spycats.append(SpycatDB(**spycat))
    return spycats

# Get a single spy cat
@router.get("/spycats/{id}", response_model=SpycatDB)
async def get_spycat(id: str):
    spycat = await spycat_collection.find_one({"_id": ObjectId(id)})
    if not spycat:
        raise HTTPException(status_code=404, detail="Spycat not found")
    spycat["id"] = str(spycat["_id"])
    return SpycatDB(**spycat)

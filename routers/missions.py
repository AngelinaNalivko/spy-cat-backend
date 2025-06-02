from fastapi import APIRouter, HTTPException
from database import mission_collection
from bson.objectid import ObjectId

from models.mission import MissionCreate, TargetUpdate, MissionDB

router = APIRouter()

# Create a mission, checking if it has 1 to 3 targets
@router.post("/missions", response_model=MissionDB)
async def create_mission(mission: MissionCreate):
    if len(mission.targets) < 1 or len(mission.targets) > 3:
        raise HTTPException(status_code=400, detail="A mission must have 1 to 3 targets")
    
    targets_with_index = [
        {**target.model_dump(), "target_index": i}
        for i, target in enumerate(mission.targets)
    ]

    new_mission = mission.model_dump()
    new_mission["targets"] = targets_with_index
    result = await mission_collection.insert_one(new_mission)
    new_mission["id"] = str(result.inserted_id)
    return MissionDB(**new_mission)

# Remove a mission, check if assigned to a spy cat
@router.delete("/missions/{id}")
async def delete_mission(id: str):
    mission = await mission_collection.find_one({"_id": ObjectId(id)})
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    # Check if the mission is assigned to a spy cat
    if mission.get("cat_id"):
        raise HTTPException(status_code=400, detail="Mission is assigned to a spy cat and cannot be deleted")

    result = await mission_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    return {"message": "Mission was deleted"}

# List all missions
@router.get("/missions", response_model=list[MissionDB])
async def get_all_missions():
    missions = []
    async for mission in mission_collection.find():
        mission["id"] = str(mission["_id"])
        missions.append(MissionDB(**mission))
    return missions

# Get a single mission
@router.get("/missions/{id}", response_model=MissionDB)
async def get_mission(id: str):
    mission = await mission_collection.find_one({"_id": ObjectId(id)})
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    mission["id"] = str(mission["_id"])
    return MissionDB(**mission)

# Assign a cat to a mission
@router.patch("/missions/{id}/assign")
async def assign_cat_to_mission(id: str, cat_id: str):
    mission = await mission_collection.find_one({"_id": ObjectId(id)})
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    # Check if the mission already has a cat assigned
    if mission.get("cat_id"):
        raise HTTPException(status_code=400, detail="The mission is already assigned to another cat")

    # Check if the cat has an active mission
    existing_active_mission = await mission_collection.find_one({
        "cat_id": cat_id,
        "mission_is_completed": False
    })

    if existing_active_mission:
        raise HTTPException(status_code=400, detail="The cat is already assigned to an active mission")

    await mission_collection.update_one({"_id": ObjectId(id)}, {"$set": {"cat_id": cat_id}})
    return {"message": "Cat assigned to mission"}

# Update a target's completion status or notes
@router.patch("/missions/{id}/targets/{target_index}", response_model=MissionDB)
async def update_target(id: str, target_index: int, target_update: TargetUpdate):
    mission = await mission_collection.find_one({"_id": ObjectId(id)})
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    if mission.get("mission_is_completed", False):
        raise HTTPException(status_code=400, detail="Mission is already completed")
    
    try:
        target = mission["targets"][target_index]
    except IndexError:
        raise HTTPException(status_code=404, detail="Target not found")

    if target.get("target_is_completed"):
        raise HTTPException(status_code=400, detail="Target is already completed")
    
    if target_update.notes is not None:
        target["notes"] = target_update.notes

    if target_update.is_completed is True:
        target["target_is_completed"] = True

    # Check if all targets are completed
    if all(t["target_is_completed"] for t in mission["targets"]):
        mission["mission_is_completed"] = True

    mission["targets"][target_index] = target
    await mission_collection.update_one({"_id": ObjectId(id)}, {"$set": mission})
    mission["id"] = str(mission["_id"])
    return MissionDB(**mission)
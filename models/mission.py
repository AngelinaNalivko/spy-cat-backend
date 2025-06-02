from pydantic import BaseModel
from typing import Optional, List

class Target(BaseModel):
    target_index: Optional[int] = None
    name: str
    country: str
    notes: str = "No notes"
    target_is_completed: bool = False

class MissionCreate(BaseModel):
    cat_id: Optional[str] = None
    targets: List[Target]
    mission_is_completed: bool = False

class TargetUpdate(BaseModel):
    is_completed: Optional[bool] = None
    notes: Optional[str] = None

class MissionDB(MissionCreate): 
    id: str

from pydantic import BaseModel

class Spycat(BaseModel):
    name: str
    years_of_experience: int
    breed: str
    salary: float

class SpycatCreate(Spycat):
    pass

class SpycatUpdate(BaseModel):
    salary: float

class SpycatDB(Spycat):
    id: str
    
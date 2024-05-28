from pydantic import BaseModel, field_validator

class Pokemon(BaseModel):
    id: int
    name: str
    height: float
    weight: float
    type: list[str]

    @field_validator("id")
    def validate_id(cls, value):
        if value < 0:
            raise ValueError("pokemon id must be a positive integer")
        return value
    
    @field_validator("height")
    def validate_height(cls, value):
        if value < 0 :
            raise ValueError("pokemon height must be a positive float")
        return value
    
    @field_validator("weight")
    def validate_weight(cls, value):
        if value < 0 :
            raise ValueError("pokemon weight must be a positive float")
        return value
from typing import Optional
from pydantic import BaseModel, Field

class MQTTSLogginSchema(BaseModel):
    topic: str = Field(...)
    msg: object = Field(...)
    event: str = Field(...)

class MQTTPayloadSchema(BaseModel):
    date: str = Field(...)
    height: float = Field(...)
    object: object = Field(...)

class MatlabDataSchema(BaseModel):
    day: str = Field(...)
    height_s1: float = Field(...)
    discharge_s1: float = Field(...)
    discharge_s2: float = Field(...)
    discharge_s3: float = Field(...)
    height_s3: float = Field(...)

class MatlabHeightRequestSchema(BaseModel):
    day: str = Field(...)
    height_s3: float = Field(...)

class MatlabPredictFurtureSchema(BaseModel):
    day: str = Field(...)
    discharge_s1: float = Field(...)
    height_s1: float = Field(...)

class MatlabPredictRawSchema(BaseModel):
    day: str = Field(...)
    discharge_s1: float = Field(...)



def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
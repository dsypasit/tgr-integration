from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from typing import List
from pydantic import BaseModel 

from server.database import (
    add_matlab_predict_future,
    update_matlab_predict_raw_data,
    add_height3_rawdata,
    get_height,
    add_matlab_rawdata,
    get_raw_data,
    get_predict_furture
)

class MatlabDataSchema(BaseModel):
    day: int 
    height_s1: float 
    discharge_s1: float 
    discharge_s2: float 
    discharge_s3: float 
    height_s3: float | None = 0

class MatlabHeightRequestSchema(BaseModel):
    day: int 
    height_s3: float 

class MatlabPredictFurtureSchema(BaseModel):
    day: int
    discharge_s1: float 
    height_s1: float

class MatlabPredictRawSchema(BaseModel):
    day: int
    discharge_s1: float 

class MatlabReq(BaseModel):
    items: List[MatlabDataSchema]

router = APIRouter()

@router.get('/get_height')
async def get_height_from_iot():
    height = await get_height()
    return height

@router.get('/rawdata')
async def get_height_from_iot():
    raw_data = await get_raw_data()
    return raw_data

@router.post('/rawdata')
async def add_raw_data(body: List[ MatlabDataSchema ]):
    data = jsonable_encoder(body)
    await add_matlab_rawdata(data)
    return 'add raw data'

@router.patch('/rawdata/height3')
async def add_height3(body: List[ MatlabHeightRequestSchema ]):
    data = jsonable_encoder(body)
    await add_height3_rawdata(data)
    return 'update height'

@router.patch('/rawdata/predict')
async def predict_rawdata(body: List[ MatlabPredictRawSchema ]):
    data = jsonable_encoder(body)
    await update_matlab_predict_raw_data(data)
    return 'update predict raw data'

@router.get('/predict') 
async def get_predict():
    raw_data = await get_predict_furture()
    return raw_data
    
@router.post('/predict')
async def create_future_predict(body: List[ MatlabPredictFurtureSchema ]):
    data = jsonable_encoder(body)
    await add_matlab_predict_future(data)
    return 'insert furture data success'
from fastapi import APIRouter
from server.mqtt.sensor_data import fast_mqtt
import json

router = APIRouter()

@router.get("/take_img", response_description="take picture from iot")
async def take_picture():
    await fast_mqtt.push
    payload = {
        'ID': 21,
        'CMD': 'TAKE_PIC_WEB',
        'event': 'TAKE_PIC_WEB'
    }
    payload_json = json.dumps(payload)
    fast_mqtt.publish("/tgr2023/LittleBoy/cmd", payload_json) #publishing mqtt topic
    return {"result": True,"message":"take picture success" }
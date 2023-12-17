from fastapi import FastAPI
from server.routes.iot import router as IotRouter
from server.routes.matlab import router as MatlabRouter
from server.mqtt.sensor_data import router as MqttRouter

app = FastAPI()

####router api part

app.include_router(MqttRouter, tags=["MQTT"],prefix="/mqtt")
app.include_router(MatlabRouter, tags=["Matlab"],prefix="/matlab")
app.include_router(IotRouter, tags=["iot"], prefix="/iot")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "My REST API server!"}

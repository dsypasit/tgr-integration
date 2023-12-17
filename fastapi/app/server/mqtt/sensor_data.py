from fastapi import APIRouter 
#fastapi_mqtt
from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi_mqtt.config import MQTTConfig
import json
from server.database import add_mqtt_logging, add_mqtt_water_level
from datetime import datetime

mqtt_config = MQTTConfig(host = "192.168.1.2",
    port= 1883,
    keepalive = 60,
    username="TGR_GROUP21",
    password="CY985F")

fast_mqtt = FastMQTT(config=mqtt_config)

router = APIRouter()

fast_mqtt.init_app(router)

@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    fast_mqtt.client.subscribe("/mqtt") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@fast_mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)

@fast_mqtt.subscribe("tgr2023/LittleBoy/evt")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)
    message = json.loads(payload.decode())
    if message['height'] == None:
        return
    try:
        msg_payload = dict(
            date = datetime.now().strftime(r'%d/%m/%Y %H:%M:%S'),
            height = float(message['height']),
        )
        msg_logging = dict(
            date = datetime.now().strftime(r'%d/%m/%Y %H:%M:%S'),
            topic = topic,
            msg = message,
            event = 'READ_WTL'
        )
        print(msg_payload)
        print(msg_logging)
        await add_mqtt_logging(msg_logging)
        await add_mqtt_water_level(msg_payload)
    except:
        pass

@fast_mqtt.subscribe("tgr2023/LittleBoy/cmd")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)
    try:
        message = json.loads(payload.decode())
        msg_logging = dict(
            date = datetime.now().strftime(r'%d/%m/%Y %H:%M:%S'),
            topic = topic,
            msg = message,
            event = "TAKE_PIC"
        )
        print(msg_logging)
        await add_mqtt_logging(msg_logging)
    except:
        pass

@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@fast_mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


@router.get("/", response_description="test publish to mqtt")
async def publish_hello():
    fast_mqtt.publish("/TGR_21", "Hello TGR_21") #publishing mqtt topic
    return {"result": True,"message":"Published" }

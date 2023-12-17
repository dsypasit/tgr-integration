import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://tesarally:contestor@mongoDB:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.water_data

raw_data_collection = database['raw_data']
predict_collection = database.get_collection("predict")
mqtt_logging_collection = database.get_collection("logging")
mqtt_water_level_collection = database.get_collection("water_level")

def RawDataResponse(data):
    return {
        "id": str(data["_id"]),
        "day": data['day'],
        "height_s1": data["height_s1"],
        "discharge_s1": data["discharge_s1"],
        "discharge_s2": data["discharge_s2"],
        "discharge_s3": data["discharge_s3"],
        "height_s3": data["height_s3"],
    }

def PredictDataResponse(data):
    return {
        "id": str(data["_id"]),
        "height_s1": data["height_s1"],
        "discharge_s1": data["discharge_s1"],
    }

# Add a new water into to the database
async def add_mqtt_logging(mqtt_data: dict) :
    await mqtt_logging_collection.insert_one(mqtt_data)

async def add_mqtt_water_level(mqtt_data: dict):
    await mqtt_water_level_collection.insert_one(mqtt_data)
    

async def get_height():
    # Querying the latest 5 documents:
    res = []
    async for l in mqtt_water_level_collection.find().sort('_id', -1).limit(5):
        r = {
            'date': l['date'],
            'height': l['height']
        }
        res.append(r)
    return res[::-1]

async def get_raw_data():
    res = []
    async for l in raw_data_collection.find():
        res.append(RawDataResponse(l))
    return res

async def get_predict_furture():
    res = []
    async for l in predict_collection.find().sort('_id', -1).limit(5):
        res.append(PredictDataResponse(l))
    return res

async def add_matlab_rawdata(data):
    print('delete')
    await raw_data_collection.drop()
    await raw_data_collection.insert_many(data)

async def add_height3_rawdata(data):
    update_all_data = []
    for u in data:
        f = {
            'day': u['day'],
            'update':  {"$set": {"height_s3": u['height_s3']}}
        }
        update_all_data.append(f)
    print(update_all_data[:5])
    
    for update in update_all_data:
        query = {"day": update["day"]}
        update_data = update["update"]
        await raw_data_collection.update_one(query, update_data)

async def update_matlab_predict_raw_data(data):
    update_all_data = []
    for u in data:
        f = {
            'day': u['day'],
            'update':  {"$set": {"discharge_s1": u['discharge_s1']}}
        }
        update_all_data.append(f)
    
    for update in update_all_data:
        query = {"day": update["day"]}
        update_data = update["update"]
        await raw_data_collection.update_one(query, update_data)

async def add_matlab_predict_future(data):
    await predict_collection.insert_many(data)
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://exceed_group14:smcts5we@158.108.182.0:2255/exceed_group14'
mongo = PyMongo(app)

myLightCollection = mongo.db.Light  # keep track of light sensitivity sensor
myMovementCollection = mongo.db.Movement  # keep track of movement
myLocationCollection = mongo.db.Location  # keep track of location
myInformation = mongo.db.Information  # keep track of calculation for user

# =================== GET ============================

# get x,y,z coordinates form gyro
@app.route('/get_movement', methods=['GET'])
def get_movement():
    movement_id = request.args.get('movement_id')
    if movement_id:
        filt = {"movement_id": int(movement_id)}

        query = myMovementCollection.find(filt)
        output = []

        for ele in query:
            output.append({
                "movement_id": ele["movement_id"],
                "fast_movement": ele["fast_movement"], # บอกว่าขยับเร็วไป
                "no_movement": ele["no_movement"] # บแกว่าไม่ค้อยขยับ
            })
        return {"result": output}
    else:
        query = myMovementCollection.find()
        output = []

        for ele in query:
            output.append({
                "movement_id": ele["movement_id"],
                "fast_movement": ele["fast_movement"], # บอกว่าขยับเร็วไป
                "no_movement": ele["no_movement"] # บแกว่าไม่ค้อยขยับ
            })
        return {"result": output}


@app.route('/get_light', methods=['GET'])
def get_light():
    light_id = request.args.get('light_id')
    if light_id:
        filt = {"light_id": int(light_id)}
        query = myLightCollection.find(filt)
        output = []

        for ele in query:
            output.append({
                "light_id": ele["light_id"],
                "light_sensitivity": ele["sensitivity"]
            })
        return {"result": output}
    else:
        query = myLightCollection.find()
        output = []

        for ele in query:
            output.append({
                "light_id": ele["light_id"],
                "light_sensitivity": ele["sensitivity"]
            })
        return {"result": dumps(output)}


@app.route('/get_location_status', methods=['GET'])
def get_location_status():
    query = myLocationCollection.find()
    output = []

    for ele in query:
        return  {"finding_status": ele["finding_status"]}  # 0 1

@app.route('/information', methods=['GET'])
def get_info():
    user_id = request.args.get('user_id')
    if user_id:
        filt = {"user_id": user_id}

        query = myInformation.find(filt)
        output = []

        for ele in query:
            output.append({
                "user_id": ele["user_id"],
                "movement_status": ele["movement_status"],  # too little, too much
                "light_status": ele["light_status"],  # too dark, too bright
                "movement_time": ele["movement_time"],  # total movement time
                "calories": ele["calories"]
            })

        return {"result": output}
    else:
        query = myInformation.find()
        output = []

        for ele in query:
            output.append({
                "user_id": ele["user_id"],
                "movement_status": ele["movement_status"],
                "light_status": ele["light_status"],
                "movement_time": ele["movement_time"],
                "calories": ele["calories"]
            })
        return {"result": output}


# =================== POST ============================

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json

    myInsert = {
        "user_id": data["user_id"],
        "movement_status": "No status",
        "light_status": "No status",
        "movement_time": 0,
        "calories": 0
    }

    myInformation.insert_one(myInsert)
    return {'result': 'Created successfully'}


# CREATE MOVEMENT
@app.route('/create_movement', methods=['POST'])
def create_movement():
    data = request.json

    myInsert = {
        "movement_id": data["movement_id"],
        "fast_movement": data["fast_movement"], # บอกว่าขยับเร็วไป
        "no_movement": data["no_movement"] # บแกว่าไม่ค้อยขยับ
    }

    myMovementCollection.insert_one(myInsert)
    return {'result': 'Created successfully'}


# CREATE LIGHT
@app.route('/create_light', methods=['POST'])
def create_light():
    data = request.json

    myInsert = {
        "light_id": data["light_id"],
        "light_sensitivity": data["sensitivity"]
    }

    myLightCollection.insert_one(myInsert)
    return {'result': 'Created successfully'}


# =================== PUT ============================

# calculate movement
@app.route('/cal_movement', methods=['PUT'])
def cal_movement():
    # id ของ movement
    index = myMovementCollection.count()
    id_filt = {"movement_id": int(index)}

    lastest_movement = myMovementCollection.find(id_filt)

    for ele in lastest_movement:
        if ele['fast_movement'] == 1 and ele['no_movement'] == 0:
            movement_status = "You are moving too fast! Please slow down, You may hurt your muscle."
        elif ele['no_movement'] == 1 and ele['fast_movement'] == 0:
            movement_status = "You are not moving at all! Please move to strength your muscle."
        else:
            movement_status = 'Your movement is good. Keep up your work!'

    # id ของ user
    user_id = request.args.get('user_id')
    filt = {"user_id": int(user_id)}

    movement_updated_status = {"$set": {"movement_status": movement_status}}
    myInformation.update_one(filt, movement_updated_status)
    return {'result': 'Updated successfully'}


# calculate light
@app.route('/cal_light', methods=['PUT'])
def cal_light():
    lastest_light = myLightCollection.find().sort([("_id", -1)]).limit(1)

    user_id = request.args.get('user_id')
    filt = {"user_id": int(user_id)}

    light_status = "None"

    for ele in lastest_light:
        if ele['light_sensitivity'] > 800:
            light_status = "Your device is too bright, Lower it down!"
        elif ele['light_sensitivity'] < 0:
            light_status = "Your device is too dim, Increase your device brightness!"
        else:
            light_status = "Keep up your good work. Your device doesn't hurt your eyes"

    light_updated_status = {"set": {"light_status": light_status}}
    myInformation.update_one(filt, light_updated_status)
    return {'result': 'Updated successfully'}


@app.route('/update_location_status', methods=['PUT'])
def find_status():
    data = request.json
    updated_finding_status = {"$set": {"finding_status": data["finding_status"]}}
    myLocationCollection.update({}, updated_finding_status)
    return {'result': 'Updated successfully'}


@app.route('/cal_calories_and_time', methods=['PUT'])
def cal_calories_and_time():
    index = myMovementCollection.count()
    id_filt = {"movement_id": int(index)}

    lastest_movement = myMovementCollection.find(id_filt)

    for ele in lastest_movement:
        if ele['fast_movement'] == 1 and ele['no_movement'] == 0:  

            # ขยับรอบระวิ ขยับๆต่อกัน 30 รอบส่ง 1 ที เป็นเวลา 30 วิ 
            total_calories = 0.016 # avg moving calories is 60 calories/hour or 0.0.16 calories/sec
            total_time = 30 

            # update both in increment
            updated_calories = {"$inc": {"calories": total_calories}} # increment in calories
            updated_times = {"$inc": {"movement_time": total_time}}

            user_id = request.args.get('user_id')
            filt = {"user_id": int(user_id)}

            myInformation.update(filt, updated_calories)
            myInformation.update(filt, updated_times)

    return {'result': 'Updated successfully'}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='50014', debug=True)

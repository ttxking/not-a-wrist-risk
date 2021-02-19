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


# GET INFO

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
                "time_stamped": ele["time_stamped"],
                "x": ele["x"],
                "y": ele["y"],
                "z": ele["z"]
            })
        return {"result": output}
    else:
        query = myMovementCollection.find()
        output = []

        for ele in query:
            output.append({
                "movement_id": ele["movement_id"],
                "time_stamped": ele["time_stamped"],
                "x": ele["x"],
                "y": ele["y"],
                "z": ele["z"]
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

# CREATE USER
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
        "x": data["x"],
        "y": data["y"],
        "z": data["z"]
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
# CALCULATION PART

# calculate movement
@app.route('/cal_movement', methods=['PUT'])
def cal_movement():
    lastest_movement = myMovementCollection.find().sort([("_id", -1)]).limit(1)
    first_movement = myMovementCollection.find().sort([("_id", 1)]).limit(1)

    user_id = request.args.get('user_id')
    filt = {"user_id": int(user_id)}

    movement_status = "None"

    for ele_i in lastest_movement:
        for ele_j in first_movement:
            if (abs(ele_i['x'] - ele_j['x']) and abs(ele_i['y'] - ele_j['y']) < 10 and abs(
                    ele_i['z'] - ele_j['z']) < 10):
                movement_status = 'Movement is too little. You need some exercise!'
            elif abs(ele_i['x'] - ele_j['x'] < 10):
                movement_status = 'Movement is x-axis is too little. Please move left and right'
            elif abs(ele_i['y'] - ele_j['y'] < 10):
                movement_status = 'Movement is y-axis is too little. Please move up and down'
            elif abs(ele_i['z'] - ele_j['z'] < 10):
                movement_status = 'Movement is z-axis is too little. Please move front and back'
            else:
                movement_status = 'Your movement is good. Keep up your work!'

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


# @app.route('/frontend',methods=['GET'])
# def get_info():
#     output = []
#     return {'result': output}


# @app.route('/create',methods=['POST'])
# def create():
#     data = request.json
#     create = {'status':data['status']}
#     myCollection.insert_one(create)
#     return {'result': 'Created successfully'}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='50014', debug=True)

from flask import Flask, request,jsonify
from flask_pymongo import PyMongo 

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://exceed_group14:smcts5we@158.108.182.0:2255/exceed_group14'
mongo = PyMongo(app)

myLightCollection = mongo.db.Light # keep track of first light sensitivity sensor
myLight2Collection = mongo.db.Light2 # keep track of second light sensitivity sensor
myMovementCollection = mongo.db.Movement # keep track of movement
myLocationCollection = mongo.db.Location # keep track of location
myInformation = mongo.db.Information # keep track of calculation for user


# GET INFO

# get x,y,z coordinates form gyro
@app.route('/get_movement', methods=['GET'])
def get_movement():
    movement_id = request.args.get('movement_id')
    if movement_id :
        filt = {"movement_id" : int(movement_id)}

        query = myMovementCollection.find(filt)
        output = []

        for ele in query:
            output.append({
                "movement_id" : ele["movement_id"],
                "time_stamped" : ele["time_stamped"],
                "x": ele["x"],
                "y" : ele["y"],
                "z" : ele["z"]
            })
        return {"result" : output}
    else : 
        query = myMovementCollection.find()
        output = []

        for ele in query:
            output.append({
                "movement_id" : ele["movement_id"],
                "time_stamped" : ele["time_stamped"],
                "x": ele["x"],
                "y" : ele["y"],
                "z" : ele["z"]
            })
        return {"result" : output}

@app.route('/get_light', methods=['GET'])
def get_light():
    light_id = request.args.get('light_id')
    if light_id :
        filt = {"light_id" : int(light_id)}

        query = myLightCollection.find(filt)
        output = []

        for ele in query:
            output.append({
                "light_id" : ele["light_id"],
                "time_stamped" : ele["time_stamped"],
                "light_sensitivity" : ele["sensitivity"]
            })
        return {"result" : output}
    else : 
        query = myLightCollection.find(filt)
        output = []

        for ele in query:
            output.append({
                "light_id" : ele["light_id"],
                "time_stamped" : ele["time_stamped"],
                "light_sensitivity" : ele["sensitivity"]
            })
        return {"result" : output}


@app.route('/get_light2', methods=['GET'])
def get_light():
    light_id = request.args.get('light_id')
    if light_id :
        filt = {"light_id" : int(light_id)}

        query = myLight2Collection.find(filt)
        output = []

        for ele in query:
            output.append({
                "light_id" : ele["light_id"],
                "time_stamped" : ele["time_stamped"],
                "light_sensitivity" : ele["sensitivity"]
            })
        return {"result" : output}
    else : 
        query = myLight2Collection.find(filt)
        output = []

        for ele in query:
            output.append({
                "light_id" : ele["light_id"],
                "time_stamped" : ele["time_stamped"],
                "light_sensitivity" : ele["sensitivity"]
            })
        return {"result" : output}

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
                "movement_status" : ele["movement_status"], # too little, too much
                "light_status" : ele["light_status"], # too dark, too bright
                "movement_time" : ele["movement_time"],  # total movement time
                "calories" : ele["calories"]
            })
        
        return {"result" : output}
    else :
        query = myInformation.find()
        output = []
        
        for ele in query:
            output.append({
                "user_id": ele["user_id"],
                "movement_status" : ele["movement_status"],
                "light_status" : ele["light_status"],
                "movement_time" : ele["movement_time"],  
                "calories" : ele["calories"]
            })
        return {"result" : output}

# CALCULATION PART 

#calculate movement
@app.route('/movement', methods=['POST'])
def cal_movement():
    data = request.json
    myMovementCollection.update_one()
    return {'result': 'Updated successfully'}

#calculate light
@app.route('/light', methods=['POST'])
def cal_light():
    data = request.json
    myLightCollection.update_one()
    return {'result': 'Updated successfully'}

# NON CATEGORY 

#find location
@app.route('/location',methods=['POST'])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200

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
    app.run(host='0.0.0.0', port='50002', debug=True)



# > db.demo141.find().sort({_id:-1}).limit(1); เอาล่าสุด
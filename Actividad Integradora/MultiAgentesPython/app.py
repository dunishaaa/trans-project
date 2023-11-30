from flask import Flask, jsonify
from ModeloV1 import *
import json

app = Flask(__name__)
model = None
class AgentData():
    def __init__(self, id, direction, x, y):
        self.id = id
        self.direction = direction
        self.x = x
        self.y = y
    

model = None
data_hist = []
g_step = 0

@app.get("/init/<int:cars>/<int:pedestrians>")
def init_cars(cars=1, pedestrians=1):
    global model
    global data_hist 
    global g_step 
    data = []
    model = None
    g_step = 1
    model = MapModel(37,37,cars, 1, pedestrians)
    data = model.ubication((0,0),(36,36))
#    data_hist.append(data)

    return jsonify(data)

@app.get("/data/<int:step>")
def get_data(step):
    global model
    global data_hist
    global g_step 

    model.step()
    data = model.ubication((0,0), (36, 36))
    return jsonify(data)




@app.route("/initialize")
def initialize():
    return"<p>Server initialized</p>"

if __name__ == "__main__":
    app.run(debug=True)
    

    

    

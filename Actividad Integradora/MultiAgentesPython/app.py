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
@app.get("/init")
def init():
    global model
    model =  MapModel(37, 37, 10, 1)
    data = model.ubication((0,0), (36, 36))

    return jsonify(data)

@app.get("/data")
def get_data():
    global model
    model.step()
    data = model.ubication((0,0), (36, 36))
    return jsonify(data)


@app.route("/initialize")
def initialize():
    return"<p>Server initialized</p>"

if __name__ == "__main__":
    app.run(debug=True)
    

    

    
from flask import Flask, jsonify
import json
import logging
from ModeloV1 import *
app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
class AgentData():
    def __init__(self, id, direction, x, y):
        self.id = id
        self.direction = direction
        self.x = x
        self.y = y
        
# class ModelData():
#     def __init__(self, gridSize, cars, metrobuses, pedestrians):
#         self.gridSize = gridSize
#         self.cars = cars
#         self.metrobuses = metrobuses
#         self.pedestrians = pedestrians
model = None
@app.route("/")
def hello():
    return "<p>Hola</p>"
    

@app.get("/init")
def init(width=37, height=37, number_cars=20, number_buses=1):
    model = MapModel(width, height, number_cars, number_buses)
    data = model.ubication((0,0), (36, 36))
    return jsonify(data)

@app.get("/get-data")
def get_model_data():
    model.step()
    data = model.ubication((0,0), (36, 36))
    return jsonify(data)
    
    

@app.get("/get-agent-dictionary")
def get_agent_dictionary():
    cars = [AgentData((1, 1), 1, 1, 3), AgentData((1, 2), 1, 12, 4)]
    metrobus = [AgentData((1, 1), 1, 1, 3), AgentData((1, 2), 1, 12, 4)]
    pedestrians = [AgentData((1, 1), 1, 1, 3), AgentData((1, 2), 1, 12, 4)]
    #agent_data = {'id': (int, int), 'direction': int, 'x': float, 'y': float}
    
    agent_dictionary = {
        "cars": [
            {"id": agent.id, "direction": agent.direction, "x": agent.x, "y": agent.y}
            for agent in cars
        ],
        "metrobus": [
            {"id": agent.id, "direction": agent.direction, "x": agent.x, "y": agent.y}
            for agent in metrobus
        ],
        "pedestrians": [
            {"id": agent.id, "direction": agent.direction, "x": agent.x, "y": agent.y}
            for agent in pedestrians
        ],
    }

    return json.dumps(agent_dictionary)


if __name__ == "__main__":
    app.run(debug=True)
    

    

    
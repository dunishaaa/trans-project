from flask import Flask
import json

app = Flask(__name__)

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
    

@app.route("/initialize")
def initialize():
    return"<p>Server initialized</p>"

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

# @app.get("/get-model-data")
# def get_model_data():
    

if __name__ == "__main__":
    app.run(debug=True)
    

    

    
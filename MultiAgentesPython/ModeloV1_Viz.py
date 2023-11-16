from ModeloV1 import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    portrayal = {}
    if type(agent) is Building:
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 2,
            "Color": "Blue",
            "w": 1,
            "h": 1,
        }
    if type(agent) is Parking:
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 2,
            "Color": "black",
            "w": 1,
            "h": 1,
        }
    if type(agent) is Traffic_light:
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Layer": 3,
            "Color": "red",
            "r": 0.8

        }
        if agent.color == 1:
            portrayal["Color"] = "yellow"
        elif agent.color == 0:
            portrayal["Color"] = "green"
        elif agent.color == 2:
            portrayal["Color"] = "red"
    
    if type(agent) is Street:
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 1,
            "w": 1,
            "h": 1,
        }
        # 0 = arriba | 1 = abajo | 2 = derecha | 3 = izquierda
        if agent.direccion == 0:
            portrayal["Color"] = "white"
        if agent.direccion == 1:
            portrayal["Color"] = "gray"
        if agent.direccion == 2:
            portrayal["Color"] = "red"
        if agent.direccion == 3:
            portrayal["Color"] = "magenta"
            #portrayal["Color"] = (128,128,128)
    if type(agent) is Car:
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Layer": 3,
            "Color": "purple",
            "r": 0.8
        }
        if not agent.show:
            portrayal["Color"] = "gray"
        
    return portrayal



var = 28
num_cars = 1 
grid = CanvasGrid(agent_portrayal, var, var)

server = ModularServer(
    MapModel,
    [grid],
    "Cleaning the grid",
    {
        "width": var,
        "height":  var,
        "number_cars": num_cars
    },
)
server.port = 8521  # The default
server.launch()


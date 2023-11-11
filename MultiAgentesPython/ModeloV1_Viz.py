from ModeloV1 import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    portrayal = {}
    if type(agent) is Building:
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 1,
            "Color": "purple",
            "w": 1,
            "h": 1,
        }
    return portrayal



grid = CanvasGrid(agent_portrayal, 28, 28)

server = ModularServer(
    MapModel,
    [grid],
    "Cleaning the grid",
    {
        "width": 28,
        "height":  28,
    },
)
server.port = 8521  # The default
server.launch()


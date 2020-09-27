from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from covid_simulation.model import CovidModel


def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "r": 0.5
    }
    if agent.is_infected:
        portrayal["Color"] = "red"
    elif agent.has_immunity:
        portrayal["Color"] = "blue"
    else:
        portrayal["Color"] = "grey"
    return portrayal


grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(CovidModel,
                       [grid],
                       "COVID Model",
                       {"N": 60, "M": 40, "width": 10, "height": 10})
server.port = 8521  # The default
server.launch()

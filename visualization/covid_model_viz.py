from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule

from covid_simulation.model import CovidModel


# The server can only run under python 3.7!
def agent_portrayal(agent):
    portrayal = {
        "Filled": "true",
        "Layer": 0,
        "r": 0.5
    }
    if agent.has_immunity:
        portrayal["Shape"] = "immune.png"
    elif agent.is_infected and not agent.wear_mask:
        portrayal["Shape"] = "infected_without_mask.png"
    elif agent.is_infected and agent.wear_mask:
        portrayal["Shape"] = "infected_mask.png"
    elif not agent.is_infected and agent.wear_mask:
        portrayal["Shape"] = "healthy_mask.png"
    else:
        portrayal["Shape"] = "healthy_without_mask.png"
    return portrayal


grid = CanvasGrid(agent_portrayal, 15, 15, 500, 500)
chart = ChartModule([{"Label": "Fatality Rate", "Color": "Black"}],
                    data_collector_name='data_collector')
server = ModularServer(CovidModel,
                       [grid, chart],
                       "COVID Model",
                       {"N": 60, "M": 5, "J": 1, "K": 2, "width": 15, "height": 15})
server.port = 8521  # The default
server.launch()

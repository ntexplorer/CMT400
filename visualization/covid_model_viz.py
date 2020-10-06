import configparser

from covid_simulation.model import CovidModel
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule

config = configparser.ConfigParser()
config.read('../covid_simulation/config.ini')
covid_model = config['covid_model']
hospital_capacity = config['hospital_capacity']


# The server can only run under python 3.7.x
# The ModularServer doesn't support two models running in one server

def agent_portrayal(agent):
    portrayal = {
        "Filled": "true",
        "Layer": 0,
    }
    if agent.has_immunity:
        portrayal["Shape"] = "immune.png"
    elif agent.is_infected and not agent.has_symptom and not agent.wear_mask:
        portrayal["Shape"] = "incubation_without_mask.png"
    elif agent.is_infected and not agent.has_symptom and agent.wear_mask:
        portrayal["Shape"] = "incubation_mask.png"
    elif agent.is_infected and agent.has_symptom and not agent.wear_mask:
        portrayal["Shape"] = "symptomatic_without_mask.png"
    elif agent.is_infected and agent.has_symptom and agent.wear_mask:
        portrayal["Shape"] = "symptomatic_mask.png"

    elif not agent.is_infected and agent.wear_mask:
        portrayal["Shape"] = "healthy_mask.png"
    else:
        portrayal["Shape"] = "healthy_without_mask.png"
    return portrayal


grid = CanvasGrid(agent_portrayal, int(covid_model['width']), int(covid_model['height']), 800, 800)

chart1 = ChartModule([{"Label": "Fatalities", "Color": "Black"},
                      {"Label": "Immune", "Color": "Blue"},
                      {"Label": "Healthy", "Color": "Green"},
                      {"Label": "Infected", "Color": "Orange"},
                      {"Label": "Hospital Occupation", "Color": "Yellow"}],
                     data_collector_name='data_collector')
chart2 = ChartModule([{"Label": "Fatality Rate", "Color": "Black"},
                      {"Label": "Morbidity Rate", "Color": "Orange"}],
                     data_collector_name='data_collector')
server = ModularServer(CovidModel,
                       [grid, chart1, chart2],
                       "COVID Model Simulation",
                       {"N": int(covid_model['N']), "M": int(covid_model['M']),
                        "J": int(covid_model['J']), "K": int(covid_model['K']),
                        "L": int(hospital_capacity["L"]),
                        "width": int(covid_model['width']),
                        "height": int(covid_model['height'])})
server.port = 8521  # The default
server.launch()

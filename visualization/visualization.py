import configparser

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule

from covid_simulation.model import CovidModel

new_config = configparser.ConfigParser()
new_config.read('../visualization/config.ini')
covid_model = new_config['covid_model']
hospital_capacity = new_config['hospital_capacity']


def agent_portrayal(agent):
    portrayal = {
        "Filled": "true",
        "Layer": 0,
    }
    if agent.has_immunity:
        portrayal["Shape"] = "img/immune.png"
    elif agent.is_infected and not agent.has_symptom and not agent.wear_mask:
        portrayal["Shape"] = "img/incubation_without_mask.png"
    elif agent.is_infected and not agent.has_symptom and agent.wear_mask:
        portrayal["Shape"] = "img/incubation_mask.png"
    elif agent.is_infected and agent.has_symptom and not agent.wear_mask:
        portrayal["Shape"] = "img/symptomatic_without_mask.png"
    elif agent.is_infected and agent.has_symptom and agent.wear_mask:
        portrayal["Shape"] = "img/symptomatic_mask.png"
    elif not agent.is_infected and agent.wear_mask:
        portrayal["Shape"] = "img/healthy_mask.png"
    else:
        portrayal["Shape"] = "img/healthy_without_mask.png"
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

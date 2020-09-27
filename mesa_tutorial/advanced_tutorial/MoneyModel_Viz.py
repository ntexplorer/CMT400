#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Tian Z
# @File : MoneyModel_Viz.py
# @Software: PyCharm
# @Version:

import numpy as np
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule

from mesa_tutorial.introductory_tutorial.money_model import *


class HistogramModule(VisualizationElement):
    package_includes = ["Chart.min.js"]
    local_includes = ["HistogramModule.js"]

    def __init__(self, bins, canvas_height, canvas_width):
        super().__init__()
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.bins = bins
        new_element = "new HistogramModule({},{},{})"
        new_element = new_element.format(bins,
                                         canvas_width,
                                         canvas_height)
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        wealth_vals = [agent.wealth for agent in model.schedule.agents]
        hist = np.histogram(wealth_vals, bins=self.bins)[0]
        return [int(x) for x in hist]


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 # "Color": "red",
                 "Filled": "true",
                 # "Layer": 0,
                 "r": 0.5}
    if agent.wealth > 0:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    return portrayal


grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

chart = ChartModule([{"Label": "Gini",
                      "Color": "Black"}],
                    data_collector_name='datacollector')

histogram = HistogramModule(list(range(10)), 200, 500)

server = ModularServer(MoneyModel,
                       [grid, chart, histogram],
                       "Money Model",
                       {"N": 100, "width": 10, "height": 10})
server.port = 8521
server.launch()

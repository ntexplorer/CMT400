from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import SingleGrid
from mesa.time import RandomActivation

from covid_simulation.covid_agent import CovidAgent
from covid_simulation.data_compute import *


class CovidModel(Model):
    """
    initialize the model with N agents, of which M agents are infected initially
    Parameter J and K for numbers of agents who wears face masks;
    add all the agents in the agent_list for function position_agent
    """

    def __init__(self, N: int, M: int, J: int, K: int, L: int, width, height):
        super().__init__()
        self.agent_number = N
        self.initial_infected = M
        self.healthy_with_mask = J
        self.carrier_with_mask = K
        self.hospital_capacity = L
        self.hospital_occupation = 0
        self.grid = SingleGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.agent_list = []

        for i in range(self.carrier_with_mask):
            infected_with_mask = CovidAgent(i, self, True, True)
            self.schedule.add(infected_with_mask)
            self.agent_list.append(infected_with_mask)

        for i in range(self.carrier_with_mask, self.initial_infected):
            infected_without_mask = CovidAgent(i, self, True, False)
            self.schedule.add(infected_without_mask)
            self.agent_list.append(infected_without_mask)

        for i in range(self.initial_infected, (self.agent_number - self.healthy_with_mask)):
            healthy_without_mask = CovidAgent(i, self, False, False)
            self.schedule.add(healthy_without_mask)
            self.agent_list.append(healthy_without_mask)

        for i in range((self.agent_number - self.healthy_with_mask), self.agent_number):
            healthy_with_mask = CovidAgent(i, self, False, True)
            self.schedule.add(healthy_with_mask)
            self.agent_list.append(healthy_with_mask)

        for agent in self.agent_list:
            # for SingleGrid use position_agent to place them the first time
            self.grid.position_agent(agent)

        self.data_collector = DataCollector(
            model_reporters={"Fatalities": compute_fatalities,
                             "Immune": compute_immune,
                             "Healthy": compute_healthy_agent,
                             "Infected": compute_infection,
                             "Hospital Occupation": compute_hospital_treated}
        )

    def step(self):
        self.data_collector.collect(self)
        self.schedule.step()

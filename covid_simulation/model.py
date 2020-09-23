from mesa import Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation

from covid_simulation.covid_agent import CovidAgent


class CovidModel(Model):
    def __init__(self, N, M, width, height):
        super().__init__()
        self.agent_number = N
        self.initial_infected = M
        self.grid = SingleGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.agent_list = []

        for i in range(self.initial_infected):
            infected_agent = CovidAgent(i, self, True)
            self.schedule.add(infected_agent)
            self.agent_list.append(infected_agent)

        for i in range(self.initial_infected, self.agent_number):
            healthy_agent = CovidAgent(i, self, False)
            self.schedule.add(healthy_agent)
            self.agent_list.append(healthy_agent)

        for agent in self.agent_list:
            self.grid.position_agent(agent)

    def step(self):
        self.schedule.step()

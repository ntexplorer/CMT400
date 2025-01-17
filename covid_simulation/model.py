import configparser

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import SingleGrid
from mesa.time import RandomActivation

from covid_simulation.covid_agent import CovidAgent
from covid_simulation.data_compute import *

config = configparser.ConfigParser()
config.read('../visualization/config.ini')
quarantine_rate = config['quarantine_rate']
quarantine_threshold = config['quarantine_threshold']


class CovidModel(Model):
    """
    initialize the model with N agents, of which M agents are infected initially
    Parameter J and K for numbers of agents who wears face masks;
    add all the agents in the agent_list for function position_agent
    """

    def __init__(self, N: int, M: int, J: int, K: int, L: int, width, height,
                 hospital_activated: bool, auto_self_isolation: bool,
                 manual_self_isolation_lvl: int):
        super().__init__()
        self.agent_number = N
        self.initial_infected = M
        self.healthy_with_mask = J
        self.carrier_with_mask = K
        self.hospital_capacity = L
        self.hospital_occupation = 0
        self.hospital_activated = hospital_activated
        self.auto_self_isolation = auto_self_isolation
        self.manual_self_isolation_lvl = manual_self_isolation_lvl
        self.grid = SingleGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.schedule_end_steps = 0
        self.schedule_end_flag = False
        self.highest_morbidity_rate = 0
        self.running = True
        self.agent_list = []
        self.symptomatic_list = []
        self.symptomatic_rate = 0
        self.quarantine_toggle = 0
        self.quarantine_list = []
        self.quarantined_agent_length_1 = 0
        self.quarantined_agent_length_2 = 0

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
                             "Hospital Occupation": compute_hospital_treated,
                             "Fatality Rate": compute_fatality_rate,
                             "Morbidity Rate": compute_morbidity_rate}
        )

    def step(self):
        self.data_collector.collect(self)
        self.schedule.step()
        self.get_end_time()
        self.get_highest_morbidity_rate()

    # A function to check if all agents are not infected
    def check_all_agents(self):
        for agent in self.agent_list:
            if agent.is_infected:
                return False
        return True

    def get_end_time(self):
        # if all the agents get rid of infection and the model has not register the steps
        if self.check_all_agents() and not self.schedule_end_flag:
            self.schedule_end_steps = self.schedule.steps
            # set the flag to true to only record the steps once
            self.schedule_end_flag = True

    def auto_quarantine_get_symptomatic_rate(self):
        # if the agent has symptom, append it to the list
        self.symptomatic_list = []
        for agent in self.agent_list:
            if agent.has_symptom:
                self.symptomatic_list.append(agent)
        # then calculate the symptomatic_rate
        self.symptomatic_rate = len(self.symptomatic_list) / len(self.agent_list)

    def auto_quarantine_update_quarantine_list(self):
        # get number of agents who need to be self-isolated for both quarantine level
        self.quarantined_agent_length_1 = round(len(self.agent_list) * float(quarantine_rate["1"]))
        self.quarantined_agent_length_2 = round(len(self.agent_list) * float(quarantine_rate["2"]))
        # level 1
        if float(quarantine_threshold['level_1_threshold']) <= self.symptomatic_rate < float(
                quarantine_threshold['level_2_threshold']) and self.quarantine_toggle != 1:
            self.auto_quarantine_reset_quarantine_list()
            # pick random agents (number set by lvl 1) to stay still
            self.quarantine_list = self.random.sample(self.agent_list, self.quarantined_agent_length_1)
            # set the toggle to 1
            self.quarantine_toggle = 1
        # level 2
        elif float(quarantine_threshold['level_2_threshold']) <= self.symptomatic_rate and self.quarantine_toggle != 2:
            self.auto_quarantine_reset_quarantine_list()
            # pick random agents (number set by lvl 2) to stay still
            self.quarantine_list = self.random.sample(self.agent_list, self.quarantined_agent_length_2)
            # set the toggle to 2
            self.quarantine_toggle = 2
        elif float(quarantine_threshold['level_1_threshold']) > self.symptomatic_rate and self.quarantine_toggle != 0:
            self.auto_quarantine_reset_quarantine_list()
            # at lvl 0 no one needs to self-isolate
            self.quarantine_list = []
            self.quarantine_toggle = 0
        # all the agents in the list to stay still
        for agent in self.quarantine_list:
            agent.self_isolation_toggle = True

    def auto_quarantine_reset_quarantine_list(self):
        for agent in self.agent_list:
            agent.self_isolation_toggle = False

    def manual_quarantine(self):
        if not self.quarantine_toggle:
            self.quarantine_toggle = 1
            quarantined_agent_length = round(len(self.agent_list)
                                             * float(quarantine_rate[str(self.manual_self_isolation_lvl)]))
            self.quarantine_list = self.random.sample(self.agent_list, quarantined_agent_length)
            for agent in self.quarantine_list:
                agent.self_isolation_toggle = True

    def get_highest_morbidity_rate(self):
        morbidity_list = []
        for agent in self.agent_list:
            if agent.is_infected:
                morbidity_list.append(agent)
        H = len(morbidity_list)
        morbidity_rate = H / self.agent_number
        if morbidity_rate > self.highest_morbidity_rate:
            self.highest_morbidity_rate = morbidity_rate

import math

from mesa import Agent
from mesa.space import Grid

from covid_simulation import const


class CovidAgent(Agent):
    # each agent has an unique ID, and a status of whether it is infected
    def __init__(self, unique_id, model, is_infected: bool, wear_mask: bool):
        super().__init__(unique_id, model)
        # agents age from 0 to 89
        self.age = self.random.randint(0, 89)
        self.is_infected = is_infected
        self.wear_mask = wear_mask
        self.infection_trigger = False
        self.incubation = 0
        self.symptomatic = 0
        self.infection_countdown = -1
        self.has_immunity = False
        self.is_dead = False
        self.fatality_rate = 0

    def step(self) -> None:
        if not self.is_dead:
            self.move()
            self.pass_covid()
            self.get_infected()
            self.infection_count()
            self.infection_end()

    def move(self):
        # find all the possible steps and if it's empty them append it into a list
        all_steps = self.model.grid.get_neighborhood(self.pos, moore=True,
                                                     include_center=False)
        possible_steps = []
        for cell in all_steps:
            if Grid.is_cell_empty(self.model.grid, cell):
                possible_steps.append(cell)

        # if the list is not empty them find a random cell for the agent to move in
        if possible_steps:
            new_position = self.random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)
        # FOR DEBUG USAGE
        # print("agent " + str(self.unique_id) + " age: " + str(self.age)
        #       + " is in position: " + str(new_position)
        #       + " -has immunity: " + str(self.has_immunity) + " -is dead: "
        #       + str(self.is_dead)
        #       + " -is infected: " + str(self.is_infected))

    def pass_covid(self):
        # find all the cellmates near the agent
        cellmates = self.model.grid.get_neighbors(self.pos, True)
        for cellmate in cellmates:
            if not cellmate.has_immunity:
                pass_probability = self.random.randint(0, 1000)
                if self.is_infected and not self.wear_mask:
                    if not cellmate.wear_mask:
                        if pass_probability <= (const.PASS_PR_BOTH_OFF * 1000):
                            cellmate.is_infected = True
                    else:
                        if pass_probability <= (const.PASS_PR_CONTACT_ON * 1000):
                            cellmate.is_infected = True
                elif self.is_infected and self.wear_mask:
                    if not cellmate.wear_mask:
                        if pass_probability <= (const.PASS_PR_CARRIER_ON * 1000):
                            cellmate.is_infected = True
                    else:
                        if pass_probability <= (const.PASS_PR_BOTH_ON * 1000):
                            cellmate.is_infected = True

    def get_infected(self):
        # infection trigger is to prevent from multiple info update
        if self.is_infected and not self.infection_trigger:
            self.incubation = self.random.randint(const.INCUBATION_MIN, const.INCUBATION_MAX)
            self.symptomatic = self.random.randint(const.SYMPTOMATIC_MIN, const.SYMPTOMATIC_MAX)
            self.infection_countdown = self.incubation + self.symptomatic
            self.infection_trigger = True

    def infection_count(self):
        # every step the agent moves the countdown goes down by 1
        if self.is_infected and self.infection_trigger and not self.has_immunity:
            self.infection_countdown -= 1

    def infection_end(self):
        # when the countdown reaches 0
        if self.infection_countdown == 0:
            self.fatality_rate = const.FATALITY_RATE[math.floor(self.age / 10)] * 1000
            if self.fatality_rate >= self.random.randint(0, 1000):
                self.is_dead = True
                self.is_infected = False
                # remove the agent from the grid
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
                # FOR DEBUG USAGE
                # print("***\nAgent " + str(self.unique_id) + " is dead and removed!\n***")
                self.infection_countdown = -1
            else:
                self.has_immunity = True
                self.is_infected = False
                self.infection_countdown = -1

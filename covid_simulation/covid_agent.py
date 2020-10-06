import configparser
import math

from mesa import Agent
from mesa.space import Grid

config = configparser.ConfigParser()
config.read('../visualization/config.ini')
default_setting = config['DEFAULT']
pass_probability = config['pass_probability']
incubation = config['incubation']
symptomatic = config['symptomatic']
fatality_rate = config['fatality_rate']
immunity_loss = config['immunity_loss']


class CovidAgent(Agent):
    # each agent has an unique ID, and a status of whether it is infected
    def __init__(self, unique_id, model, is_infected: bool, wear_mask: bool):
        super().__init__(unique_id, model)
        # agents age from 0 to 89
        self.age = self.random.randint(0, 89)
        self.is_infected = is_infected
        self.wear_mask = wear_mask
        self.has_symptom = False
        self.in_hospital = False
        self.infection_toggle = False
        self.incubation_count = 0
        self.symptomatic_count = 0
        self.infection_countdown = -1
        self.has_immunity = False
        self.is_dead = False
        self.fatality_rate = 0
        self.immunity_loss_rate = 0
        self.immunity_countdown = -1
        self.immunity_loss_toggle = False
        self.social_distancing_toggle = False

    def step(self) -> None:
        # if the agent is not dead then proceed steps
        if not self.is_dead:
            self.hospital_treatment()
            self.check_quarantine_status()
            if not self.social_distancing_toggle:
                self.move()
            self.pass_covid()
            self.get_infected()
            self.infection_count()
            self.infection_end()
            self.immunity_loss_check()
            self.immunity_loss()

    # check if auto quarantine change mode is on, if not switch to manual mode
    def check_quarantine_status(self):
        if default_setting.getboolean('activate_automatic_mode'):
            self.model.auto_quarantine_get_symptomatic_rate()
            self.model.auto_quarantine_update_quarantine_list()
        else:
            self.model.manual_quarantine()

    # check if hospital mode is on
    def hospital_treatment(self):
        if default_setting.getboolean('activate_hospital'):
            # if the agent is symptomatic and there's still room in the hospital and it's not in it
            if self.has_symptom and self.model.hospital_occupation < \
                    self.model.hospital_capacity and not self.in_hospital:
                # remove the agent from the grid
                self.model.grid.remove_agent(self)
                self.model.hospital_occupation += 1
                self.in_hospital = True

    def move(self):
        if not self.in_hospital:
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
        if not self.in_hospital:
            # find all the cellmates near the agent
            cellmates = self.model.grid.get_neighbors(self.pos, True)
            for cellmate in cellmates:
                if not cellmate.has_immunity:
                    if self.is_infected and not self.wear_mask:
                        if not cellmate.wear_mask:
                            if self.random.randint(0, 1000) <= \
                                    (float(pass_probability['PASS_PR_BOTH_OFF']) * 1000):
                                cellmate.is_infected = True
                        else:
                            if self.random.randint(0, 1000) <= \
                                    (float(pass_probability['PASS_PR_CONTACT_ON']) * 1000):
                                cellmate.is_infected = True
                    elif self.is_infected and self.wear_mask:
                        if not cellmate.wear_mask:
                            if self.random.randint(0, 1000) <= \
                                    (float(pass_probability['PASS_PR_CARRIER_ON']) * 1000):
                                cellmate.is_infected = True
                        else:
                            if self.random.randint(0, 1000) <= \
                                    (float(pass_probability['PASS_PR_BOTH_ON']) * 1000):
                                cellmate.is_infected = True

    def get_infected(self):
        # infection toggle is to prevent from multiple info update
        if self.is_infected and not self.infection_toggle:
            self.incubation_count = self.random.randint(int(incubation['INCUBATION_MIN']),
                                                        int(incubation['INCUBATION_MAX']))
            self.symptomatic_count = self.random.randint(int(symptomatic['SYMPTOMATIC_MIN']),
                                                         int(symptomatic['SYMPTOMATIC_MAX']))
            self.infection_countdown = self.incubation_count + self.symptomatic_count
            self.infection_toggle = True

    def infection_count(self):
        # every step the agent moves the countdown goes down by 1
        if self.is_infected:
            self.infection_countdown -= 1
        if self.infection_countdown == self.symptomatic_count:
            self.has_symptom = True

    def infection_end(self):
        # when the countdown reaches 0
        if self.infection_countdown == 0:
            self.fatality_rate = float(fatality_rate[str(math.floor(self.age / 10))]) * 1000
            if self.fatality_rate >= self.random.randint(0, 1000):
                # the agent dies
                self.is_dead = True
                self.is_infected = False
                self.has_symptom = False
                if not self.in_hospital:
                    # if it's not in the hospital then remove it from the grid
                    self.model.grid.remove_agent(self)
                else:
                    # if in the hospital then remove it from the hospital
                    self.in_hospital = False
                    self.model.hospital_occupation -= 1
                # remove the agent from the schedule
                self.model.schedule.remove(self)
                # FOR DEBUG USAGE
                # print("***\nAgent " + str(self.unique_id) + " is dead and removed!\n***")
                self.infection_countdown = -1
            else:
                # the agent got immunity
                self.has_immunity = True
                # if it recovers in the hospital, place it back to the grid
                if self.in_hospital:
                    self.model.grid.position_agent(self)
                    self.in_hospital = False
                    self.model.hospital_occupation -= 1
                # reset the status
                self.is_infected = False
                self.has_symptom = False
                self.infection_countdown = -1

    def immunity_loss_check(self):
        # if the agent has immunity and not been checked yet
        if self.has_immunity and not self.immunity_loss_toggle:
            # turn on the toggle to prevent multiple check
            self.immunity_loss_toggle = True
            # get the probability of losing immunity
            self.immunity_loss_rate = float(immunity_loss['IMMUNITY_LOSS_PR']) * 1000
            if self.random.randint(0, 1000) <= self.immunity_loss_rate:
                self.immunity_countdown = self.random.randint(int(immunity_loss['IMMUNITY_LOSS_MIN']),
                                                              int(immunity_loss['IMMUNITY_LOSS_MAX']))

    def immunity_loss(self):
        if self.immunity_loss_toggle and self.immunity_countdown > 0:
            self.immunity_countdown -= 1
        # when the countdown reaches 0, reset the agent to a healthy one without immunity
        elif self.immunity_loss_toggle and self.immunity_countdown == 0:
            self.immunity_countdown = -1
            self.has_immunity = False
            self.infection_toggle = False
            self.immunity_loss_toggle = False

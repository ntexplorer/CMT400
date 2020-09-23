from mesa import Agent
from mesa.space import Grid


class CovidAgent(Agent):
    def __init__(self, unique_id, model, is_infected):
        super().__init__(unique_id, model)
        self.is_infected = is_infected

    def step(self) -> None:
        self.move()
        self.pass_covid()

    def move(self):
        all_steps = self.model.grid.get_neighborhood(self.pos, moore=True,
                                                     include_center=False)
        possible_steps = []
        for cell in all_steps:
            if Grid.is_cell_empty(self.model.grid, cell):
                possible_steps.append(cell)

        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        print("agent " + str(self.unique_id) + " is in position: " + str(new_position))

    def pass_covid(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if self.is_infected:
            for cellmate in cellmates:
                pass_probability = self.random.randint(0, 100)
                if pass_probability <= 80:
                    cellmate.is_infected = True

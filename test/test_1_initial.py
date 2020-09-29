from covid_simulation.model import CovidModel

model = CovidModel(50, 1, 10, 10)
for i in range(200):
    model.step()

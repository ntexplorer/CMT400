from covid_simulation.model import CovidModel

model = CovidModel(50, 49, 10, 10)
model.step()
for i in range(200):
    model.step()

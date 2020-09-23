from covid_simulation.model import CovidModel

model = CovidModel(50, 2, 10, 10)
model.step()
# for i in range(20):
#     model.step()

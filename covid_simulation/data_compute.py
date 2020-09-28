def compute_fatality_rate(model):
    N = model.agent_number
    D = len([agent for agent in model.schedule.agents])
    return (N - D) / N

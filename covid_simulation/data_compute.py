def compute_fatality_rate(model):
    N = model.agent_number
    D = len([agent for agent in model.schedule.agents])
    return (N - D) / N


def compute_morbidity_rate(model):
    morbidity_list = []
    N = model.agent_number
    for agent in model.agent_list:
        if agent.is_infected:
            morbidity_list.append(agent)
    H = len(morbidity_list)
    return H / N


def compute_fatalities(model):
    N = model.agent_number
    D = len([agent for agent in model.schedule.agents])
    return N - D


def compute_immune(model):
    immune_list = []
    for agent in model.agent_list:
        if agent.has_immunity:
            immune_list.append(agent)
    return len(immune_list)


def compute_healthy_agent(model):
    healthy_list = []
    for agent in model.agent_list:
        if not agent.is_infected and not agent.has_immunity \
                and not agent.is_dead:
            healthy_list.append(agent)
    return len(healthy_list)


def compute_infection(model):
    infected_list = []
    for agent in model.agent_list:
        if agent.is_infected:
            infected_list.append(agent)
    return len(infected_list)


def compute_hospital_treated(model):
    hospital_treated_list = []
    for agent in model.agent_list:
        if agent.in_hospital:
            hospital_treated_list.append(agent)
    return len(hospital_treated_list)

import configparser

config = configparser.ConfigParser()
config['DEFAULT'] = {
    "; Toggle to activate hospital\n"
    "activate_hospital": "true",
    "; If auto mode is off, set the self-isolation level below (0-2) manually\n"
    "manual_self_isolation_lvl": '0',
    "; Toggle to activate auto-self-isolation\n"
    "activate_automatic_mode": "true"
}

config['covid_model'] = {
    "; Number of agents\n"
    "N": "200",
    "; Number of initially infected agents\n"
    "M": "30",
    "; Number of healthy agents who wear face masks\n"
    "J": "0",
    "; Number of infected agents who wear face masks\n"
    "K": "0",
    "; Mu of age distribution\n"
    "MU": "30",
    "; Sigma of age distribution\n"
    "SIGMA": "15",
    "; Width of the grid\n"
    "width": "50",
    "; Height of the grid\n"
    "height": "50"
}

config['hospital_capacity'] = {
    "; Hospital Capacity\n"
    "L": "35"
}

config['pass_probability'] = {
    "; Pass probability when both agents wear masks\n"
    "PASS_PR_BOTH_ON": "0.015",
    "; Pass probability when only the carrier wear masks\n"
    "PASS_PR_CARRIER_ON": "0.05",
    "; Pass probability when only the healthy contact wear masks\n"
    "PASS_PR_CONTACT_ON": "0.7",
    "; Pass probability when both agents don't wear masks\n"
    "PASS_PR_BOTH_OFF": "0.95",
    "; Pass probability when the agents is in quarantine\n"
    "PASS_PR_QUARANTINE": "0.02"
}

config['incubation'] = {
    "; Minimum incubation period\n"
    "INCUBATION_MIN": "1",
    "; Maximum incubation period\n"
    "INCUBATION_MAX": "14"
}

config['symptomatic'] = {
    "; Minimum symptomatic period\n"
    "SYMPTOMATIC_MIN": "14",
    "; Maximum symptomatic period\n"
    "SYMPTOMATIC_MAX": "35"
}

config['fatality_rate'] = {
    "; Fatality rate for agents aged between 0~9 years old\n"
    '0': '0.5',
    "; Fatality rate for agents aged between 10~19 years old\n"
    '1': '0.4',
    "; Fatality rate for agents aged between 20~29 years old\n"
    '2': '0.2',
    "; Fatality rate for agents aged between 30~39 years old\n"
    '3': '0.3',
    "; Fatality rate for agents aged between 40~49 years old\n"
    '4': '0.3',
    "; Fatality rate for agents aged between 50~59 years old\n"
    '5': '0.4',
    "; Fatality rate for agents aged between 60~69 years old\n"
    '6': '0.4',
    "; Fatality rate for agents aged between 70~79 years old\n"
    '7': '0.4',
    "; Fatality rate for agents aged above 80~89 years old\n"
    '8': '0.5'
}

config['immunity_loss'] = {
    "; Probability of people losing immunity after a while\n"
    'IMMUNITY_LOSS_PR': '0.83',
    "; Minimum time people lose immunity after recovery\n"
    'IMMUNITY_LOSS_MIN': '7',
    "; Maximum time people lose immunity after recovery\n"
    'IMMUNITY_LOSS_MAX': '14',
}

config['quarantine_rate'] = {
    "; The rate of people who need to self-isolate\n"
    '0': '0',
    '1': '0.6',
    '2': '0.9',
}

config['quarantine_threshold'] = {
    "; The threshold of the rate of agents to start self-isolation policy\n"
    'level_1_threshold': '0.1',
    'level_2_threshold': '0.2',
}

with open('config.ini', 'w') as config_file:
    config.write(config_file)

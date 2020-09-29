import configparser

config = configparser.ConfigParser()
config['DEFAULT'] = {
    "activate_hospital": "true",
    "activate_social_distancing": '0'
}
config['covid_model'] = {
    "; Number of agents\n"
    "N": "200",
    "; Number of initially infected agents\n"
    "M": "30",
    "; Number of healthy agents who wear face masks\n"
    "J": "40",
    "; Number of infected agents who wear face masks\n"
    "K": "2",
    "; Width of the grid\n"
    "width": "50",
    "; Height of the grid\n"
    "height": "50"
}

config['hospital_capacity'] = {
    "; Hospital Capacity\n"
    "L": "40"
}

config['pass_probability'] = {
    "; Pass probability when both agents wear masks\n"
    "PASS_PR_BOTH_ON": "0.015",
    "; Pass probability when only the carrier wear masks\n"
    "PASS_PR_CARRIER_ON": "0.05",
    "; Pass probability when only the healthy contact wear masks\n"
    "PASS_PR_CONTACT_ON": "0.7",
    "; Pass probability when both agents don't wear masks\n"
    "PASS_PR_BOTH_OFF": "0.95"
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
    "; Fatality rate for agents aged between 80~89 years old\n"
    '8': '0.5'
}

with open('config.ini', 'w') as config_file:
    config.write(config_file)

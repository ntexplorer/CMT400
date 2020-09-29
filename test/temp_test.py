import configparser

config = configparser.ConfigParser()
config.read('../covid_simulation/config.ini')

print(int(config['incubation']['INCUBATION_MIN']))
print(int(config['incubation']['INCUBATION_MAX']))

# import configparser
#
# config = configparser.ConfigParser()
# config.read('../covid_simulation/config.ini')
#
# print(int(config['incubation']['INCUBATION_MIN']))
# print(int(config['incubation']['INCUBATION_MAX']))
#
# print(bool(1))
import math
import random


# for i in range(0, 50):
#     print(random.normalvariate(45, 15))

def set_age():
    while True:
        temp_age = math.floor(random.normalvariate(45, 15))
        if 0 <= temp_age <= 89:
            return temp_age


for i in range(0, 50):
    print(set_age())

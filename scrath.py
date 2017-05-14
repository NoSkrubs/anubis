from collections import namedtuple
from numpy import exp
from decimal import Decimal
from enum import Enum
import logging
import time
import os.path
import os
import sys

timestr = time.strftime("%Y%m%d-%H%M%S")
program = os.path.basename(sys.argv[0])

#Global assumptions
class Model(Enum):
    PREVALANCE = 0
    INCIDENCE = 1

#only USA for now
class Region(Enum):
    UNITEDSTATES = 0
    UNITEDKINGDOM = 1
    FRANCE = 2
    GERMANY = 3
    SPAIN = 4
    ITALY = 5
    JAPAN = 6

model_type = Model.PREVALANCE #or incidence
discount = 0.15
price_increase = 0.02
decay_time = 5.0
erosion = 0.4
year_model_ends = 2034

#Clinical trial assumptions
induction_doses = 5 #react user input, total doses
induction_length = 2 #react user input, in months
inductDosesPerMonth = induction_doses / induction_length

maintenance_doses = 8 #react user input, per treatment period
maintenance_days = 90 #react user input, days of treatement period
maintenance_duration = 5 #react user input, in dosing periods
dosingPeriodMonths = maintenance_days/(365.25/12) #convert to months
dosingLength = dosingPeriodMonths * maintenance_duration #half life of maintenance period

#Pricing Assumptions
compliance_rate = 0.75 #percent of doses used (varies by country)
# price_comparable_selection = "Avastin"
price = 1250 #pull from parse or react?
royalty = 0.05 #input from react
rebates = 0.15 #input from react

#Market assumptions
incidence = 0.0002
prevalance = 0.002 #input from react
reimbursement = 0.5 #input from react
cash_market = 0.1 #input from react

launch_month = 9 #input from react
launch_year = 2019 #input from react
loss_of_exclusivity = 2032 #input from react
# peak_share_selection = "Avastin" #react user inpute
peak_share = 0.5 #Pull from parse
# uptake_selection = "Avastin" #react user input

#Market competition
comp_launch_year = 2025 #input from react
comp_strength = 0.5 #input form react in the "strength field"
#comp_uptake = "Avastin" #use this to pull uptake from Parse

#arrays that would be called from parse
years = range(2015, year_model_ends + 1)

uptake_selection = [
    0.1
    ,0.2
    ,0.3
    ,0.4
    ,0.5
    ,0.6
    ,0.7
    ,0.8
    ,0.9
    ,1
    ,1
    ,1
    ,1
    ,1
    ,1
    ,1
    ,1
    ,1
    ,1
    ,1
]
comp_uptake = uptake_selection

#population pulled from parse
total_population = {
    2015: 321369000
    ,2016: 323996000
    ,2017: 326626000
    ,2018: 329256000
    ,2019: 331844000
    ,2020: 334503000
    ,2021: 337109000
    ,2022: 339698000
    ,2023: 342267000
    ,2024: 344814000
    ,2025: 347335000
    ,2026: 349826000
    ,2027: 352281000
    ,2028: 354698000
    ,2029: 357073000
    ,2030: 359402000
    ,2031: 361685000
    ,2032: 363920000
    ,2033: 366106000
    ,2034: 368246000
}

#UPDATE CURVE CREATION
#create uptake curve
rawUptake = {}
for index, year in enumerate(years):
    if year >= launch_year: #check to see if drug has launched
        rawShare = peak_share * uptake_selection[year - launch_year]
        if comp_strength > 0 and year >= comp_launch_year: #check if competition has started
            compShare = comp_strength * comp_uptake[year - comp_launch_year]
            share = (1 - compShare) * rawShare
            rawUptake[year] = (share * reimbursement) + (share * cash_market) #adjust for competition
        else: #if no competiiton then simple share with reimbursmenet & cashmarket
            rawUptake[year] = (rawShare * reimbursement) + (rawShare * cash_market)
    else:
        rawUptake[year] = 0

#decay uptake curve
uptake = {}
shareBeforeExpiry = rawUptake[loss_of_exclusivity - 1]
for year in rawUptake:
    if year < loss_of_exclusivity:
        uptake[year] = rawUptake[year]
    else:
        decayed = exp(-((year - loss_of_exclusivity + 1)/decay_time))
        uptake[year] = max(shareBeforeExpiry * erosion, decayed * shareBeforeExpiry)

#GET PATIENT POPULATION
patients = {}
for year in total_population:
    if model_type == Model.PREVALANCE:
        patients[year] = prevalance * total_population[year]
    elif model_type == Model.INCIDENCE:
        patients[year] = incidence * total_population[year]
    else:
        print('model type not selected! BREAK!')
        break
print(patients)

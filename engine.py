from collections import namedtuple
from numpy import exp
from decimal import Decimal
from enum import Enum
import logging
import time
import os.path
import os
import sys

#andrwafawe
#OLIVIA WAS HERE
#OLIVIA ROCKS SOCKS!
#O


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

class GlobalParameters(object):
    def __init__(self):
        self.model_type = Model.PREVALANCE #or incidence
        self.discount = 0.15
        self.price_increase = 0.02
        self.decay_time = 5.0
        self.erosion = 0.4
        self.year_model_ends = 2034
        self.years = range(2015, self.year_model_ends + 1)
        self.modelTime = {}
        for index, year in enumerate(self.years):
            self.modelTime[year] = range(1, 13)
params = GlobalParameters()

#Clinical trial assumptions for a indication
class Indication(object):
    def __init__(self, disease):
        self.name = disease
        self.inductionDoses = 5 #react user input, total doses
        self.inductionLength = 2 #react user input, in months
        self.inductDosesPerMonth = self.inductionDoses / self.inductionLength
        self.maintenanceDoses = 8 #react user input, per treatment period
        self.maintenanceDays = 90 #react user input, days of treatement period
        self.maintenanceDuration = 5 #react user input, in dosing periods
        self.dosingPeriodMonths = self.maintenanceDays/(365.25/12) #convert to months
        self.dosingLength = self.dosingPeriodMonths * self.maintenanceDuration #half life of maintenance period

#ultimately to be inited from a parse object
class Market(object):
    def __init__(self, region, params):
        self.region = region

        #Pricing Assumptions
        self.compliance = 0.75 #percent of doses used (varies by country)
        # price_comparable_selection = "Avastin"
        self.price = 1250 #pull from parse or react?
        self.royalty = 0.05 #input from react
        self.rebates = 0.15 #input from react

        #population
        self.incidence = 0.0002
        self.prevalance = 0.002 #input from react

        #market share inputs
        self.reimbursement = 0.5 #input from react
        self.cashMarketSize = 0.1 #input from react

        self.launchYear = 2019 #input from react
        self.patentLoss = 2032 #input from react
        self.peakShare = 0.5 #Pull from parse

        #Market competition
        self.competitorLaunch = 2025 #input from react
        self.competitionStrength = 0.5 #input form react in the "strength field"

        #arrays that would be called from parse
        self.uptakeSelection = [
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
        self.competitorUptakeSelection = self.uptakeSelection

        #population pulled from parse
        self.totalPopulation = {
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
        for index, year in enumerate(params.years):
            if year >= self.launchYear: #check to see if drug has launched
                rawShare = self.peakShare * self.uptakeSelection[year - self.launchYear]

                if self.competitionStrength > 0 and year >= self.competitorLaunch: #check if competition has started
                    compShare = self.competitionStrength * self.competitorUptakeSelection[year - self.competitorLaunch]
                    share = (1 - compShare) * rawShare
                    rawUptake[year] = (share * self.reimbursement) + (share * self.cashMarketSize) #adjust for competition
                else: #if no competiiton then simple share with reimbursmenet & cashmarket
                    rawUptake[year] = (rawShare * self.reimbursement) + (rawShare * self.cashMarketSize)
            else:
                rawUptake[year] = 0

        #decay uptake curve
        uptake = {}
        shareBeforeExpiry = rawUptake[self.patentLoss - 1]
        for year in rawUptake:
            if year < self.patentLoss:
                uptake[year] = rawUptake[year]
            else:
                decayed = exp(-((year - self.patentLoss + 1)/params.decay_time))
                uptake[year] = max(shareBeforeExpiry * params.erosion, decayed * shareBeforeExpiry)
        self.uptake = uptake
        print(uptake)

spattergroit = Indication('Spattergroit')
usa = Market(Region.UNITEDSTATES, params)

# #GET PATIENT POPULATION
#
#     if model_type == Model.PREVALANCE:
#     elif model_type == Model.INCIDENCE:
#         patients[year] = incidence * total_population[year]
#     else:
#         print('model type not selected! BREAK!')
#         break

# #PREVALENCE TREATMENT FLOW
# if model_type == Model.PREVALANCE:
#     print('Begin prevelance model treatment')
#     patients = {}
#     for year in total_population:
#         patients[year] = prevalance * total_population[year]
#
# #INCIDENCE TREATMENT FLOW
# elif model_type == Model.INCIDENCE:
#     print('Begin incidence model tratement')
#     patients = {}
#     for year in total_population:
#         patients[year] = incidence * total_population[year]

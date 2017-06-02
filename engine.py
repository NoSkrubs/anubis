from collections import namedtuple
from numpy import exp, arange, array
from decimal import Decimal
from enum import Enum
import logging
import time
import os.path
import os
import sys
import numpy

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

#Clinical trial assumptions for a indication
class Indication(object):
	def __init__(self, disease):
		self.name = disease
		self.inductionDoses = 5.0 #react user input, total doses
		self.inductionLength = 2.0 #react user input, in months
		self.inductDosesPerMonth = self.inductionDoses / self.inductionLength
		self.maintenanceDoses = 8.0 #react user input, per treatment period
		self.maintenanceDays = 90.0 #react user input, days of treatement period
		self.maintenanceDuration = 5.0 #react user input, in dosing periods
		self.dosingPeriodMonths = self.maintenanceDays/(365.25/12) #convert to months
		self.dosingLength = self.dosingPeriodMonths * self.maintenanceDuration #half life of maintenance period

#ultimately to be inited from a parse object
class Market(object):
	def __init__(self, region, params):
		self.region = region

		#Pricing Assumptions
		self.compliance = 0.75 #percent of doses used (varies by country)
		# price_comparable_selection = "Avastin"
		self.price = 1250.0 #pull from parse or react?
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
		print('Final uptake below,')
		print(self.uptake)

		#patient populations per year
		self.incidentPatients = {}
		self.prevalentPatients = {}
		# self.patients = {}`
		for year in params.years:

			#prevalance model
			self.prevalentPatients[year] = (self.prevalance * self.totalPopulation[year] * self.uptake[year])

			#incidence model
			self.incidentPatients[year] = (self.incidence * self.totalPopulation[year] * self.uptake[year])

class TreatmentMatrix(object):
	def __init__(self, market: Market, indication: Indication, params: GlobalParameters):
		#this class is just a connector to subclasses (could be a function)
		self.market = market
		self.indication = indication
		self.params = params

	def treatPatients(self):
		# create arrays necessary for matrix calcs
		# months = list(range(len(params.years) * 12))
		months = arange(len(params.years) * 12)
		cohorts = arange(len(params.years) * 12)


		#select relevant patient population
		if params.model_type == Model.INCIDENCE:
			annualPatients = self.market.incidentPatients
		elif params.model_type == Model.PREVALANCE:
			annualPatients = self.market.prevalentPatients
		else:
			print('no model selected exit function')
			return
		print('annual patients below,')
		print(annualPatients)

		#seed array of monthly patients
		monthlyPatients = []
		for year in annualPatients:
			for index in range(12):
				monthlyPatients.append(annualPatients[year])
		print(monthlyPatients)
		cohortPopulation = arange(len(params.years) * 12) * 0
		totalDoses = arange(len(params.years) * 12) * 0
		totalPatients = arange(len(params.years) * 12) * 0

		#initiate matrix calcs
		patientMatrix = []
		for index in range((len(params.years) * 12)):
			patientMatrix.append(arange((len(params.years) * 12)) * 0)
		treatmentMatrix = patientMatrix

		#Check before loop
		print('InductionLength ' + str(self.indication.inductionLength) + ' duration: ' + str(self.indication.dosingLength))

		for cohort in range(len(cohorts)):
			# print('Begin cohort loop for cohort: ' + str(cohort))
			months = arange(len(params.years) * 12)
			for month in range(len(months)):
				# print('Begin month loop for month: ' + str(month))

				#this seeds both incident and prevelant models for month first month
				if month == 0 and cohort == 0:
					print('month and cohort are 0')
					patientMatrix[cohort][month] = monthlyPatients[month]
					treatmentMatrix[cohort][month] = float(monthlyPatients[month]) * self.indication.inductionDoses

				#this controls for population in prevelant model (REVISIT FOR INCIDENT MODEL!)
				elif month == cohort:
					# print('month equals cohort')
					prevalanceControl = 0
					for cohortIndex in range(cohort):
						prevalanceControl += patientMatrix[cohortIndex][month]
					print('Prevelance control for cohort: ' + str(cohort) + ' month: ' + str(month) + ', ' + str(prevalanceControl))
					if prevalanceControl < monthlyPatients[cohort]:
						cohortPopulation[cohort] = monthlyPatients[cohort] - prevalanceControl

					else:
						cohortPopulation[cohort] = 0

				#implied decayed population at month for cohort
				decayFactor = exp(-1.0 * ((month - (cohort + self.indication.inductionLength - 1.0))/ self.indication.dosingLength))

				#If the Month is less than the Cohort # then the cohort population is 0
				if month < cohort:
					# print('month is less than cohort ' + 'month: ' + str(month) + ' cohort: ' + str(cohort))
					treatmentMatrix[cohort][month] = 0
					patientMatrix[cohort][month] = 0

				#If the month is less than Cohort # + Induction period length then the cohort population is initial patient population
				elif cohort + self.indication.inductionLength > month:
					# print('month is greater than cohort and induction length')
					treatmentMatrix[cohort][month] = float(cohortPopulation[cohort]) * self.indication.inductionDoses
					patientMatrix[cohort][month] = cohortPopulation[cohort]

				elif self.indication.maintenanceDuration == 0:
					treatmentMatrix[cohort][month] = 0
					patientMatrix[cohort][month] = 0

				#If the month is greater than the Cohort # + Induction period, but the decay is less than the rounding threshold then round to 0
				elif cohortPopulation[cohort] * decayFactor < 0.5:
					# print('population is decayed')
					treatmentMatrix[cohort][month] = 0
					patientMatrix[cohort][month] = 0

				#Otherwise, decay the population based on e^( - Time on Treatment / Duration), as time on treatment grows population declines
				else:
					# print('population is decaying')
					treatmentMatrix[cohort][month] = float(cohortPopulation[cohort]) * decayFactor * self.indication.maintenanceDoses
					patientMatrix[cohort][month] = float(cohortPopulation[cohort]) * decayFactor

				#track the sum
				# print('month: ' + str(month) + ' cohort: ' + str(cohort) + ', patients: ' + str(float(treatmentMatrix[cohort][month])))
				totalDoses[cohort] += float(treatmentMatrix[month][cohort])
				totalPatients[cohort] += float(patientMatrix[month][cohort])

			totalDoses[cohort] = totalDoses[cohort] * self.market.compliance

		#sum it all up
		numpyDoseArray = array(totalDoses)
		numpyPatientArray = array(totalPatients)
		print('Total patients below,')
		print(totalPatients)
		print('Total doses below,')
		print(totalDoses)

		monthlyTotalDoses = numpyPatientArray * numpyPatientArray
		dosesSold = sum(monthlyTotalDoses)
		sales = dosesSold * self.market.price

		print(sales)
		#Desired total sales amount is $68,748,740,000
		#2019 sales should be $164,580,000, 2034 sales should be $4,919,110,000

params = GlobalParameters()
spattergroit = Indication('Spattergroit')
usa = Market(Region.UNITEDSTATES, params)
treatment = TreatmentMatrix(usa, spattergroit, params)
treatment.treatPatients()
# print(usa_spattergroit.market.region)

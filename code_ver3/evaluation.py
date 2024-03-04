'''
Evaluating all truck samples, and for each sample, calculate TCO by tech and energy use by tech

'''
import copy
from agent import Agent
from infrastructure import Infrastructure
from vehicle import Vehicle
from policy import Policy
import pandas as pd
import numpy as np
import os


pd.set_option('max_columns', None)
dirname = os.path.dirname(__file__)

class Evaluation:
    
    kWhperDGE = 37.95      #kWh per diesel gallon equivalent
    
    
    def __init__(self, start_year, end_year, df, scenario):
        
        print("    Initialzing...")
        self.start_year = start_year      #year of start of sale
        self.end_year = end_year          # year of end of sale
        self.all_years = list(range(2005, 2051))      #all years for results
        self.segments = list(df["Segment"].unique())   #segments: e.g., Day_cab, Sleeper, Bus
        self.scenario = scenario
        
        self.infrastructure = Infrastructure(scenario)
        self.vehicle = Vehicle(scenario)
        self.policy = Policy(scenario)
        
        #for storing results
        self.BEV_sales = {key1 : {key2 : 0 for key2 in self.all_years} for key1 in self.segments} #done
        self.BEV_stocks = {key1 : {key2 : 0 for key2 in self.all_years} for key1 in self.segments} #done
        self.DV_sales = {key1 : {key2 : 0 for key2 in self.all_years} for key1 in self.segments} #done
        self.DV_stocks = {key1 : {key2 : 0 for key2 in self.all_years} for key1 in self.segments} #done
        self.BEV_VMT = {key1 : {key2 : 0 for key2 in self.all_years} for key1 in self.segments} #done miles
        self.DV_VMT = {key1 : {key2 : 0 for key2 in self.all_years} for key1 in self.segments} #done miles
        self.BEV_incentive = {key1 : {key2 : 0 for key2 in self.all_years} for key1 in self.segments} #done $
        self.infrastructure_incentive = {key1 : {key2 : 0 for key2 in self.all_years} for key1 in self.segments} #$
        self.diesel = {key1 : {key2 : 0 for key2 in self.all_years} for key1 in self.segments}    #DGE
        self.electricity = {key1 : {key2 : 0 for key2 in self.all_years} for key1 in self.segments} #done #kwh
        self.carbon_emissions = {key1 : {key2 : 0 for key2 in self.all_years} for key1 in self.segments} #done #kgs
        
        self.truck_agent_object_list = []
        temp_list = df.to_dict('records')
        
        
        print("    Creating truck agents...")
        for t in range(self.start_year, self.end_year + 1):
            #print(t)
            for i in range(0, len(temp_list)):
                agent = Agent(temp_list[i], t, self.infrastructure, self.vehicle, self.policy)
                self.truck_agent_object_list.append(agent)

        

    def calculate(self):
        print ("    Calculating evolutions of sales, stock, energy use, etc. ")
        for i in range(0, len(self.truck_agent_object_list)):
            if i % 999 == 0:
                print("        processing agent: " + str(self.truck_agent_object_list[i].tad["Segment"]) + " " + 
                      str(self.truck_agent_object_list[i].tad["ID"]) + " in year " + 
                      str(self.truck_agent_object_list[i].tad["year"]))
            
            self.truck_agent_object_list[i].calculate()
            model_year = self.truck_agent_object_list[i].tad["year"]
            lifetime = self.truck_agent_object_list[i].tad["Lifetime"]
            segment = self.truck_agent_object_list[i].tad["Segment"]
            sale = self.truck_agent_object_list[i].tad["Sale"]
            annual_mile_avg = self.truck_agent_object_list[i].tad["Annual_mile_avg"]
            
            if_BEV = (self.truck_agent_object_list[i].tad["TCO"]["BEV"] <= self.truck_agent_object_list[i].tad["TCO"]["DV"])
            if if_BEV:
                self.BEV_sales[segment][model_year] += sale
                self.BEV_incentive[segment][model_year] += sale * self.truck_agent_object_list[i].tad["BEV_incentive"]
                for t in range(0, lifetime):
                    self.BEV_stocks[segment][model_year + t] += sale 
                    self.BEV_VMT[segment][model_year + t] += sale * annual_mile_avg
                    self.electricity[segment][model_year + t] += sale * self.truck_agent_object_list[i].tad["annual_average_energy"]["BEV"] * Evaluation.kWhperDGE
            else:
                self.DV_sales[segment][model_year] += sale
                for t in range(0, lifetime):
                    self.DV_stocks[segment][model_year + t] += sale
                    self.DV_VMT[segment][model_year + t] += sale * annual_mile_avg
                    self.diesel[segment][model_year + t] += sale * self.truck_agent_object_list[i].tad["annual_average_energy"]["DV"]
        print("    calculating infrastructure incentive")
        for s in self.segments:        
            for t in range(self.start_year, self.end_year + 1):
                self.infrastructure_incentive[s][t] = self.electricity[s][t] / Evaluation.kWhperDGE * self.infrastructure.capital[s][t] * self.policy.charging_incentive[s][t]
        print("    calculating GHG emissions")
        for s in self.segments:
            for t in range(self.start_year, self.end_year + 1):
                self.carbon_emissions[s][t] = self.electricity[s][t] * self.infrastructure.carbon_intensity["electricity"][t] + \
                self.diesel[s][t] * self.infrastructure.carbon_intensity["diesel"][t]
                
    def print_agent_results(self):
        temp_df_list = []
        for i in range(0, len(self.truck_agent_object_list)):
            temp_df_list.append(self.truck_agent_object_list[i].tad)
        temp_df = pd.DataFrame.from_dict(temp_df_list)[list (temp_df_list[0].keys())] 
        temp_df.to_csv(dirname + "/temp/agent_year.csv", header = True, index = None)
            
        
    def generate_results(self):
        self.print_agent_results()
        ans_list = []
        for s in self.segments:
            for t in range(2020, self.end_year + 1):
                record = {"Segment" : s,
                          "Year" : t,
                          "BEV_sales" : self.BEV_sales[s][t],
                          "DV_sales" : self.DV_sales[s][t],
                          "BEV_stock" : self.BEV_stocks[s][t],
                          "DV_stock" : self.DV_stocks[s][t],
                          "BEV_VMT" : self.BEV_VMT[s][t],
                          "DV_VMT" : self.DV_VMT[s][t],
                          "diesel" : self.diesel[s][t],
                          "electricity" : self.electricity[s][t],
                          "BEV_incentive" : self.BEV_incentive[s][t],
                          "infrastructure_incentive" : self.infrastructure_incentive[s][t],
                          "carbon_emissions" : self.carbon_emissions[s][t]
                        }
                ans_list.append(record)
        ans_df = pd.DataFrame.from_dict(ans_list)[list (ans_list[0].keys())] 
        ans_df.to_csv(dirname + "/results/" + self.scenario + "_results.csv", header = True, index = None)
    

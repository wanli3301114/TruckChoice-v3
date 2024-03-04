import pandas as pd
import os
dirname = os.path.dirname(__file__)

df = pd.read_excel('scenario.xlsx', sheet_name=None)  

folder_dict = {"input" : "/",
               "segments" : "/",
               "capital" : "/infrastructure/",
               "carbon_intensity" : "/infrastructure/",
               "fuel_prices" : "/infrastructure/",
               "BEV_charging_power" : "/infrastructure/",
               "BEV_queue_time" : "/infrastructure/",
               "BEV_incentive" : "/policy/",
               "charging_incentive" : "/policy/",
               "BEV_consumption" : "/vehicle/",
               "BEV_price" : "/vehicle/",
               "DV_consumption" : "/vehicle/",
               "DV_idling_consumption" : "/vehicle/",
               "BEV_range" : "/vehicle/",
               "DV_price" : "/vehicle/"
        }

for key in df.keys(): 
    df[key].to_csv(dirname + folder_dict[key] + '%s.csv' %key, header = True, index = None)

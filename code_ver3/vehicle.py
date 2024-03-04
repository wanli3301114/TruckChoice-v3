'''
class containing all vehicle related parameters
-vehicle price $/vehicle
-fuel consumption  DGE/mile

'''

import pandas as pd
import os
pd.set_option('max_columns', None)

dirname = os.path.dirname(__file__)

class Vehicle:

    def __init__(self, scenario):
        #$/DGE
        self.BEV_prices = pd.read_csv(dirname + "/input/" + scenario + "/vehicle/BEV_price.csv").set_index("Year").to_dict('series')
        self.DV_prices = pd.read_csv(dirname + "/input/" + scenario + "/vehicle/DV_price.csv").set_index("Year").to_dict('series')
        self.BEV_consumption = pd.read_csv(dirname + "/input/" + scenario + "/vehicle/BEV_consumption.csv").set_index("Year").to_dict('series')
        self.DV_consumption = pd.read_csv(dirname + "/input/" + scenario + "/vehicle/DV_consumption.csv").set_index("Year").to_dict('series')
        self.DV_idling_consumption = pd.read_csv(dirname + "/input/" + scenario + "/vehicle/DV_idling_consumption.csv").set_index("Year").to_dict('series')
        self.BEV_range = pd.read_csv(dirname + "/input/" + scenario + "/vehicle/BEV_range.csv").set_index("Year").to_dict('series')
        
    
        '''
        units:
            BEV_prices
                $
            DV_prices
                $
            BEV_consumption
                DGE/mile
            DV_consumption
                DGE/mile
            DV_idling_consumption
                DGE/hr
            BEV_range
                miles
        '''


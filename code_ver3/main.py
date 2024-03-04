from truck_segment_generator import Truck_Segment_Generator
from evaluation import Evaluation
import pandas as pd
pd.set_option('display.max_rows', None)


def truckChoice(seed, scenario):
    print("Generating truck segments using Monte Carlo Simulation...")
    
    generator = Truck_Segment_Generator(seed, scenario)
    monte_carlo_segments = generator.generate_samples_for_all_segments()
    
    print("Creating truck choice model...")
    truck_choice_model = Evaluation(2005, 2035, monte_carlo_segments, scenario)
    print("Simulation begins...")
    truck_choice_model.calculate()
    print("saving results.")
    truck_choice_model.generate_results()


def main():
    #truckChoice(5, "base")
    truckChoice(5, "no_incentive")
    #truckChoice(5, "high_tech")
    truckChoice(5, "high_tech_hybrid_sleeper")

main()


import pandas as pd
import UCF_Visualizations
from UCF_Utils import read_and_combine_jsons
from Building import Building
import argparse

# data_dir = "./data"
# data_csv = "data.csv"
variables_file = "./output/ucf_variables.csv"

parser = argparse.ArgumentParser()
parser.add_argument("-d", '--data_directory', action='store', type=str,
                    help='Directory that contains *_messages.json fiels')
parser.add_argument('data_file', action='store', type=str,
                    help='The CSV file which contains all data from json files')
args = parser.parse_args()

if args.data_directory:
    df = read_and_combine_jsons(args.data_directory, args.data_file)
# Loading data #
df = pd.read_csv(args.data_file)

df['msg.timestamp'] = pd.to_datetime(df['msg.timestamp'])

falcon = Building(bname='falcon', zones_file='./building_info/falcon_zoning.csv',
                  victims_file='./building_info/falcon_victims_coords.csv',
                  sizes=(5, 9), limits=[-2110, -2020, 141, 193])
sparky = Building(bname='sparky', zones_file='./building_info/sparky_zoning.csv',
                  victims_file='./building_info/sparky_victims_coords.csv',
                  sizes=(5, 6), limits=[-2160, -2100, 151, 200])

UCF_Visualizations.building_animate_traces(df, trial_id=11, building=falcon,
                                           out_file="./output/%s_trial_%d.gif" % (falcon.bname, 11))

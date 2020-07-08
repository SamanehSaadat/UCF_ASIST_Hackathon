from UCF_Utils import read_and_combine_jsons
import UCF_TemporalVariables
import UCF_PerformanceVariables
import UCF_SpatialVariables
from Building import Building
import pandas as pd
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

variable_dfs = []

# EXTRACTING UCF TEMPORAL VARIABLES #
triaging_time_df = UCF_TemporalVariables.extract_event_time(df,
                                                            event_type='Event:Triage', state_col='data.triage_state',
                                                            end_states=['SUCCESSFUL', 'UNSUCCESSFUL'])
variable_dfs.append(triaging_time_df)

sprinting_time_df = UCF_TemporalVariables.extract_event_time(df,
                                                             event_type='Event:PlayerSprinting',
                                                             state_col='data.sprinting', end_states=[False])
variable_dfs.append(sprinting_time_df)

navigating_time_df = UCF_TemporalVariables.extract_navigating_time(df)
variable_dfs.append(navigating_time_df)

# EXTRACTING PERFORMANCE VARIABLES #
saved_victims_df = UCF_PerformanceVariables.extract_saved_victims(df)
variable_dfs.append(saved_victims_df)


# EXTRACTING UCF SPACIAL VARIABLES #
falcon = Building(bname='falcon', zones_file='./building_info/falcon_zoning.csv',
                  trials=['4', '7', '9', '11', '12', '15'])
sparky = Building(bname='sparky', zones_file='./building_info/sparky_zoning.csv',
                  trials=['3', '6', '8', '10', '13', '14'])

falcon_spacial_variables_df = UCF_SpatialVariables.building_spatial_variables(df, falcon)
sparky_spacial_variables_df = UCF_SpatialVariables.building_spatial_variables(df, sparky)
spacial_variables_df = pd.concat([falcon_spacial_variables_df, sparky_spacial_variables_df])
variable_dfs.append(spacial_variables_df)

variables = pd.concat(variable_dfs, axis=1)
variables.to_csv(variables_file)

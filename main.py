from UCF_Utils import read_and_combine_jsons
import UCF_TemporalVariables
import UCF_PerformanceVariables
import UCF_SpacialVariables
import pandas as pd

data_dir = "./data"
data_csv = "data.csv"
variables_file = "UCF_variables.csv"


# df = read_and_combine_jsons(data_dir, data_csv)

### Loading data ###
df = pd.read_csv(data_csv)
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
map_trials = {
    'sparky': ['3', '6', '8', '10', '13', '14'],
    'falcon': ['4', '7', '9', '11', '12', '15']
}
map_zones_file = {
    'sparky': './map_info/sparky_zoning.csv',
    'falcon': './map_info/falcon_zoning.csv'
}

dfs = []
for asist_map, trials in map_trials.items():
    map_spacial_variables_df = UCF_SpacialVariables.map_spacial_variables(df, trials, map_zones_file[asist_map])
    print(map_spacial_variables_df)
    dfs.append(map_spacial_variables_df)
spacial_variables_df = pd.concat(dfs)
variable_dfs.append(spacial_variables_df)

variables = pd.concat(variable_dfs, axis=1)
variables.to_csv(variables_file)

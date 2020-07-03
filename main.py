from UCF_Utils import read_and_combine_jsons
import UCF_TemporalVariables
import pandas as pd

data_dir = "./data"
data_csv = "data.csv"


# df = read_and_combine_jsons(data_dir, data_csv)

### Loading data ###
df = pd.read_csv(data_csv)
df['msg.timestamp'] = pd.to_datetime(df['msg.timestamp'])

variable_dfs = []

### EXTRACTING UCF TEMPORAL VARIABLES ###
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

variables = pd.concat(variable_dfs, axis=1)
print(variables)
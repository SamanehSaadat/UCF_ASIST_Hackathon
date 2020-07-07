import pandas as pd
import UCF_Visualizations
import Building

data_csv = "data.csv"

# Loading data #
df = pd.read_csv(data_csv)
df['msg.timestamp'] = pd.to_datetime(df['msg.timestamp'])

falcon = Building.Building(bname='falcon', zones_file='./building_info/falcon_zoning.csv',
                           victims_file='./building_info/falcon_victims_coords.csv',
                           sizes=(5, 9), limits=[-2110, -2020, 141, 193])
sparky = Building.Building(bname='sparky', zones_file='./building_info/sparky_zoning.csv',
                           victims_file='./building_info/sparky_victims_coords.csv',
                           sizes=(5, 6), limits=[-2160, -2100, 151, 200])

UCF_Visualizations.building_animate_traces(df, trial_id=11, building=falcon,
                                           out_file="./output/%s_trial_%d.gif" % (falcon.bname, 11))

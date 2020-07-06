import pandas as pd

data_csv = "data.csv"

# Loading data #
df = pd.read_csv(data_csv)
df['msg.timestamp'] = pd.to_datetime(df['msg.timestamp'])

map_zones_file = {
    'sparky': './map_info/sparky_zoning.csv',
    'falcon': './map_info/falcon_zoning.csv'
}

map_victims_file = {
    'sparky': './map_info/sparky_victims_coords.csv',
    'falcon': './map_info/falcon_victims_coords.csv'
}



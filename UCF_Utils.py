import pandas as pd
import json
from pandas import json_normalize
import os


def read_and_combine_jsons(directory, out_file=None):
    """
        Reads all files in the directory, combines them and saves the result in the out_file.
        I has been assumed that all the files in the directory are json files.
        Records related to one json file can be recognized by their trial_id.
    """
    def json2df(f):
        data = []
        with open(f) as fin:
            for line in fin:
                data.append(json.loads(line))
        df = json_normalize(data)
        df['trial_id'] = str(int(f.split('_')[-2]))
        df['@timestamp'] = pd.to_datetime(df['@timestamp'])
        df = df.sort_values(by='@timestamp')
        trial_times = df[df['header.message_type'] == 'trial']['@timestamp'].tolist()
        if len(trial_times) > 0:
            [trial_start, trial_end] = trial_times
            df = df[(df['@timestamp'] > trial_start) & (df['@timestamp'] < trial_end)]
        mission_times = df[df['msg.sub_type'] == 'Event:MissionState']['@timestamp'].tolist()
        if len(mission_times) > 0:
            mission_start = mission_times[0]
            df = df[df['@timestamp'] > mission_start]
        return df

    files = os.listdir(directory)
    dfs = []
    for f in files:
        print("Reading", f)
        dfs.append(json2df(directory + "/" + f))
    print("Combining files!")
    df = pd.concat(dfs)
    if out_file:
        df.to_csv(out_file)
    return df

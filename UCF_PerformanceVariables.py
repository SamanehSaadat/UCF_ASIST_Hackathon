import pandas as pd
from collections import Counter


def extract_saved_victims(df):
    event_df = df[df['msg.sub_type'] == 'Event:Triage']
    grouped = event_df.groupby('trial_id')
    saved_victim_data = []
    for ti, grp in grouped:
        successful_triages = grp[grp['data.triage_state'] == 'SUCCESSFUL']
        saved_victims = successful_triages['data.color'].tolist()
        triage_order = "".join([s[0] for s in saved_victims])
        counter = Counter(saved_victims)
        saved_victim_data.append([ti, counter['Green'], counter['Yellow'], triage_order])
    saved_victims_df = pd.DataFrame.from_records(saved_victim_data,
                                                 columns=['trial_id', 'green_victims_saved_count',
                                                          'yellow_victims_saved_count', 'triaging_order'])
    return saved_victims_df.set_index('trial_id')

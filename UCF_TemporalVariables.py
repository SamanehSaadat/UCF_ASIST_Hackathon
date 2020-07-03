import pandas as pd


def extract_event_time(df, event_type, state_col, end_states):
    """
    Calculate the time spent performing an event type for each trial
    :param df: combined json file in pandas DataFrame format
    :param event_type: 'msg.sub_type' values in json files (e.g. 'Event:Triage')
    :param state_col: the column that determines the state of the event (e.g. 'data.triage_state')
    :param end_states: there is a record for the event when the event starts and ends. end_states is a list of states
    that represent the ending of an event. (e.g. ['SUCCESSFUL', 'UNSUCCESSFUL'] for triage)
    :return: a pandas DataFrame containing trial id and time spent performing the event in that trial
    """
    event_df = df[df['msg.sub_type'] == event_type]
    grouped = event_df.groupby('trial_id')
    trial_event_times = []
    for ti, grp in grouped:
        grp['time_diff'] = grp['msg.timestamp'].diff()
        trial_event_df = grp[grp[state_col].isin(end_states)]
        event_time = trial_event_df['time_diff'].sum()
        trial_event_times.append([ti, event_time.total_seconds()])
    event_col_name = event_type + "_time"
    event_time_df = pd.DataFrame.from_records(trial_event_times, columns=['trial_id', event_col_name])
    return event_time_df.set_index('trial_id')


def extract_navigating_time(df):
    """
    Calculate navigating time for each trial. Navigating is detected by observing non-zero movement along x or z axes
    :param df: combined json file in pandas DataFrame format
    :return: a pandas DataFrame containing trial id and time spent navigating    in that trial
    """
    nav_df = df[['trial_id', 'msg.timestamp', 'data.x', 'data.z']].dropna()
    grouped = nav_df.groupby('trial_id')
    trial_navtime = []
    for ti, grp in grouped:
        grp['xdiff'] = grp['data.x'].diff()
        grp['zdiff'] = grp['data.z'].diff()
        grp['xmove'] = grp['xdiff'] != 0
        grp['zmove'] = grp['zdiff'] != 0
        grp['nav'] = grp['xmove'] & grp['zmove']
        grp.dropna(subset=['msg.timestamp'])
        nav = grp['nav'].tolist()
        t = grp['msg.timestamp'].tolist()
        nav_time = 0
        i = 1
        while i < len(nav):
            if nav[i]:
                start = i - 1
                end = i
                i += 1
                while i < len(nav) and nav[i]:
                    end += 1
                    i += 1
                nav_time += (t[end] - t[start]).total_seconds()
            else:
                i += 1
        trial_navtime.append([ti, nav_time])
    nav_df = pd.DataFrame.from_records(trial_navtime, columns=['trial_id', 'navigating_time'])
    return nav_df.set_index('trial_id')

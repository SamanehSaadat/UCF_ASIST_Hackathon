import pandas as pd
from datetime import timedelta


def assign_zone(player_x, player_z, zone_coords):
    """
    Based on coordination of the player, finds which zone is the player in
    :param player_x: data.x
    :param player_z: data.z
    :param zone_coords: coordinations of all zones in the map
    :return: the zone number if the x and z are within the map zones and -1 if not
    """
    for zone in zone_coords:
        [zone_number, xtl, xbr, ztl, zbr] = zone
        if (xbr <= player_x <= xtl) and (ztl <= player_z <= zbr):
            return zone_number
    return -1


def zone_visits_revisits(df, zones, experiment):
    zone_coords = zones[['Zone Number', 'Xcoords-TopLeft', 'XCoords-BotRight',
                         'Zcoords-TopLeft', 'ZCoords-BotRight']].values.tolist()

    df['zone'] = df.apply(lambda row: assign_zone(row['data.x'], row['data.z'], zone_coords), axis=1)
    df['zone'] = df['zone'].astype(int)

    df = df.loc[df['zone'] != df['zone'].shift()]

    zone_visits_count = pd.DataFrame(df['zone'].value_counts())
    zone_visits_count = zone_visits_count.drop(-1)

    zone_visits = zone_visits_count != 0
    zone_revisits = zone_visits_count > 1

    total_zones_count = len(zone_coords)

    percent_zone_visited = (zone_visits.values.sum() / total_zones_count)
    percent_zone_revisited = (zone_revisits.values.sum() / total_zones_count)

    visit_revisit_percent_df = pd.DataFrame.from_records([[percent_zone_visited, percent_zone_revisited]],
                                                         columns=["percent_zone_visited_" + experiment,
                                                                  "percent_zone_revisited_" + experiment])

    return visit_revisit_percent_df


def map_spacial_variables(df, map_trials, map_zones_file):
    map_df = df[df['trial_id'].isin(map_trials)]
    map_zones = pd.read_csv(map_zones_file)

    map_df.dropna(subset=['data.x', 'data.z'], inplace=True)
    grouped = map_df.groupby('trial_id')
    dfs = []
    for ti, trial_df in grouped:
        res_df_simple = zone_visits_revisits(trial_df, map_zones, "simple")

        map_zones['total_victims'] = map_zones['Number of Green'] + map_zones['Number of Yellow']
        map_zones_with_victim = map_zones[map_zones['total_victims'] > 0]
        res_df_with_victim = zone_visits_revisits(trial_df, map_zones_with_victim, "with_victim")

        map_rooms = map_zones[map_zones['Zone Type'] == 3]
        res_df_rooms = zone_visits_revisits(map_df, map_rooms, "rooms")

        map_rooms = map_zones[map_zones['Zone Type'] == 1]
        res_df_hallways = zone_visits_revisits(map_df, map_rooms, "hallways")

        map_rooms = map_zones[map_zones['Zone Type'] == 2]
        res_df_entrances = zone_visits_revisits(map_df, map_rooms, "entrances")

        five_min_threshold = trial_df['msg.timestamp'].min() + timedelta(minutes=5)
        first_5min_df = trial_df[trial_df['msg.timestamp'] < five_min_threshold]
        second_5min_df = trial_df[trial_df['msg.timestamp'] >= five_min_threshold]
        res_df_first_5min = zone_visits_revisits(first_5min_df, map_zones, "first_5min")
        res_df_second_5min = zone_visits_revisits(second_5min_df, map_zones, "second_5min")

        trial_spacial_df = pd.concat([res_df_simple, res_df_with_victim,
                                      res_df_rooms, res_df_hallways, res_df_entrances,
                                      res_df_first_5min, res_df_second_5min],
                                     axis=1)
        trial_spacial_df['trial_id'] = ti
        dfs.append(trial_spacial_df.set_index('trial_id'))
    spacial_variables_df = pd.concat(dfs)
    return spacial_variables_df



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


def building_spacial_variables(df, building_trials, building_zones_file):
    building_df = df[df['trial_id'].isin(building_trials)]
    building_zones = pd.read_csv(building_zones_file)

    building_df.dropna(subset=['data.x', 'data.z'], inplace=True)
    grouped = building_df.groupby('trial_id')
    dfs = []
    for ti, trial_df in grouped:
        res_df_simple = zone_visits_revisits(trial_df, building_zones, "simple")

        building_zones['total_victims'] = building_zones['Number of Green'] + building_zones['Number of Yellow']
        building_zones_with_victim = building_zones[building_zones['total_victims'] > 0]
        res_df_with_victim = zone_visits_revisits(trial_df, building_zones_with_victim, "with_victim")

        building_rooms = building_zones[building_zones['Zone Type'] == 3]
        res_df_rooms = zone_visits_revisits(building_df, building_rooms, "rooms")

        building_rooms = building_zones[building_zones['Zone Type'] == 1]
        res_df_hallways = zone_visits_revisits(building_df, building_rooms, "hallways")

        building_rooms = building_zones[building_zones['Zone Type'] == 2]
        res_df_entrances = zone_visits_revisits(building_df, building_rooms, "entrances")

        five_min_threshold = trial_df['msg.timestamp'].min() + timedelta(minutes=5)
        first_5min_df = trial_df[trial_df['msg.timestamp'] < five_min_threshold]
        second_5min_df = trial_df[trial_df['msg.timestamp'] >= five_min_threshold]
        res_df_first_5min = zone_visits_revisits(first_5min_df, building_zones, "first_5min")
        res_df_second_5min = zone_visits_revisits(second_5min_df, building_zones, "second_5min")

        trial_spacial_df = pd.concat([res_df_simple, res_df_with_victim,
                                      res_df_rooms, res_df_hallways, res_df_entrances,
                                      res_df_first_5min, res_df_second_5min],
                                     axis=1)
        trial_spacial_df['trial_id'] = ti
        dfs.append(trial_spacial_df.set_index('trial_id'))
    spacial_variables_df = pd.concat(dfs)
    return spacial_variables_df



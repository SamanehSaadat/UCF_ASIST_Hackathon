import pandas as pd
import UCF_SpatialVariables
import numpy as np
from datetime import timedelta
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt


def building_animate_traces(df, trial_id, building, out_file):
    """

    :param df:
    :param trial_id:
    :param building:
    :param out_file:
    :return:
    """
    building_victims = pd.read_csv(building.victims_file)
    building_zones = pd.read_csv(building.zones_file)
    df.dropna(subset=['data.x', 'data.z'], inplace=True)
    trial_df = df[df['trial_id'] == trial_id]
    animate_traces(trial_df, building_zones, building_victims, building.sizes, building.limits, out_file)


def animate_traces(df, zones, victims, building_size, building_limits, out_file='animation.gif'):
    zone_coords = zones[['Zone Type Description', 'Xcoords-TopLeft', 'XCoords-BotRight',
                         'Zcoords-TopLeft', 'ZCoords-BotRight']].values.tolist()

    df['zone'] = df.apply(lambda row: UCF_SpatialVariables.assign_zone(row['data.x'], row['data.z'], zone_coords),
                          axis=1)

    def plot_animate(x1, y1, x2, y2, ax, fig, point_pre_frame=20, c1='tab:blue', c2='tab:orange', m1='o', m2='x',
                     interval=1):
        scat1 = ax.scatter(x1, y1, s=60, c=c1, marker=m1)
        scat2 = ax.scatter(x2, y2, s=60, c=c2, marker=m2)
        index_to_start_second = len(x1)

        def animate(i):
            j = (i + 1) * point_pre_frame
            if j < index_to_start_second:
                X = np.c_[x1[:min(len(x1), j)], y1[:min(len(y1), j)]]
                scat1.set_offsets(X)
                X2 = np.c_[x2[:0], y2[:0]]
                scat2.set_offsets(X2)
                return scat1, scat2
            else:
                X1 = np.c_[x1[:index_to_start_second], y1[:index_to_start_second]]
                scat1.set_offsets(X1)
                X2 = np.c_[x2[:min(len(x2), j - index_to_start_second)], y2[:min(len(y2), j - index_to_start_second)]]
                scat2.set_offsets(X2)
                return scat1, scat2

        anim = FuncAnimation(
            fig, animate, interval=interval, frames=(len(x1) + len(x2)) // point_pre_frame)
        return anim

    def plot_victims(victims):
        yellows = victims[victims['vcolor'] == 'Y']
        plt.scatter(yellows['z'], yellows['x'], color='y', marker='s', s=80)
        greens = victims[victims['vcolor'] == 'G']
        plt.scatter(greens['z'], greens['x'], color='g', marker='s', s=80)

    fig, ax = plt.subplots(figsize=building_size, dpi=100)
    plot_victims(victims)

    five_min_threshold = df['msg.timestamp'].min() + timedelta(minutes=5)
    first_5min_df = df[df['msg.timestamp'] < five_min_threshold]
    second_5min_df = df[df['msg.timestamp'] >= five_min_threshold]

    anim = plot_animate(first_5min_df['data.z'], first_5min_df['data.x'],
                        second_5min_df['data.z'], second_5min_df['data.x'], ax, fig)
    ax.set_ylim(building_limits[0], building_limits[1])
    ax.set_xlim(building_limits[2], building_limits[3])

    anim.save(out_file, writer='imagemagick')

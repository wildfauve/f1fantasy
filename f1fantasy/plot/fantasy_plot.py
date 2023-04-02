import matplotlib.pyplot as plt
import matplotlib.path as mpath
import numpy as np
from matplotlib.lines import Line2D

from f1fantasy import dataframe

markers = Line2D.filled_markers

def rank_plot(file, df):
    rank_df = dataframe.race_rank(df)
    _draw_rank_plot(file, rank_df, gps=df.columns[1:])

def total_score_plot(file, df):
    _draw_total_score_plot(file, df, gps=df.columns[1:])


def _draw_rank_plot(file, rank_df, gps):
    np_arr = rank_df.to_numpy()
    races = rank_df.columns[1:]

    fig, ax = _plot_figure(gps)

    ax.set_yticks(range(0, 16))
    ax.set_xticklabels(gps)    # ax.axis([1, 22, 1, 15])
    for team_rank in np_arr:
        ax.plot(races, team_rank[1:], label=team_rank[0], marker=_to_marker(team_rank[0]))
    ax.set_ylabel('Team Rank')  # Add a y-label to the axes.
    ax.set_title("Team Rank Per GP")  # Add a title to the axes.
    ax.legend(bbox_to_anchor=(1.1, 1.05), fancybox=True, shadow=True)  # Add a legend.
    fig.savefig(file)


def _draw_total_score_plot(file, df, gps):
    np_arr = df.to_numpy()
    races = df.columns[1:]

    fig, ax = _plot_figure(gps)

    for team_race_scores in np_arr:
        ax.plot(races, team_race_scores[1:], label=team_race_scores[0], marker=_to_marker(team_race_scores[0]))
    ax.set_ylabel('Team Total Scores')  # Add a y-label to the axes.
    ax.set_title("Team Total Accumulating Scores Per GP")  # Add a title to the axes.
    ax.legend(bbox_to_anchor=(1.1, 1.05), fancybox=True, shadow=True)  # Add a legend.
    fig.savefig(file)


def _plot_figure(gps):
    fig, ax = plt.subplots(figsize=(15, 7), layout='constrained')
    ax.set_xticks(range(0, len(gps)))
    ax.set_xticklabels(gps)
    ax.set_xlabel('GPs')  # Add an x-label to the axes.
    return fig, ax


def _to_marker(team):
    return markers[hash(team) % 16]

def _markers2():
    star = mpath.Path.unit_regular_star(6)
    circle = mpath.Path.unit_circle()
    # concatenate the circle with an internal cutout of the star
    cut_star = mpath.Path(
        vertices=np.concatenate([circle.vertices, star.vertices[::-1, ...]]),
        codes=np.concatenate([circle.codes, star.codes]))

    return {'star': star, 'circle': circle, 'cut_star': cut_star}

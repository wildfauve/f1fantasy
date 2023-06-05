from typing import List, Tuple

from rich.table import Table

from f1fantasy.adapter import discord

from . import console


def plot_to_channel(file: str, channel: bool, position: str):
    if channel == "to-discord":
        _send_to_discord(file, _plot_description(position))
    pass


def _plot_description(position):
    if position:
        return "ranking-plot"
    return 'totals-plot'

def _send_to_discord(file, description):
    discord.send_attachment(msg_title="Fantasy Plot",
                            file_path=file,
                            description=description,
                            file_name="plot.png")
    pass

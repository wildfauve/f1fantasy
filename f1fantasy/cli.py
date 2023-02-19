import click

from f1fantasy.command import graph_command
from f1fantasy.f1_seasons import season

def seasons():
    return [str(season_module.season) for season_module in season.seasons]

@click.group()
def cli():
    pass


# @click.command()
@click.option("--season", "-s",
              type=click.Choice(seasons()),
              help="Pick a Seasion")
@click.command()
def generate_graph(season):
    """
    Generates the graph at the standard repo location.
    """
    graph_command.generate_graph(int(season))
    pass


@click.command()
def teams():
    """
    Displays the teams and their members
    """
    graph_command.display_teams()
    pass



cli.add_command(generate_graph)
cli.add_command(teams)

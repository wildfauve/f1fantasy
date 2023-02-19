import click

from f1fantasy import command
from f1fantasy import initialiser



@click.group()
def cli():
    pass

@click.option('--team', '-t')
@click.option('--members', '-m', multiple=True)
@click.option('--principle', '-p')
@click.command()
def create(team, members, principle):
    """
    Creates a new Fantasy Team with members
    """
    command.create_team(team, members, principle)
    pass


cli.add_command(create)

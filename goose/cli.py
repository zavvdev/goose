import click
from goose.commands.goose import goose
from goose.commands.rush import rush as goose_rush

@click.group()
def cli():
  goose()

@cli.command()
@click.argument('ftp_adress')
def rush(ftp_adress):
  goose_rush(ftp_adress)
import click

from src.server import server_main


@click.command()
@click.option("--ip", help="Host ip address")
@click.option("--port", help="Host port")
def main(ip, port):
    server_main(ip, port)

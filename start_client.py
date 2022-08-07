import click

from src.client import client_main


@click.command()
@click.option("--ip", help="Server ip address")
@click.option("--port", help="Server port")
def main(ip, port):
    uri = f"ws://{ip}:{port}"
    client_main(uri)


if __name__ == "__main__":
    main()

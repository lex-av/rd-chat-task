import asyncio

import click

from server.server_utils import run_server


@click.command()
@click.option("--ip", help="Host ip address")
@click.option("--port", help="Host port")
def main(ip, port):
    try:
        print("Server started ...")
        asyncio.run(run_server(ip, port))

    except KeyboardInterrupt:
        print("stopping server")
        exit()


if __name__ == "__main__":
    main()

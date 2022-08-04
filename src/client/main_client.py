import asyncio

import websockets


async def register(server_ws):
    """
    Tries to register on server by given username
    :param server_ws: Selected server's websocket
    :return: None
    """

    while True:
        user_name = input("Enter your username ")
        await server_ws.send(user_name)
        user_name_answer = await server_ws.recv()

        if bool(int(user_name_answer)):
            print("Username registered")
            break
        else:
            print("Username is already in use")


async def choose_mode(server_ws):
    """
    User chooses between connection to another user or to
    stand by a connection from another user

    :param server_ws: Selected server's websocket
    :return: None
    """

    while True:
        mode = input(
            "Enter your desired state (0 - await for connection from another user or\n 1 for "
            "connection to another user) "
        )

        mode_int = int(mode)  # try needed here

        if mode_int != 0 and mode_int != 1:
            print("Wrong option selected. Try again")
            continue
        else:
            await server_ws.send(mode)
            break


async def connect():
    """
    Main client's function to register on server and
    send messages to another clients
    """

    uri = "ws://localhost:2024"

    async with websockets.connect(uri) as websocket:
        await register(websocket)
        await choose_mode(websocket)


if __name__ == "__main__":
    print("Client started ...")
    asyncio.run(connect())

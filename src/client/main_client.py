import asyncio
import json

import websockets


async def register(server_ws):
    """
    Tries to register on server by given username
    :param server_ws: Selected server's websocket
    :return: Accepted username
    """

    while True:
        user_name = input("Enter your username ")
        await server_ws.send(user_name)
        user_name_answer = await server_ws.recv()

        if bool(int(user_name_answer)):
            print("Username registered")
            return user_name
        else:
            print("Username is already in use")


async def choose_mode(server_ws) -> bool:
    """
    User chooses between connection to another user or to
    stand by a connection from another user

    :param server_ws: Selected server's websocket
    :return: User state mod index in str
    """

    while True:
        mode = input("Choose initialization mode. For active mode type 1\n" "for passive mode type 0 ")

        mode_int = int(mode)  # try needed here

        if mode_int != 0 and mode_int != 1:
            print("Wrong option selected. Try again")
            continue
        else:
            break

    if bool(mode_int):
        destination_username = input("Enter destination username")
        json_info = json.dumps({"mode": "active", "username": destination_username})
    else:
        source_username = input("Enter source username")
        json_info = json.dumps({"mode": "passive", "username": source_username})
        print("Passive mode set")

    while True:
        await server_ws.send(json_info)
        server_answer = await server_ws.recv()
        if bool(int(server_answer)):
            print("Active mode set")
            break
        else:
            new_username = input("Given destination username is not registered. Try again ")
            json_info = json.dumps({"mode": "active", "username": new_username})
            await server_ws.send(json_info)

    return True if mode_int == 1 else False


async def messaging_handler_active(server_ws):
    """

    :param server_ws:
    :return:
    """
    while True:
        try:
            message = input(">>> ")
            await server_ws.send(message)
            new_msg = await server_ws.recv()
            print(new_msg)
        except KeyboardInterrupt:
            break


async def messaging_handler_passive(server_ws):
    """

    :param server_ws:
    :return:
    """
    while True:
        try:
            new_msg = await server_ws.recv()
            print(new_msg)
            message = input(">>> ")
            await server_ws.send(message)
        except KeyboardInterrupt:
            break


async def connect():
    """
    Main client's function to register on server and
    send messages to another clients
    """

    uri = "ws://localhost:2024"

    async with websockets.connect(uri, ping_interval=None) as websocket:
        await register(websocket)
        user_mode = await choose_mode(websocket)
        print(user_mode)

        if user_mode:
            print("active")
            await messaging_handler_active(websocket)
        else:
            print("passive")
            await messaging_handler_passive(websocket)


if __name__ == "__main__":
    print("Client started ...")
    asyncio.run(connect())

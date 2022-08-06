import asyncio
import logging

import websockets
from websockets import WebSocketServerProtocol

USERS_MAPPING = {}  # Maps username to it's websocket

logging.basicConfig(
    format="%(message)s",
    level=logging.DEBUG,
)


async def add_user(user_websocket: WebSocketServerProtocol, user_name: str, users_mapping: dict) -> bool:
    """
    Adds new user to user mapper. Returns True if user was
    added and False otherwise. Prevents adding username, that
    already exists in mapper

    :param user_websocket: Connected user's websocket
    :param user_name: Username, given by user
    :param users_mapping: Server mapping username->websocket
    :return: bool
    """

    if user_name in users_mapping:
        return False
    else:
        users_mapping[user_name] = user_websocket
        return True


def remove_user(user_name: str, users_mapping: dict):
    """

    :param user_name:
    :param users_mapping:
    :return:
    """

    users_mapping.pop(user_name)


async def register_user(user_ws: WebSocketServerProtocol, users_mapping: dict) -> str:
    """
    Allows user to register on server by entering his own username. Gets
    username from connected user. Uses codes "1" and "0" to inform user
    about registration status
    :param user_ws: Connected user's websocket
    :param users_mapping: Server mapping from username to it's websocket
    :return: None
    """

    while True:
        current_username = await user_ws.recv()
        add_user_ok = await add_user(user_ws, current_username, users_mapping)

        if add_user_ok:
            await user_ws.send("1")
            print("users: ", users_mapping)  # DEBUG, DELETE LATER
            return current_username
        else:
            await user_ws.send("0")


async def pair_users(user_ws: WebSocketServerProtocol, users_mapping: dict) -> str:
    """

    :param user_ws:
    :param users_mapping:
    :return:
    """

    while True:
        destination_username = await user_ws.recv()

        if destination_username in users_mapping.keys():
            await user_ws.send("1")
            return destination_username
        else:
            await user_ws.send("0")


async def user_connection_handler(user_websocket: WebSocketServerProtocol):
    """
    Main server handler for incoming connections and
    messages routing

    :param user_websocket: connected user websocket
    """

    try:
        sender = await register_user(user_websocket, USERS_MAPPING)
        recipient = await pair_users(user_websocket, USERS_MAPPING)

        try:
            while 1:
                sender_data = await user_websocket.recv()

                if sender_data == ":quit:" or len(USERS_MAPPING) < 2:
                    raise websockets.ConnectionClosedOK(1000, 1000)

                sender_msg = f"[{sender}] " + sender_data
                msg_to_sender = "[server] Message sent to user"

                sender_ws = USERS_MAPPING[sender]
                recipient_ws = USERS_MAPPING[recipient]

                await recipient_ws.send(sender_msg)
                await sender_ws.send(msg_to_sender)

        except websockets.ConnectionClosedOK:  # Handle user disconnect while messaging
            remove_user(sender, USERS_MAPPING)
            if len(USERS_MAPPING) > 1:  # Proper user quit and disconnect
                await USERS_MAPPING[recipient].send("[server] User left")
                print(sender, " disconnected")

    except websockets.ConnectionClosedError:  # Handle user register fail
        print("User connection failed")


async def main():
    async with websockets.serve(user_connection_handler, "localhost", 2024, ping_interval=None):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    print("server started ...")
    print("awaiting")
    asyncio.run(main())

import asyncio
import logging

import websockets

USERS_MAPPING = {}  # Maps username to it's websocket

logger = logging.getLogger("websockets")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


async def add_user(user_websocket, user_name: str, users_mapping: dict) -> bool:
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


async def remove_user(user_name: str, users_mapping: dict):
    """

    :param user_name:
    :param users_mapping:
    :return:
    """

    users_mapping.pop(user_name)


async def register_user(user_ws, users_mapping: dict):
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


async def user_connection_handler(user_websocket):
    """
    Main server handler for incoming connections and
    messages routing

    :param user_websocket: connected user websocket
    """

    try:
        sender = await register_user(user_websocket, USERS_MAPPING)

        try:
            while 1:
                # Broadcast received message to all connected users except sender
                new_msg = await user_websocket.recv()
                users_to_send = [user for user in USERS_MAPPING if user != sender]
                print(users_to_send)
                msg_to_sender = "[server] Message sent to users"  # Special message to sender
                sending_tasks = [
                    asyncio.create_task(USERS_MAPPING[user].send(f"[{sender}] {new_msg}")) for user in users_to_send
                ]

                # Message delivered notification as separate task
                sending_tasks.append(asyncio.create_task(USERS_MAPPING[sender].send(msg_to_sender)))

                await asyncio.wait(sending_tasks)

        except websockets.ConnectionClosedOK:  # Handle user disconnect while messaging
            await remove_user(sender, USERS_MAPPING)
            print(sender, " disconnected")
    except websockets.ConnectionClosedError:
        print("User connection failed")


async def main():
    async with websockets.serve(user_connection_handler, "localhost", 2024, ping_interval=None):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    print("server started ...")
    print("awaiting")
    asyncio.run(main())

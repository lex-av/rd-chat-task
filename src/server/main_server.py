import asyncio

import websockets

USERS_MAPPING = {}  # Maps username to it's websocket
AWAITING_USERS = set()


async def add_user(user_websocket, user_name: str, users_mapping: dict) -> bool:
    """
    Adds new user to user mapper. Returns True if user was
    added and False otherwise. Prevents adding username, that
    already exists in mapper

    :param user_websocket: Connected user's websocket
    :param user_name: Username, given by user
    :param users_mapping: Server mapping from username to it's websocket
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
    Allows user to register on server by entering hit own username. Gets
    username from connected user. If username is already in use func informs
    user about it and offers user to try again
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


async def user_choose_mode(user_ws, username: str, awaiting_users: set):
    """
    User chooses between connection to another user or to
    stand by a connection from another user

    :param user_ws: Connected user's websocket
    :param username: Username in str, given by connected user
    :param awaiting_users: Server set of users in connection awaiting mode
     corresponding websockets
    :return: None
    """

    current_mode = await user_ws.recv()

    if bool(int(current_mode)):
        print("Not implemented yet")
    else:
        awaiting_users.add(username)
        print(awaiting_users)


async def user_connection_handler(websocket):
    """
    Main server handler for incoming connections and
    messages routing

    :param websocket: connected user websocket
    """

    current_username = await register_user(websocket, USERS_MAPPING)
    await user_choose_mode(websocket, current_username, AWAITING_USERS)
    await remove_user(current_username, USERS_MAPPING)


async def main():
    async with websockets.serve(user_connection_handler, "localhost", 2024):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    print("server started ...")
    print("awaiting")
    asyncio.run(main())

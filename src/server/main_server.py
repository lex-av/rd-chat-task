import asyncio

import websockets

USERS_MAPPING = {}  # Maps username to it's websocket


async def add_user(user_websocket, user_name: str) -> bool:
    """
    Adds new user to user mapper. Returns True if user was
    added and False otherwise. Prevents adding username, that
    already exists in mapper

    :param user_websocket: Connected user's websocket
    :param user_name: Username, given by user
    :return: bool
    """

    if user_name in USERS_MAPPING:
        return False
    else:
        USERS_MAPPING[user_name] = user_websocket
        return True


async def user_connection_handler(websocket):
    """
    Main server handler for incoming connections and
    messages routing

    :param websocket: connected user websocket
    """

    user_name = await websocket.recv()
    add_user_ok = await add_user(websocket, user_name)
    print("users: ", USERS_MAPPING)
    if add_user_ok:
        await websocket.send("Got your u_name")
    else:
        await websocket.send("Username already exists")


async def main():
    async with websockets.serve(user_connection_handler, "localhost", 2024):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    print("server started ...")
    print("awaiting")
    asyncio.run(main())

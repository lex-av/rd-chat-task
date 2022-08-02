import asyncio

import websockets


async def connect():
    """
    Main client's function to register on server and
    send messages to another clients
    """

    uri = "ws://localhost:2024"

    async with websockets.connect(uri) as websocket:
        u_name = input("What's your u_name? ")
        await websocket.send(u_name)
        u_name_answ = await websocket.recv()
        print(f">>> {u_name_answ}")


if __name__ == "__main__":
    print("Client started ...")
    asyncio.run(connect())

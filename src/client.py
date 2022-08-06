import threading

import websocket


def register(server_ws):
    """
    Tries to register on server by given username
    :param server_ws: Selected server's websocket
    :return: Accepted username
    """

    while True:
        user_name = input("Enter your username ")
        server_ws.send(user_name)
        user_name_answer = server_ws.recv()

        if bool(int(user_name_answer)):
            print("Username registered")
            return user_name
        else:
            print("Username is already in use")


def prt_answ(ws):
    while 1:
        answr = ws.recv()
        print(answr)


if __name__ == "__main__":
    ws = websocket.WebSocket()
    ws.connect("ws://localhost:2024")

    register(ws)
    msg_thread = threading.Thread(target=prt_answ, args=[ws])
    msg_thread.daemon = True
    msg_thread.start()

    try:
        while 1:
            msg = input()
            ws.send(msg)

    except KeyboardInterrupt:
        ws.close()

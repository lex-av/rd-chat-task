import threading

import websocket


def verify_username(username: str) -> int:
    """
    Checks username to be appropriate length and content.
    Returns int codes for calling func to interpret

    :param username: Username to verify
    :return: True or False
    """
    restricted_chars = {".", ",", "(", ")", "'", '"', "~", "`"}

    if len(username) < 3:
        return 1
    if len(username) > 20:
        return 2
    if not username[0].isalpha():
        return 3
    if any(char in username for char in restricted_chars):
        return 4
    return 0


def generate_verification_msg(code: int) -> str:
    """
    Generates human-readable message, based on verification
    function int code

    :param code: in number from verify_username()
    :return: human-readable message
    """

    if code == 1:
        return "Username too short"
    if code == 2:
        return "Username too long"
    if code == 3:
        return "Username has to start with letter"
    if code == 4:
        return "Username contains restricted characters"
    return "Username OK"


def register(server_ws) -> str:
    """
    Tries to register on server by given username
    :param server_ws: Selected server's websocket
    :return: Accepted username
    """

    while True:
        user_name = input("Enter your username ")
        verify_code = verify_username(user_name)
        if verify_code == 0:
            server_ws.send(user_name)
            user_name_answer = server_ws.recv()
        else:
            print(generate_verification_msg(verify_code))
            continue

        if bool(int(user_name_answer)):
            print("Username registered")
            return user_name
        else:
            print("Username is already in use")


def print_server_answers(ws) -> None:
    """
    Function to listen server answers to client
    messages and print them. This function has to run
    in dedicated thread to work simultaneously with
    user input
    :param ws: Server websocket
    :return: None
    """

    while 1:
        srv_answer = ws.recv()
        print(srv_answer)


if __name__ == "__main__":
    # Initialise server websocket
    ws = websocket.WebSocket()
    ws.connect("ws://localhost:2024")

    # Register user on server
    register(ws)

    # Launch thread to print server messages
    msg_thread = threading.Thread(target=print_server_answers, args=[ws])
    msg_thread.daemon = True  # For ctrl-c termination
    msg_thread.start()

    # Input and send message to server
    try:
        while 1:
            msg = input()
            ws.send(msg)

    except KeyboardInterrupt:
        ws.close()

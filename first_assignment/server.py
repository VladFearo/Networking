import socket

UDP_IP = '0.0.0.0'
UDP_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sock.bind((UDP_IP, UDP_PORT))

name_pool = dict()


def check_message_type(message):
    """
    Checks to find the type of the message, tyeps can be of either Name or Name and message

    Args:
        message (String): the message recieved from the user

    Returns:
        String: The type of the message
    """
    parts = message.split(' ', 1)
    if len(parts) == 1:
        return "Name"
    elif len(parts) == 2:
        return "Name and message"
    else:
        return "Invalid format"


def find_sender(address):
    """
    Checks the name pool to find a sender for a given address otherwise returns an empty string

    Args:
        address (String): The ip address and port of the user we're trying to find

    Returns:
        String: The name of the user found or an empty string if the user is not found.
    """
    for name, addr in name_pool.items():
        if addr == address:
            return name
    # if user not found return an empty string
    return ""


while True:
    try:
        data, addr = sock.recvfrom(1024)
        message = data.decode()
        msg_type = check_message_type(message)
        if msg_type == "Name":
            name = message
            if name not in name_pool:
                name_pool[name] = addr
                print("added", name, addr)
                sock.sendto("Name Added".encode(), addr)

        elif msg_type == "Name and message":
            name, message_content = message.split(' ', 1)

            if name not in name_pool:
                sock.sendto("Users need to sign up before sending messages".encode(), addr)
                continue

            sender = find_sender(name_pool[name])
            if sender == "":
                sock.sendto("Users need to sign up before sending messages".encode(), addr)
                continue

            print('received message:', name, addr)

            if name in name_pool:
                sock.sendto(f"{sender}: {message_content}".encode(), name_pool[name])
                sock.sendto("Message sent".encode(), addr)
                print("message sent")
        else:
            raise ValueError("Invalid message format. Expected format: 'Name Message'")
    except (ConnectionResetError, ValueError, KeyError) as e:
        print(f"Error: {e}")

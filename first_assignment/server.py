import socket

UDP_IP = '0.0.0.0'
UDP_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sock.bind((UDP_IP, UDP_PORT))

name_pool = dict()


def check_message(message):
    parts = message.split(' ', 1)
    if len(parts) == 1:
        return "Name"
    elif len(parts) == 2:
        return "Name and message"
    else:
        return "Invalid format"


def find_sender(address):
    for name, addr in name_pool.items():
        if addr == address:
            return name


while True:
    try:
        data, addr = sock.recvfrom(1024)
        message = data.decode()
        type = check_message(message)
        if type == "Name":
            name = message
            if name not in name_pool:
                name_pool[name] = addr
                print("added", name, addr)
                sock.sendto("Name Added".encode(), addr)

        elif type == "Name and message":

            # TODO: Check what to do if nameless user.
            name, message_content = message.split(' ', 1)
            print('received message:', name, addr)
            if name not in name_pool:
                sock.sendto("User doesn't exist".encode(), addr)

            elif name in name_pool:
                sender = find_sender(name_pool[name])
                sock.sendto(f"{sender}: {message_content}".encode(), name_pool[name])
                sock.sendto("Message sent".encode(), addr)
                print("message sent")
        else:
            raise ValueError("Invalid message format. Expected format: 'Name Message'")
    except (ConnectionResetError, ValueError) as e:
        print(f"Error: {e}")

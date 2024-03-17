import socket
import threading
 
HEADER = 64
PORT = 5050 # You can change the port number to any port number but client and server must have the same port number.
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def send_message(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg = input("Enter a command to execute on the client: ")

        if msg == "!DISCONNECT":
            send_message(conn, msg)
            print(f"Disconnecting {addr}")
            connected = False
        elif msg.startswith("!GET:"):
            send_message(conn, msg)
            filename = msg[5:]
            download_path = f"downloaded_{filename}"
            filesize = int(conn.recv(HEADER).decode(FORMAT))
            print(f"Receiving file: {filename} Size: {filesize} bytes")
            with open(download_path, 'wb') as f:
                for _ in range(filesize // 20000 + 1):
                    bytes_read = conn.recv(20000)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
                    print(f"Received {f.tell()} of {filesize} bytes ({100.0 * f.tell() / filesize:.2f}%)")
            print(f"File {filename} downloaded successfully to {download_path}.")
            continue
        elif msg.startswith("!CMD:"):
            send_message(conn, f"{msg}")
        else:
            print("Please enter a valid command")

        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                print(f"[{addr}] {msg}")

        except Exception as e:
            print(f"Error in handle_client: {e}")
            break
    connected = True
    conn.close()
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {ADDRESS[0]}:{PORT}")
    print("Enter !CMD: for running commands on the client's command prompt")
    print("Enter !GET: for downloading files from the client")
    print("Enter !DISCONNECT: for disconnecting from the client")
    print("#################################################################")


    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] Server is starting...")
start()

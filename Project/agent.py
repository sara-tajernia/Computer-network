import socket
import json
import psutil

IP = socket.gethostbyname(socket.gethostname())
PORT = 7777
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"


def agent():
    counter = 0
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADDR)
            print(f" [CONNECTED] Client connected to server at {IP}: {PORT}")
            connected = True
            while connected:
                msg = input(">")
                msg = jason_data(client, counter)
                counter += 1
                print(f"[SERVER] {msg}")
                client.send(msg.encode(FORMAT))

        except:
            print("connection failed do you want to try again?")
            x = input()
            if x == 'Yes':
                continue
            else:
                print(DISCONNECT_MSG)
                break

def jason_data(client, counter):
    data_metrics = {
        'RAM_usage': psutil.virtual_memory().percent,
        'CPU_usage': psutil.cpu_percent(),
        'RAM_total': psutil.virtual_memory().total,
        'number': counter
    }

    msg = json.dumps(data_metrics)
    return msg

if __name__ == '__main__':
    agent()




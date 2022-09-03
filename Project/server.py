import json
import socket
import threading
from prometheus_client import Gauge,start_http_server

IP = socket.gethostbyname(socket.gethostname())
PORT = 7777
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

RAM_usage = Gauge('RAM_usage', 'RAM usage', ['number'])
CPU_usage = Gauge('CPU_usage', 'CPU usage', ['number'])
RAM_total = Gauge('RAM_total', 'RAM total', ['number'])

def handle_client(conn, addr):
    print (f" [NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        try:
            msg = conn.recv(SIZE).decode(FORMAT)
            print(f"[{addr}] {msg}")
            metrics_client = json.loads(msg)
            RAM_usage.labels(number=metrics_client['number']).set(metrics_client['RAM_usage'])
            CPU_usage.labels(number=metrics_client['number']).set(metrics_client['CPU_usage'])
            RAM_total.labels(number=metrics_client['number']).set(metrics_client['RAM_total'])

        except:
            print("connection failed!")
            connected = False
    conn.close ()


def server():
    print ("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print (f"[LISTENING] Server is listening on {IP}:{PORT}")


    while True:
        conn, addr = server.accept ()
        thread = threading.Thread (target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() -1}")


if __name__ == '__main__':
    start_http_server(3000)
    server()


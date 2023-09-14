import socket
import json
import requests

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
HOST = (str)(s.getsockname()[0])
s.close()
PORT = 7777

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

server_socket.listen()

print(f"\nServer listening on {HOST}:{PORT}\n")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"\nClient connected from {client_address}")
    
    received_data = client_socket.recv(1024)

    s_s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s_s.connect(("172.17.0.4",8888))
    s_s.sendall(received_data)
    response = s_s.recv(1024).decode()
    response = response[1:-1]
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{response}/ids?start=0&count=20&api_key=RGAPI-8b5b1cf2-3e08-4326-8026-374adfc3a351"
    response = requests.get(url)
    if response.status_code == 200:
            data = response.json()
            url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{data[0]}?api_key=RGAPI-8b5b1cf2-3e08-4326-8026-374adfc3a351"
            response = requests.get(url)
            data = response.json()
            client_socket.sendall(json.dumps(data).encode())
    client_socket.close()
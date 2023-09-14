import requests
import pymongo
import socket
import json

client = pymongo.MongoClient("172.17.0.2:27017")
db = client["lol"]
users = db["users"]

users.delete_many({})

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
HOST = (str)(s.getsockname()[0])
s.close()
PORT = 8888

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST,PORT))
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"\nClient connected from {client_address}")
    received_data = client_socket.recv(1024)
    summoner_info = json.loads(received_data.decode())
    summoner_info = summoner_info.split('|')
    summoner_name = summoner_info[0].replace(" ","%20")
    region = summoner_info[1]
    res = users.find_one({"summoner_name": summoner_name})
    res_puuid = "Error"
    if res:
        res_puuid = res["summoner_puuid"]
    else:
        url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key=RGAPI-8b5b1cf2-3e08-4326-8026-374adfc3a351"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            user_data = {"summoner_name": summoner_name, "summoner_puuid": data["puuid"]}
            res_puuid = user_data["summoner_puuid"]
            users.insert_one(user_data)
            print(f"Data added:\n{user_data}\n")
        else:
            print("Request failed or API returned unsuccessful response.\n")
            res_puuid = "Error"
    req_json = json.dumps(res_puuid).encode()
    client_socket.sendall(req_json)
    client_socket.close()

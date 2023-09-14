import socket
import json

SERVER_HOST = 'localhost'
SERVER_PORT = 8080
print("\n=================================================")
print("===> League of Legends - Extended statistics <===")
print("=================================================")

regions = ["BR1","EUN1","EUW1","JP1","KR","LA1","LA2","NA1","OC1","PH2","RU","SG2","TH2","TR1","TW2","VN2"]
summoner_name = ""
region = ""

while True:
    summoner_name = input("\nEnter your summoner name: ")
    print(f"Your summoner name: {summoner_name}")
    ans = input("Is that correct ?(y/n): ")
    if ans.lower() == "y": break
    
while True:
    region = input("\nEnter region: ")
    region = region.lower()
    if region.upper() in regions: break
    else: print("Region does not exist")
    
summoner_info = f"{summoner_name}|{region}"
req_json = json.dumps(summoner_info).encode()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))
client_socket.sendall(req_json)

while True:
    response = client_socket.recv(1024).decode()
    if response == "": break
    print(response)




client_socket.close()

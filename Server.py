import socket
import threading
import json
import requests
import Menu.py

HOST = '127.0.0.1'
PORT = 8000
Client = []

# Connecting to at Least 3 Clients [Check]
MAX_CONNECTIONS = 5
API_KEY = 'd4be61055cd64fc09926fdf2f31370fe'
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'


# Function to make a Json text
def fetch_news(endpoint, params):
    url = f"{BASE_URL}{endpoint}"
    params['apiKey'] = API_KEY
    response = requests.get(url, params=params)
    return response.json()

# Function to handle client connection
def handle_client(conn, addr):
    # Display Name Sent by Client [Check]
    print(f"New connection from {addr}")
    conn.sendall(b"Welcome! Please enter your name:")  # because in bits
    client_name = conn.recv(1024).decode()  # Decode the name
    clients.append((conn, client_name))
    print(f"Client name: {client_name}")

    # Take the option
    Main_menu()

    # While loop will be here

    print(f"Connection with {client_name} closed.")
    conn.close()  # Close the connection
    clients.remove((conn, client_name))  # Remove client from the list


# Main server function
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_CONNECTIONS)

    # Server Display Client Name Upon Connecting [check]
    print(f"Server started, listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        # Multi Threading!
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()
        handle_client()


# To Start the Server
if _name_ == "_main_":
    main()

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
BASE_URL = 'https://newsapi.org/v2/'  # Changed from NEWS_API_URL to BASE_URL

# Function to fetch news from NewsAPI
def fetch_news(endpoint, params):
    url = f"{BASE_URL}{endpoint}"
    params['apiKey'] = API_KEY
    response = requests.get(url, params=params)
    response.json()


# Function to handle client connection
def handle_client(conn, addr):
    # Display Name Sent by Client
    print(f"New connection from {addr}")
    client_name = conn.recv(1024).decode()  # Decode the name
    clients.append((conn, client_name))
    print(f"Client name: {client_name}")

    try:
        while True:
            try:
                request = conn.recv(1024).decode()  # Changed from client_socket to conn
                if not request:
                    break

                option, params = json.loads(request)
                if option == 'headlines':
                    data = fetch_news('top-headlines', params)
                elif option == 'sources':
                    data = fetch_news('sources', params)
                else:
                    data = {'error': 'Invalid option'}
                
                # Save Json in a file
                filename = f"B8_{client_name}_{option}.json"
                with open(filename, 'w') as f:
                    json.dump(data, f)

                response = json.dumps(data)
                conn.send(response.encode())  # Changed from client_socket to conn
            except Exception as e:
                print(f"Error handling request from {addr}: {e}")
                break
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        print(f"Connection closed with {addr}")
        conn.close()

    print(f"Connection with {client_name} closed.")
    clients.remove((conn, client_name))  # Remove client from the list

# Main server function
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_CONNECTIONS)

    # Server Display Client Name Upon Connecting
    print(f"Server started, listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        # Multi Threading!
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

# To Start the Server
if __name__ == "__main__": 
    main()

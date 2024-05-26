import socket
import threading
import requests
import json
import Nmenu

# Configuration
HOST = '127.0.0.1'
PORT = 8001
clients = []
MAX_CONNECTIONS = 5
API_KEY = 'd4be61055cd64fc09926fdf2f31370fe'
BASE_URL = 'https://newsapi.org/v2/top-headlines'

# Function to fetch news from NewsAPI
def fetch_news(endpoint, params):
    url = f"{BASE_URL}{endpoint}"
    params['apiKey'] = API_KEY
    response = requests.get(url, params=params)

    if response.status_code == 200:
        try:
            data = response.json()
            return data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print(f"Failed to fetch news. Status code: {response.status_code}")
        return None


# Function to handle client connection
def handle_client(conn, addr):
    # Display Name Sent by Client
    print(f"New connection from {addr}")
    client_name = conn.recv(1024).decode()
    clients.append((conn, client_name))
    print(f"Client name: {client_name}")

    try:
        while True:
            try:
                request = conn.recv(1024).decode('ascii')
                if not request:
                    break

                option, params = json.loads(request)
                if option == 'headlines':
                    data = fetch_news('top-headlines', params)
                elif option == 'sources':
                    data = fetch_news('sources', params)
                else:
                    data = {'error': 'Invalid option'}

                response = json.dumps(data if data else {'error': 'No data found'})
                conn.send(response.encode('ascii'))
            except Exception as e:
                print(f"Error handling request from {addr}: {e}")
                break
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        print(f"Connection closed with {addr}")
        conn.close()
        clients.remove((conn, client_name))
        print(f"Connection with {client_name} closed.")

# Main server function
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(MAX_CONNECTIONS)

    print(f"Server started, listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

# To Start the Server
if __name__ == "__main__":
    main()

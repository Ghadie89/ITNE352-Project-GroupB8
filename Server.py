import socket
import threading
import json
import logging
import Nmenu
import os
# Configuration
HOST = '127.0.0.1'
PORT = 8001
MAX_CONNECTIONS = 5

# Setup logging
logging.basicConfig(level=logging.INFO)

clients = []
users_db = "users.json"
def load_users():
    if os.path.exists(users_db):
        with open(users_db, 'r') as file:
            return json.load(file)
    return {}
def save_users(users):
    with open(users_db, 'w') as file:
        json.dump(users, file, indent=4)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    users[username] = password
    save_users(users)
    return True, "Registration successful."

def authenticate_user(username, password):
    users = load_users()
    if username in users and users[username] == password:
        return True, "Login successful."
    return False, "Invalid username or password."

# Function to handle client connection
def handle_client(conn, addr):
    logging.info(f"New connection from {addr}")
    try:
        while True:
            auth_choice = conn.recv(1024).decode()
            username = conn.recv(1024).decode()
            password = conn.recv(1024).decode()

            if auth_choice == 'R':
                success, message = register_user(username, password)
            elif auth_choice == 'L':
                success, message = authenticate_user(username, password)
            else:
                success, message = False, "Invalid authentication choice."

            conn.send(message.encode())

            if success:
                break

        client_name = conn.recv(1024).decode()
        logging.info(f"Client name: {client_name}")
        while True:
            request = conn.recv(1024).decode()
            if not request:
                break
            option, params = json.loads(request)
            if option == 'headlines':
                Nmenu.headline('top-headlines', params, conn,option,client_name)
            elif option == 'sources':
                Nmenu.sources('sources', params, conn,option,client_name)
            else:
                response = json.dumps({'error': 'Invalid option'})
                conn.send(response.encode())
    except Exception as e:
        logging.error(f"Error handling request from {addr}: {e}")
        response = json.dumps({'error': str(e)})
        conn.send(response.encode())
    finally:
        logging.info(f"Connection closed with {addr}")
        conn.close()


# Main server function
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(MAX_CONNECTIONS)

    logging.info(f"Server started, listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

# To Start the Server
if __name__ == "__main__":
    main()

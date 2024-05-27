import socket
import threading
import json
import logging
import Nmenu

# Configuration
HOST = '127.0.0.1'
PORT = 8001
MAX_CONNECTIONS = 5

# Setup logging
logging.basicConfig(level=logging.INFO)

clients = []

# Function to handle client connection
def handle_client(conn, addr):
    logging.info(f"New connection from {addr}")
    try:
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
                Nmenu.source('sources', params, conn)
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

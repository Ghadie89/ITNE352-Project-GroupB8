import socket
import threading
import json
import requests

HOST = '127.0.0.1'
PORT = 65432

# Connecting to at Least 3 Clients [Check]
MAX_CONNECTIONS = 5
API_KEY = 'd4be61055cd64fc09926fdf2f31370fe'
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'


# A function to Fetch the news
def fetch_news(option):
    url = f'https://newsapi.org/v2/top-headlines?country={option}&apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to handle client connection
def handle_client(client_socket, client_address):

    # Display Name Sent by Client [Check]
    print(f"New connection from {addr}")
    conn.sendall(b"Welcome! Please enter your name:") # because in bits
    client_name = conn.recv(1024).decode() # Decode the name
    clients.append((conn, client_name))
    print(f"Client name: {client_name}")
    while True:
        try:
            conn.sendall(b"Enter a country code (e.g., 'us' for United States):")
            country_code = conn.recv(1024).decode()  # Receive country code from client
            news_data = fetch_news(country_code)  # Fetch news data for the given country code

            if news_data:
                # Save the news data to a JSON file for evaluation purposes [Check]
                json_filename = f"{addr[1]}_{client_name}_{country_code}.json"
                with open(json_filename, 'w') as json_file:
                    json.dump(news_data, json_file)

                # Prepare a summary of the news articles
                articles = news_data.get('articles', [])
                summary = [f"{i + 1}. {article['title']}" for i, article in enumerate(articles)]
                summary_str = "\n".join(summary)
                conn.sendall(summary_str.encode())  # Send summary to client (List) [Check?]

                conn.sendall(b"\nEnter the number of the article you want details for:")
                article_num = int(conn.recv(1024).decode())  # Receive the article number (Answer from Client) [Check]

                if 0 < article_num <= len(articles):
                    selected_article = articles[article_num - 1]
                    details = json.dumps(selected_article, indent=2)  # Prepare detailed info and Jason format
                    conn.sendall(details.encode())  # Send detailed info to client
                else:
                    conn.sendall(b"Invalid article number.")
            else:
                conn.sendall(b"Failed to fetch news.")

        except Exception as e:
            print(f"Error: {e}")
            break

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

# To Start the Server
if __name__ == "__main__":
    main()


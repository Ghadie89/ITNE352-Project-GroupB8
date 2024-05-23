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

def Back_to_the_mainMenu(conn):
    Main_menu(conn)
def Main_menu(conn):
    Main_Menu = ("1. Search Headlines \n"
                 "2. List of Sources \n"
                 "3. Quit")
    conn.sendall(Main_Menu.encode(), 'ascii')
    option = server_socket.recv(1024).decode('ascii')
    if option == '1':
        Search_by_headlines()
    elif option == '2':
        list_of_sources_menue()
    elif option == '3':
        conn.sendall("Goodbye!".encode(), 'ascii')
        conn.close()  # Close the connection with the client
        server_socket.close()  # Close the server socket
        exit()
# Function to fetch headlines from NewsAPI based on a country code
def Search_by_headlines(conn):
    headline_menu = ("1.1 Search for Keywords \n"
                     "1.2 Search by category \n"
                     "1.3 Search by Country \n"
                     "1.4 List all New Headlines \n"
                     "1.5 Back to the Main Menu")

    conn.sendall(headline_menu.encode(), 'ascii')
    H_option = server_socket.recv(1024).decode('ascii')

    if H_option == '1.1':
        conn.sendall("Enter a keyword: ".encode('ascii'))
        keyword = conn.recv(1024).decode('ascii')
        Menu.HM_Search_for_Keywords(conn, keyword)

    elif H_option == '1.2':
        conn.sendall("Enter a Category: ".encode('ascii'))
        Category = conn.recv(1024).decode('ascii')
        Menu.HM_Search_by_Category(Category)

    elif H_option == '1.3':
        conn.sendall("Enter a keyword: ".encode('ascii'))
        Country = conn.recv(1024).decode('ascii')
        Menu.H_HM_Search_by_Country(Country)
    elif H_option == '1.4':
        Menu.HM_List_all_New_Headlines()
    elif H_option == '1.5':
        Back_to_the_mainMenu()
def list_of_sources_menue(conn):
    Sources_menue = ("2.1 Search for Category \n"
                     "2.2 Search by county \n"
                     "2.3 Search by language \n"
                     "2.4 List all \n"
                     "2.5 Back to the Main Menu")
    conn.sendall(Sources_menue.encode(), 'ascii')
    S_option = server_socket.recv(1024).decode('ascii')

    if S_option == '2.1':
        Menu.SM_Search_by_Category()
    elif S_option == '2.2':
        Menu.SM_Search_by_Country()
    elif S_option == '2.3':
        Menu.SM_Search_by_Language()
    elif S_option == '2.4':
        Menu.SM_List_all()
    elif S_option == '2.5':
        Back_to_the_mainMenu()
# Function to make a Json text
def save_article_to_json(news_data, client_name, option):
    # Save the news data to a JSON file for evaluation purposes [Check]
    json_filename = f"B8_{client_name}_{option}.json"
    with open(json_filename, 'w') as json_file:
        json.dump(news_data, json_file)

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

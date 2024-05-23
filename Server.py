import socket
import threading
import json
import requests
import Menu

HOST = '127.0.0.1'
PORT = 65432
Client=[]

# Connecting to at Least 3 Clients [Check]
MAX_CONNECTIONS = 5
API_KEY = 'd4be61055cd64fc09926fdf2f31370fe'
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'

def Main_menu ():
    Main_Menu = ("1. Search Headlines \n"
                 "2. List of Sources \n"
                 "3. Quit")
    conn.sendall(Main_Menu.encode(), 'ascii')
    option = server_socket.recv(1024).decode('ascii')
    if option == '1' :
        Search_by_headlines()
    elif option == '2' :
        list_of_sources_menue()
    elif option  == '3' :
        conn.sendall("Goodbye!".encode(), 'ascii')
        conn.close()  # Close the connection with the client
        server_socket.close()  # Close the server socket
        exit()

# Function to fetch headlines from NewsAPI based on a country code
def Search_by_headlines ():
    headline_menu = ("1. Search for Keywords \n"
                     "2. Search by category \n"
                     "3. Search by Country \n"
                     "4. List all New Headlines \n"
                     "5. Back to the Main Menu")
    
    conn.sendall(headline_menu.encode(), 'ascii')
    H_option = server_socket.recv(1024).decode('ascii')

    if option == '1' :
        HM_Search_for_Keywords()
    elif option == '2' :
        HM_Search_by_Category()
    elif option  == '3' :
        HM_Search_by_Country()
    elif option == '4' :
        HM_List_all_New_Headlines()
    elif option == '5' :
        HM_Back_to_the_mainMenu()



def list_of_sources_menue ():

    Sources_menue = ("1. Search for Category \n"
                     "2. Search by county \n"
                     "3. Search by language \n"
                     "4. List all \n"
                     "5. Back to the Main Menu")
    conn.sendall(Sources_menue.encode(), 'ascii')
    S_option = server_socket.recv(1024).decode('ascii')

    if option == '1' :
        SM_Search_by_Category()
    elif option == '2' :
        SM_Search_by_Country()
    elif option  == '3' :
        SM_Search_by_Language()
    elif option == '4' :
        SM_List_all()
    elif option == '5' :
        SM_Back_to_the_mainMenu()


# Function to make a Json text
def Json ():
    # Save the news data to a JSON file for evaluation purposes [Check]
    json_filename = f"B8_{client_name}_{country_code}.json"
    with open(json_filename, 'w') as json_file:
        json.dump(news_data, json_file)

# a function to Fetch the news
def fetch_news(option):
    url = f'https://newsapi.org/v2/top-headlines?country={option}&apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
# Function to handle client connection
def handle_client(conn, addr):
    # Display Name Sent by Client [Check]
    print(f"New connection from {addr}")
    conn.sendall(b"Welcome! Please enter your name:") # because in bits
    client_name = conn.recv(1024).decode() # Decode the name
    clients.append((conn, client_name))
    print(f"Client name: {client_name}")

    # Take the option
    Main_menu()


    # While

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
if _name_ == "_main_":
    main()

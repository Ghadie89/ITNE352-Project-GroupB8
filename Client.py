import socket
import json

# Configuration
HOST = '127.0.0.1'  # Server's IP address
PORT = 8001


# Function to display menus and handle user input
def display_menu():
    print("Main Menu:")
    print("1. Search headlines")
    print("2. List of Sources")
    print("3. Quit")
    choice = input("Enter choice: ")
    return choice

def handle_headlines(client_socket):
    print("Headlines Menu:")
    print("1. Search for keywords")
    print("2. Search by category")
    print("3. Search by country")
    print("4. List all new headlines")
    print("5. Back to the main menu")
    choice = input("Enter choice: ")

    params = {}
    if choice == '1':
        params['q'] = input("Enter keyword: ")
    elif choice == '2':
        print("Categories: \n"
              "1. Business \n"
              "2. Entertainment \n"
              "3. General \n"
              "4. Health \n"
              "5. Science \n"
              "6. Sports \n"
              "7. Technology \n")
        params['category'] = input("Enter category: ")
    elif choice == '3':
        params['country'] = input("Enter country: ")
    elif choice == '4':
        pass
    elif choice == '5':
        return

    request = json.dumps(('headlines', params))
    client_socket.send(request.encode())
    response = client_socket.recv(4096).decode()
    data = json.loads(response)
    print(json.dumps(data, indent=4))

    response = client_socket.recv(4096).decode()  # Receive response
    print("Received response:", response)
    data = json.loads(response)  # Decode JSON


def handle_sources(client_socket):
    print("Sources Menu:")
    print("1. Search by category")
    print("2. Search by country")
    print("3. Search by language")
    print("4. List all")
    print("5. Back to the main menu")
    choice = input("Enter choice: ")

    params = {}
    if choice == '1':
        print("Categories: \n"
             "1. Business \n"
             "2. Entertainment \n"
             "3. General \n"
             "4. Health \n"
             "5. Science \n"
             "6. Sports \n"
             "7. Technology \n")

        params['category'] = input("Enter category: ")
    elif choice == '2':
        params['country'] = input("Enter country: ")
    elif choice == '3':
        params['language'] = input("Enter language: ")
    elif choice == '4':
        pass
    elif choice == '5':
        return

    request = json.dumps(('sources', params))
    client_socket.send(request.encode())
    response = client_socket.recv(4096).decode()  # Increase buffer size if needed
    data = json.loads(response)
    print(json.dumps(data, indent=4))


# Main client function
def start_client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))

        client_name = input("Enter your name: ")
        client_socket.send(client_name.encode())

        while True:
            choice = display_menu()
            if choice == '1':
                handle_headlines(client_socket)
            elif choice == '2':
                handle_sources(client_socket)
            elif choice == '3':
                print("Quitting...")
                break
            else:
                print("Invalid choice. Please try again.")

        client_socket.close()
    except ConnectionRefusedError:
        print("Failed to connect to the server. Ensure the server is running and reachable.")
    except ConnectionResetError:
        print("Connection lost. The server may have closed the connection.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    start_client()

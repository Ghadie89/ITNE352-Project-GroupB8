import socket
import json
import Nserver

HOST = '127.0.0.1'
PORT = 8001

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
        print("Categories:\n1. Business\n2. Entertainment\n3. General\n4. Health\n5. Science\n6. Sports\n7. Technology")
        category_choice = input("Enter category number: ")
        categories = {
            '1': 'business',
            '2': 'entertainment',
            '3': 'general',
            '4': 'health',
            '5': 'science',
            '6': 'sports',
            '7': 'technology'
        }
        params['category'] = categories.get(category_choice)
    elif choice == '3':
        print("Countries: \n 1. au \n 2. nz \n 3. ca \n 4. ae \n 5. sa \n 6. gb \n 7. us \n 8. eg \n 9. ma \n")
        country_choice = input("Enter country number: ")
        countries = {
            '1': 'au',
            '2': 'nz',
            '3': 'ca',
            '4': 'ae',
            '5': 'sa',
            '6': 'gb',
            '7': 'us',
            '8': 'eg',
            '9': 'ma'
        }
        params['country'] = countries.get(country_choice)
    elif choice == '4':
        pass
    elif choice == '5':
        return

    request = json.dumps(('headlines', params))
    client_socket.send(request.encode('ascii'))
    response = client_socket.recv(4096).decode('ascii')

    print("Received response:", response)

    try:
        data = json.loads(response)
        if isinstance(data, list):
            for article in data:
                print(json.dumps(article, indent=4))
        else:
            print(data)
    except json.JSONDecodeError as e:
        print(f"An error occurred: {e}")

    article_choice = input("Input article number: ")
    client_socket.send(article_choice.encode('ascii'))
    print(client_socket.recv(4096).decode('ascii'))

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
        print("Categories:\n1. Business\n2. Entertainment\n3. General\n4. Health\n5. Science\n6. Sports\n7. Technology")
        category_choice = input("Enter category number: ")
        categories = {
            '1': 'business',
            '2': 'entertainment',
            '3': 'general',
            '4': 'health',
            '5': 'science',
            '6': 'sports',
            '7': 'technology'
        }
        params['category'] = categories.get(category_choice, 'general')
    elif choice == '2':
        params['country'] = input("Enter country: ")
    elif choice == '3':
        params['language'] = input("Enter language: ")
    elif choice == '4':
        pass
    elif choice == '5':
        return

    request = json.dumps(('sources', params))
    client_socket.send(request.encode('ascii'))
    response = client_socket.recv(4096).decode('ascii')

    print("Received response:", response)  # Debugging line

    try:
        data = json.loads(response)
        if isinstance(data, list):
            for source in data:
                print(json.dumps(source, indent=4))
        else:
            print(data)
    except json.JSONDecodeError as e:
        print(f"An error occurred: {e}")

    article_choice = input("Input article number: ")
    client_socket.send(article_choice.encode('ascii'))
    print(client_socket.recv(4096).decode('ascii'))

# Main client function
def start_client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))

        client_name = input("Enter your name: ")
        client_socket.send(client_name.encode('ascii'))

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


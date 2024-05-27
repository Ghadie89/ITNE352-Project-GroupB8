import socket
import json

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
    while True:
        print("Headlines Menu:\n1. Search for keywords\n2. Search by category\n3. Search by country\n4. List all new headlines\n5. Back to the main menu")
        choice = input("Enter choice: ")
        params = {}
        if choice == '1':
            params['q'] = input("Enter keyword: ")
        elif choice == '2':
            print('1-Business\n2-Entertainment\n3-General\n4-Health\n5-Science\n6-Sports\n7-Technology')
            categories = {'1': 'business', '2': 'entertainment', '3': 'general', '4': 'health', '5': 'science',
                          '6': 'sports', '7': 'technology'}
            params['category'] = categories.get(input("Enter category number: "))
        elif choice == '3':
            print('1-au\n2-nz\n3-ca\n4-ae\n5-sa\n6-gb\n7-us\n8-eg\n9-ma')
            countries = {'1': 'au', '2': 'nz', '3': 'ca', '4': 'ae', '5': 'sa', '6': 'gb', '7': 'us', '8': 'eg', '9': 'ma'}
            params['country'] = countries.get(input("Enter country number: "))
        elif choice == '4':
            pass
        elif choice == '5':
            return

        request = json.dumps(('headlines', params))
        client_socket.send(request.encode())

        while True:
            response = client_socket.recv(4096).decode()
            print(response)
            if "Input article number" in response:
                article_choice = input("A valid article number: ")
                client_socket.send(article_choice.encode())
                article_content = client_socket.recv(4096).decode()
                if "Invalid choice. Please enter a number between 1 and 15." in article_content:
                    print(article_content)
                else:
                    print(article_content)
                    break


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
    client_socket.send(request.encode())
    response = client_socket.recv(4096).decode()

    print("Received response:", response)

    try:
        data = json.loads(response)
        if isinstance(data, list):
            for source in data:
                print(json.dumps(source, indent=4))
        else:
            print(data)
    except json.JSONDecodeError as e:
        print(f"An error occurred: {e}")

    article_choice = input()
    client_socket.send(article_choice.encode())
    print(client_socket.recv(4096).decode())


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

# ITNE352 Project
## Project Discription:
Semester : Second Semester of 2023/2024
### Group
Group name: B8
Course Code: ITNE352
Section: 02
**Student names:** 
1. Ghadeer Mohammed 202204965
2. Fatema Ali 202208354

### Table of Content
1. Server Side Python
2. Client Side Code

### Requirment
Project was done using pure python, so to run this project. we are gonna need to install the latest version of python from **The Original Website** *https://www.python.org/downloads/* . or from **pip** , in powershell or command prompt, you can : *python get-pip.py*. Second, you will need to set up the Environment in your Device, one way to do it is by using command prompt: choose a file in your machine then track it using **cd** then create the virtual Environment *python3 -m venv venv* . then after activating it. install all the requirment listed below.

In this project, we are going to use HTTP to send a GET request to newsAPI.org. to have the ability to do that we are gonna be needing to install **Requests**, which is a simple, yet elegant, HTTP library and to istall it using pip **:** *pip install requests*
Required Dependancies: install requests
install authentication

### How To:

**Steps in Configuration:**

**Configure Environment:** Verify that Python is installed on your computer. It is available for download from Python.org.
Use venv or virtualenv to optionally build up a virtual environment to isolate dependencies.
Establishing the Project: Take a clone of the project repository using a version control system (like Git).
Go to the project directory by navigating. Utilizing pip, install the project dependencies.

**Launch the server:**
Launch the project's main Python file. For instance, execute the server.py and make sure that you have the python script called "Menu"; which is an extension of the erver script.

Keep an eye on the output: Look for any error messages or signs that the server has started up successfully in the terminal or console output. *Log messages* usually indicate whether or not the server is listening on a specific port. if so, rerun the server.py then the client.py. You should notice log messages showing that the server is up and operating and waiting for incoming connections if it begins correctly.

### The Script

**The Client-Server Script :** This project includes three Python scripts with the menu as an extension of the server script. a straightforward client-server program that makes use of the News API to enable clients to obtain news headlines and source information. The primary features and elements of each script are broken down as follows:

**1. Functions of the server script (server.py)** include handling incoming client connections, handling client requests, and interacting with the news API to retrieve news content.

*a. Used Packages:*
socket: To establish connections with a socket.threading: To manage several client connections at once. json: For JSON data encoding and decoding. logging: To record server actions. Functions for retrieving headlines and sources from the News API are included in Nmenu (presumed to be a distinct module; not supplied here). 

*b. Main Function:*
handle_client(conn, addr): Responds to requests from clients, accepts them, processes them, and handles individual client connections. The main() method launches the server, waits for connections, and creates threads to process requests from clients.

_Server code Snippet_
def handle_client(conn, addr):
    _Handles individual client connections_

def main():
    _Main server function_

if __name__ == "__main__":
    main()


**2. Client Script**
*a. Functionality:* Enables users to interactively explore news headlines and sources from the server using the client script (client.py).
_b. Used Packages_:
socket: For establishing connections with the server using sockets. json: For JSON data encoding and decoding.
_c. Main Functions:_
display_menu(): Provides the user with a list of the primary menu selections. Handles user interaction for searching headlines by nation, category, or keyword using handle_headlines(client_socket). handle_sources(client_socket): Manages user interaction for category, nation, or language-based news source searches.
The primary function start_client() initiates the client, establishes a connection with the server, and communicates with it through user input.

_Client snippet_
def handle_headlines(client_socket):
    _Handles user interaction for searching headlines_

def handle_sources(client_socket):
    _Handles user interaction for searching news sources_

def start_client():
    _Main client function_

if __name__ == "__main__":
    start_client()

### Additional Concept
## Authentication:
Making ensuring that only users who have registered may access the server's services is the aim of the authentication system. Users have the option of creating a new account or logging in using an already-existing one. This gives the communication an extra degree of protection and customization.

By entering their username and password, new users may register and establish an account.
User Login: enables current users to access their account by entering their password and username.
User Data Storage: On the server, a JSON file containing user credentials is kept.
Modifications Made

Currently, the server is waiting on an authentication request ('R' for register or 'L' for login) before allowing more requests to be made.
The user can access the menu choices for obtaining sources or headlines once they have successfully authenticated with the server.
User Prompted for Authentication on the Client Side:

The user is prompted by the client to select whether to create a new account or utilize an already-existing one.
It gathers the password and username, then transmits these information to the server.
Handling Server Responses:

The server sends the authentication result to the client, which displays it. Should authentication fail, the user is prompted to attempt again.



### Acknowledgement

I would like to express my heartfelt gratitude to out tutor for their invaluable guidance and support during this project. Their expertise and encouragement have been pivotal in its success. 

Thank you for your dedication and inspiration.

Sincerely,  
### Conclusion

To sum up, working on this project has been a rewarding experience that has helped me grasp a variety of programming, networking, and application development ideas at a deeper level. I have learned useful lessons about developing scalable and effective systems by integrating client-server communication and external APIs.

The project's goals, which included implementing news headline retrieval, identifying news sources, and user authentication, were all accomplished with success. Authentication is added to the services to improve security and guarantee that only authorized users may access them.

I ran against obstacles during the development process that called for critical thinking and problem-solving abilities. But these obstacles were surmounted with persistence and help from peers and mentors, resulting in a strong and useful application.

There is room for improvement in the future, including adding more functions, enhancing the user experience, and maximizing performance. This initiative has given rise to a strong base on which further advancements may be made.

All things considered, I am happy with the results and appreciative of the educational possibilities this project has provided. It has been a fulfilling experience, and I'm eager to use the information and abilities I've acquired in my future software development ventures.



### Resources
Python Requests : *{https://pypi.org/project/requests/}*
Documentation NewsAPI : *{https://newsapi.org/docs}*

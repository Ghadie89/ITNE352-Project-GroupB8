import requests
import json

API_KEY = 'd4be61055cd64fc09926fdf2f31370fe'

def fetch_news(option):
    url = f'https://newsapi.org/v2/top-headlines?country={option}&apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def HM_Search_for_Keywords(keyword, client_socket):
    news_data = fetch_news(keyword)
    if news_data and 'articles' in news_data:
        articles = news_data['articles']
        for i, article in enumerate(articles, start=1):
            source_name = article['source']['name']
            author = article['author']
            title = article['title']
            article_info = f"{i}. Source: {source_name}, Author: {author}, Title: {title}\n"
            client_socket.sendall(article_info.encode())  # Send article information to client

        choice = int(client_socket.recv(1024).decode())  # Receive the client's choice

        if 1 <= choice <= len(articles):
            chosen_article = articles[choice - 1]
            # Assuming 'save_article_to_json' function is defined in 'Server.py'
            save_article_to_json(chosen_article) # Save the article in a Json

            # Display chosen article content to the client
            chosen_article_content = f"\nChosen article content:\n"
            chosen_article_content += f"Source: {chosen_article['source']['name']}\n"
            chosen_article_content += f"Author: {chosen_article['author']}\n"
            chosen_article_content += f"Title: {chosen_article['title']}\n"
            chosen_article_content += f"URL: {chosen_article['url']}\n"
            chosen_article_content += f"Description: {chosen_article['description']}\n"
            chosen_article_content += f"Publish Date: {chosen_article['publishedAt'][:10]}\n"  # Extracting date part
            chosen_article_content += f"Publish Time: {chosen_article['publishedAt'][11:19]}\n"  # Extracting time part

            # Send chosen article content to the client
            client_socket.sendall(chosen_article_content.encode('ascii'))

        else:
            print("Invalid choice.")
    else:
        print("No articles found.")

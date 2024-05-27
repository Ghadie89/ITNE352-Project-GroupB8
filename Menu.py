import requests
import json
import logging
import os

API_KEY = 'd4be61055cd64fc09926fdf2f31370fe'
BASE_URL = 'https://newsapi.org/v2/'

logging.basicConfig(level=logging.INFO)

def fetch_news(endpoint, params):
    url = f"{BASE_URL}{endpoint}"
    params['apiKey'] = API_KEY

    for attempt in range(3):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Attempt {attempt + 1}: Error fetching news: {e}")
            if attempt < 2:
                logging.info("Retrying...")
    return None


def headline(endpoint, param, client_socket):
    news_data = fetch_news(endpoint, param)
    if news_data and 'articles' in news_data:
        articles = news_data['articles'][:15]  # Limiting to 15 articles
        extracted_data = []

        # Add a search information entry before the articles
        search_info = ""
        if 'q' in param:
            search_info = f"Search by keyword: {param['q']}"
        elif 'category' in param:
            search_info = f"Search by category: {param['category']}"
        elif 'country' in param:
            search_info = f"Search by country: {param['country']}"
        extracted_data.append({'search_info': search_info})

        for i, article in enumerate(articles, start=1):
            source_name = article['source']['name']
            author = article.get('author', 'Unknown')
            title = article['title']
            article_info = f"{i}. \n Source: {source_name} \n Author: {author} \n Title: {title} \n"
            extracted_data.append({'source': source_name, 'author': author, 'title': title})
            client_socket.sendall(article_info.encode())

        while True:
            client_socket.sendall(b"\nInput article number: ")
            choice = client_socket.recv(1024).decode()
            if not choice.isdigit():
                client_socket.sendall(b"Invalid choice. Please enter a valid number.")
                continue

            choice = int(choice)
            if 1 <= choice <= len(articles):
                chosen_article = articles[choice - 1]
                chosen_article_content = (
                    f"\nChosen article content:\n"
                    f"Source: {chosen_article['source']['name']}\n"
                    f"Author: {chosen_article.get('author', 'Unknown')}\n"
                    f"Title: {chosen_article['title']}\n"
                    f"URL: {chosen_article['url']}\n"
                    f"Description: {chosen_article['description']}\n"
                    f"Publish Date: {chosen_article['publishedAt'][:10]}\n"
                    f"Publish Time: {chosen_article['publishedAt'][11:19]}\n"
                )
                client_socket.sendall(chosen_article_content.encode())
                break
            else:
                client_socket.sendall(b"Invalid choice. Please enter a number between 1 and 15.")
    else:
        client_socket.sendall(b"No articles found.")


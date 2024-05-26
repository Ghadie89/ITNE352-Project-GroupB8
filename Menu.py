import requests
import json
import logging

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


def headline(endpoint, param, client_socket, client_name, option):
    news_data = fetch_news(endpoint, param)
    if news_data and 'articles' in news_data:
        articles = news_data['articles'][:15]
        extracted_data = []

        for i, article in enumerate(articles, start=1):
            source_name = article['source']['name']
            author = article['author']
            title = article['title']
            article_info = f"{i}. \n Source: {source_name} \n Author: {author} \n Title: {title} \n"
            client_socket.sendall(article_info.encode('ascii'))

            extracted_info = {
                'source': source_name,
                'author': author,
                'title': title
            }
            extracted_data.append(extracted_info)
        json_filename = f"B8_{client_name}_{option}.json"
        with open(json_filename, 'w') as json_file:
            json.dump(extracted_data, json_file, indent=4, separators=(',', ': '))
        client_socket.sendall(b"Input article number: ")
        choice = int(client_socket.recv(1024).decode('ascii'))

        if 1 <= choice <= len(articles):
            chosen_article = articles[choice - 1]
            chosen_article_content = (
                f"\nChosen article content:\n"
                f"Source: {chosen_article['source']['name']}\n"
                f"Author: {chosen_article['author']}\n"
                f"Title: {chosen_article['title']}\n"
                f"URL: {chosen_article['url']}\n"
                f"Description: {chosen_article['description']}\n"
                f"Publish Date: {chosen_article['publishedAt'][:10]}\n"
                f"Publish Time: {chosen_article['publishedAt'][11:19]}\n"
            )
            client_socket.sendall(chosen_article_content.encode('ascii'))
        else:
            client_socket.sendall(b"Invalid choice.")
    else:
        client_socket.sendall(b"No articles found.")

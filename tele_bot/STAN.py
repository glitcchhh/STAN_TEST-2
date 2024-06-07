from Gpt_logic import GP_Generate
import requests
from bs4 import BeautifulSoup
import re

GPT_API_KEY = "API KEY"

gpt = GP_Generate(api_key=GPT_API_KEY)

class STAN:
    def __init__(self, query) -> None:
        self.query = query
    
    def scrape_website(self, url):
        try:
            # Send an HTTP request to the specified URL
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content of the webpage using BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find all text content within the HTML body
                text_content = soup.get_text()

                # Clean up the extracted text (remove extra spaces and newlines)
                cleaned_text = re.sub(r'\s+', ' ', text_content)

                # Save the cleaned text to a text file
                with open('website_content.txt', 'w', encoding='utf-8') as file, open('content.txt', 'w') as content:
                    file.write(cleaned_text)
                    content.write(cleaned_text)

                print(f'Successfully scraped the website and saved content to website_content.txt')
            else:
                print(f'Failed to retrieve content from {url}. Status code: {response.status_code}')
        except Exception as e:
            print(f'An error occurred: {str(e)}')

    def do_magic(self, url):
        self.scrape_website(url)
        text_file_path = "website_content.txt" # Replace with the path to your text file
        final_article = gpt.ask(text_file_path)
        with open("website_content.txt", "w", encoding="utf-8") as file:
            file.write(final_article)

        return text_file_path

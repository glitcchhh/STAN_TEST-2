import requests
from bs4 import BeautifulSoup
import re

def scrape_website(url):
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
            with open('website_content.txt', 'w', encoding='utf-8') as file:
                file.write(cleaned_text)

            print(f'Successfully scraped the website and saved content to website_content.txt')
        else:
            print(f'Failed to retrieve content from {url}. Status code: {response.status_code}')
    except Exception as e:
        print(f'An error occurred: {str(e)}')

# Example usage:
#url = input('Enter the URL of the website you want to scrape: ')
#scrape_website(url)

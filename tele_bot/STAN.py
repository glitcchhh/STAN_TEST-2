
from Gpt_logic import GP_Generate
from webScrap import scrape_website

GPT_API_KEY = "YOUR KEY"

gpt = GP_Generate(api_key=GPT_API_KEY)


class STAN:

    def __init__(self, query) -> None:
        self.query = query

    def do_magic(self):
        scrape_website(self.query)
        text_file_path = "website_content.txt" # Replace with the path to your text file
        gpt.add_text_file_to_history(text_file_path)
        final_article = gpt.ask()
        with open("website_content.txt", "w") as file:
            file.write(final_article)

        return text_file_path
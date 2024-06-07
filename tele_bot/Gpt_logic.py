from openai import OpenAI

class GP_Generate:
    """
    A class for generating text using the OpenAI API.

    Attributes:
        api_key (str): The API key used to authenticate with the OpenAI API.
        client (OpenAI): An instance of the OpenAI class for making API requests.
    """

    def __init__(self, api_key):
        """
        Initializes the Generate class with the provided API key.

        Args:
            api_key (str): The API key used to authenticate with the OpenAI API.
        """
        self.client = OpenAI(api_key=api_key)

    def read_text_file(self, file_path):
        """
        Reads the content of a text file.

        Args:
            file_path (str): The path to the text file.
        
        Returns:
            str: The content of the text file.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return None
        except Exception as e:
            print(f"An error occurred while reading the file: {str(e)}")
            return None

    def ask(self, file_path):
        """
        Generates text based on the content of the provided text file using the OpenAI API.

        Args:
            file_path (str): The path to the text file.

        Returns:
            str: The generated text containing answers to user queries.
        """
        content = self.read_text_file(file_path)
        if content is None:
            return "Error: Unable to read the file content."

        message = (
            "WRITE A NEWS ARTICLE USING THE DATA I GAVE YOU in 800 words AFTER THAT DO AN ANALYSIS OF THE ARTICLE INTO THREE SECTIONS "
            "TITLED: THE GOOD, THE BAD, THE GIST, WITH EACH SECTION CONSISTING OF 200 WORDS"
        )
        
        context = [
            {"role": "system", "content": content},
            {"role": "user", "content": message}
        ]

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",  # Specify the GPT model
            messages=context
        )
        response = completion.choices[0].message.content
        return response

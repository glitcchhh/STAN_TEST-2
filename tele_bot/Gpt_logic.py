from openai import OpenAI

class GP_Generate:
    """
    A class for generating text using the OpenAI API.

    Attributes:
        api_key (str): The API key used to authenticate with the OpenAI API.
        client (OpenAI): An instance of the OpenAI class for making API requests.
        conversation_history (list): A list to store conversation history.
    """

    def __init__(self, api_key):
        """
        Initializes the Generate class with the provided API key.

        Args:
            api_key (str): The API key used to authenticate with the OpenAI API.
        """
        self.client = OpenAI(api_key=api_key)
        self.conversation_history = []

    def add_text_file_to_history(self, file_path):
        """
        Adds the content of a text file to the beginning of the conversation history.

        Args:
            file_path (str): The path to the text file.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                self.conversation_history.insert(0, {"role": "system", "content": content})
                print(f"Text from file '{file_path}' added to conversation history.")
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {str(e)}")

    def ask(self):
        """
        Generates text based on the provided message using the OpenAI API.

        Returns:
            str: The generated text containing answers to user queries.
        """
        message = "WRITE A NEWS ARTICLE USING THE DATA I GAVE YOU in 1100 words include a seperate section called THE GOOD THE BAD THE GIST,each section with a word count of 200."
        query = "\nNew query: " + message
        self.conversation_history.append({"role": "user", "content": message})  # Add user query to conversation history
        context = [{"role": "system", "content": query}]
        context.extend(self.conversation_history[-5:])  # Include last 5 messages in the context
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",  # Specify the GPT model
            messages=context
        )
        response = completion.choices[0].message.content
        # Add AI response to conversation history with role 'assistant'
        self.conversation_history.append({"role": "assistant", "content": response})
        return response
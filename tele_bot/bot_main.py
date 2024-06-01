from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from STAN import STAN

# Define bot token and username
TOKEN: Final = "YOUR KEY"
BOT_USERNAME: Final = "@trendy_reporter_bot"

class TrendyBot:
    def __init__(self, update: Update, context: ContextTypes) -> None:
        self.update = update
        self.context = context
        self.help_text = """
🤖 **Trendy Reporter Bot Help**

Here are the available commands:
/start - Start a conversation with the bot
/help - Display this help message
/analyze [query] - Analyze a URL by scraping its content

Example:
/analyze https://example.com

Feel free to ask me anything! 🚀
"""
        self.hello_text = """
👋 Hello there!

Welcome to Trendy Reporter Bot. I'm here to provide you with the latest trends and insights.

Feel free to start a conversation with me or ask for assistance using the available commands.

Let's explore the trends together! 📈
"""

    # Command to start conversation with the bot
    async def start_command(self, update: Update, context: ContextTypes):
        await update.message.reply_text(f"{self.hello_text}")

    # Command to provide assistance
    async def help_command(self, update: Update, context: ContextTypes):
        await update.message.reply_text(f"{self.help_text}")

    # Command to analyze user's query (expects URL for website scraping)
    async def analyze_command(self, update: Update, context: ContextTypes):
        # Check if there are any arguments provided after the command
        if len(context.args) > 0:
            url = context.args[0]  # Extract the first argument as the URL
            s = STAN(query=url)  # Instantiate STAN class with the URL as the query
            file_name = s.do_magic()  # Perform website scraping
            
            await update.message.reply_document(document=open('content.txt', 'rb'), caption="content of website", filename="website content")
            await update.message.reply_document(document=open(file_name, "rb"), filename="Article", caption="gpt file")
        else:
            await update.message.reply_text("Please provide a URL after the /analyze command.")

    # Function to handle responses based on user input
    def handle_response(self, text: str) -> str:
        text = text.lower()
        match text:
            case "hello" : return self.hello_text
            case "help"  : return self.help_text
            case _ : return "I do not understand. Please provide a valid command. Use /help for more."

    # Function to handle incoming messages
    async def handle_message(self, update: Update, context: ContextTypes):
        # Determine the type of chat the message came from
        message_type: str = update.message.chat.type
        text: str = update.message.text
        print(f"User ({update.message.chat.id}) in {message_type}: {text}")

        # Handle bot responses based on chat type
        if message_type == 'group' and BOT_USERNAME in text:
            # Extract message excluding bot username
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = self.handle_response(new_text)
        elif message_type == 'private':
            response: str = self.handle_response(text)
        else:
            return

        print('Bot:', response)
        await update.message.reply_text(response)

    # Function to handle errors
    async def error(self, update: Update, context: ContextTypes):
        print(f"Update {update} caused error {context.error}")

if __name__ == "__main__":
    print("Starting Bot...")
    BOT = TrendyBot(update=None, context=None)  # Passing None for update and context as they're not used in __init__
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', BOT.start_command))
    app.add_handler(CommandHandler('help', BOT.help_command))
    app.add_handler(CommandHandler('analyze', BOT.analyze_command))

    # Register message handler
    app.add_handler(MessageHandler(filters.TEXT, BOT.handle_message))

    # Register error handler
    app.add_error_handler(BOT.error)

    # Start polling for updates (checks every 1 second)
    app.run_polling(poll_interval=1)

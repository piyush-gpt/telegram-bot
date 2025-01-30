# Telegram Bot with Gemini API, Image/File Analysis, and Web Search

This project is a Telegram bot that integrates several powerful features like user registration, Gemini-powered chat, image/file analysis, and web search. It uses the **Gemini API** to respond to user queries and analyze image contents, along with **MongoDB** to store user interactions and metadata.

## Features

### 1. **User Registration**
- Upon the first interaction, the bot saves the user’s details (first name, username, and chat ID) in **MongoDB**.
- Requests and stores the user’s phone number using Telegram’s contact button, followed by a confirmation message.

### 2. **Gemini-Powered Chat**
- The bot uses the **Gemini API** to answer user queries, providing detailed responses based on the context.
- It stores the chat history (user input and bot response) in **MongoDB** with timestamps.

### 3. **Image/File Analysis**
- Users can send images (JPG, PNG) and PDF files to the bot.
- The bot analyzes the content using **Gemini API** and returns a description of the content.
- Metadata such as file name and description is saved in **MongoDB**.

### 4. **Web Search**
- Users can perform a web search by typing `/websearch`.
- The bot uses an AI agent to search the web for the query and returns a summary of the results with top web links.

## Tech Stack

- **Backend**: Python
- **Telegram API**: Python-telegram-bot library
- **Gemini API**: Google’s generative AI for NLP tasks
- **Database**: MongoDB (for storing user details and chat history)
- **Libraries/Tools**:
  - `python-telegram-bot`
  - `pymongo`
  - `requests`
  - `google-generativeai`
  
## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/piyush-gpt/telegram-bot-gemini.git
    ```

2. Navigate to the project directory:
    ```bash
    cd telegram-bot-gemini
    ```

3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your **Telegram Bot** and obtain the **API Token** by following the instructions on the [Telegram BotFather](https://core.telegram.org/bots#botfather).

5. Set up your **Gemini API Key** (Google's generative AI) for querying the API.

6. Set up **MongoDB** and configure the database connection.

7. Create a `.env` file and add the necessary credentials (Telegram token, Gemini API key, MongoDB URI):
    ```bash
    TELEGRAM_API_TOKEN=your_telegram_bot_token
    GEMINI_API_KEY=your_gemini_api_key
    MONGO_URI=your_mongodb_uri
    ```

8. Run the bot:
    ```bash
    python bot.py
    ```

## Usage

- Start the bot in Telegram and interact with it.
- **User Registration**: The bot will store your information (first name, username, chat ID) and ask for your phone number.
- **Chat**: Ask the bot any query, and it will respond using the **Gemini API**.
- **Send an image/file**: Send an image or PDF file to get content analysis and metadata storage.
- **Web Search**: Use `/websearch` followed by your query to get a summary and web links.

## Contributing

Feel free to fork the repository, create an issue, or submit a pull request for new features or improvements.

## License

This project is open-source and available under the MIT License.

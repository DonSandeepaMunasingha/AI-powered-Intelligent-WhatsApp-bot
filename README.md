
# Sandeepa Restaurant WhatsApp Chatbot

## Overview

This project is a WhatsApp-based virtual assistant for Sandeepa Restaurant, named "DineMate". It leverages Retrieval-Augmented Generation (RAG) to provide context-aware responses to customer inquiries about reservations, menu, hours, delivery, and more. The bot integrates with Twilio for WhatsApp messaging and uses OpenRouter's API for AI-powered conversations, ensuring natural and helpful interactions.

## Features

- **WhatsApp Integration**: Seamlessly handles incoming messages via Twilio's WhatsApp Business API.
- **RAG-Powered Responses**: Retrieves relevant context from a predefined Q&A dataset using sentence embeddings and cosine similarity.
- **AI-Generated Replies**: Utilizes OpenRouter's Qwen model for human-like, adaptive responses.
- **Conversation Memory**: Maintains a history of the last 6 messages per user for contextual awareness.
- **Repeat Detection**: Detects and handles repeated questions by varying responses to avoid monotony.
- **Intent Hashing**: Uses MD5 hashing for efficient intent detection and repeat checking.
- **Error Handling**: Graceful fallbacks for API failures or unclear queries.

## Installation


2. **Install Dependencies**:

3. **Set Up Environment Variables**:
   Create a `.env` file or set environment variables for sensitive data:
   - `OPENROUTER_API_KEY`: Your OpenRouter API key (obtain from [OpenRouter](https://openrouter.ai/)).

## Configuration

1. **Twilio Setup**:
   - Sign up for a Twilio account and enable WhatsApp Sandbox or Business API.
   - Set the webhook URL for incoming messages to `https://your-domain.com/whatsapp` (replace with your deployed app's URL).
   - Note: For local testing, use ngrok to expose your local server.

2. **Q&A Data**:
   - The `qnada.json` file contains the knowledge base with questions and answers categorized by topics like hours, reservations, menu, etc.
   - Customize or expand this file as needed. It supports both dictionary and list formats.

3. **OpenRouter API**:
   - Ensure your API key is set. The bot uses the `qwen/qwen3-8b` model with tuned parameters for creativity and relevance.

## Usage

1. **Run the Application**:
  
   The Flask app will start on port 5000.

2. **Interact via WhatsApp**:
   - Send messages to your Twilio WhatsApp number.
   - The bot will respond based on the context retrieved from `qnada.json` and AI generation.
   - Example queries: "What are your opening hours?", "Can I make a reservation?", "Do you have vegetarian options?"

3. **Testing**:
   - Use Twilio's sandbox for testing without a real WhatsApp number.
   - Monitor logs for conversation history and API responses.

## Project Structure

- `app.py`: Main Flask application handling WhatsApp webhooks, AI calls, and conversation logic.
- `rag.py`: Implements RAG functionality, including embedding generation and context retrieval.
- `qnada.json`: JSON file containing Q&A pairs and categories for the restaurant's knowledge base.
- `README.md`: This file, providing project documentation.

## Dependencies

- `flask`: Web framework for the API.
- `twilio`: For WhatsApp messaging integration.
- `requests`: HTTP library for API calls.
- `sentence-transformers`: For generating sentence embeddings.
- `numpy`: For vector operations and similarity calculations.

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Make changes and test thoroughly.
4. Submit a pull request with a clear description of the changes.

For issues or suggestions, please open an issue on the repository.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

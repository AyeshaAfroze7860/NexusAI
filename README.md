# NexusAI - Intelligent Local AI Chatbot

## Project Overview

NexusAI is an intelligent conversational chatbot developed using Python, Streamlit, LangChain, and Ollama. It uses a locally hosted Large Language Model (LLM) to generate responses and LangChain conversation memory to maintain context across interactions.

The application provides a user-friendly chat interface where users can ask questions, explore topics, and interact with an AI assistant without relying on cloud-based LLM APIs.

## Features

- Local LLM Integration using Ollama.
- Llama 3.2 model for intelligent response generation.
- LangChain integration for prompt management.
- Conversation memory using InMemoryChatMessageHistory.
- Context-aware responses using RunnableWithMessageHistory.
- Unique session management for conversations.
- Adjustable response creativity through temperature settings.
- Interactive chatbot interface using Streamlit.
- Clear conversation and new conversation options.
- Error handling for local model connectivity.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | User interface |
| LangChain | LLM application framework |
| Ollama | Local LLM runtime |
| Llama 3.2 | Language model |

## Project Structure

```text
NexusAI/
│
├── app.py
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/NexusAI.git
```

### 2. Navigate to the Project Directory

```bash
cd NexusAI
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Install Ollama

Download and install Ollama from:

https://ollama.com/download

### 7. Download the Llama 3.2 Model

```bash
ollama pull llama3.2
```

### 8. Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser.

## How It Works

NexusAI follows a conversational processing workflow:

1. The user enters a question through the Streamlit chat interface.
2. LangChain receives the input and retrieves the previous conversation history.
3. The prompt template combines system instructions, conversation history, and the current question.
4. Ollama sends the structured prompt to the locally running Llama 3.2 model.
5. The language model generates a response.
6. LangChain automatically updates the conversation history with the user input and AI response.
7. The response is displayed in the Streamlit interface.

## LangChain Memory Implementation

The project uses the following LangChain components for conversation memory:

- **InMemoryChatMessageHistory:** Stores previous user messages and AI responses in memory.
- **MessagesPlaceholder:** Inserts conversation history into the prompt.
- **RunnableWithMessageHistory:** Automatically manages message history during chatbot interactions.
- **Session ID:** Maintains separate conversation histories for different sessions.

This allows NexusAI to understand previous interactions and generate context-aware responses.

## Configuration

The chatbot supports adjustable model settings through the sidebar.

| Parameter | Description |
|---|---|
| Model | Selects the local language model |
| Temperature | Controls response creativity |
| Memory | Enables conversation history |
| Clear Conversation | Removes the current conversation |
| New Conversation | Starts a fresh session |

## Requirements

- Python 3.9 or above
- Ollama installed and running
- Llama 3.2 model downloaded
- Internet connection for initial package and model downloads

## Future Enhancements

- Persistent conversation memory using SQLite.
- Chat history management.
- Export conversations as text or PDF.
- Document-based question answering.
- Support for additional local language models.
- Improved chatbot interface.
- Streaming AI responses.

## Limitations

- Conversation memory is stored in application memory and is not persistent across application restarts.
- Response speed depends on the system hardware.
- The chatbot requires Ollama and a locally installed language model.

# AI Agentic RAG with CrewAI

This project implements a multi-agent AI system using the **CrewAI** framework to perform **Retrieval-Augmented Generation (RAG)**. It features a researcher agent for information gathering from the web and a writer agent for composing comprehensive answers. The entire system is exposed via a RESTful API built with **LitServe**, and a command-line client is provided for interaction.

## ✨ Features

-   **Multi-Agent System**: Utilizes a "crew" of AI agents, including a `Senior Researcher` and a `Senior Writer`, to handle complex queries.
    
-   **Extensible Toolset**: Agents are equipped with tools to access external information:
    
    -   **FireCrawl**: For real-time web searching and content scraping.
        
    -   **Vector Database**: A placeholder for searching internal knowledge bases (can be integrated with ChromaDB, Pinecone, etc.).
        
-   **API-driven**: The agentic crew is served via a LitServe API, making it easy to integrate with other applications.
    
-   **Simple Client**: Includes a command-line client (`client.py`) to easily send queries to the server and receive generated responses.
    

----------

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

-   Python 3.8+
    
-   An API key from [FireCrawl](https://www.firecrawl.dev/)
    

### Installation & Configuration

1.  **Clone the repository:**
    
    Bash
    
    ```
    git clone <your-repository-url>
    cd <your-repository-directory>
    
    ```
    
2.  **Create and activate a virtual environment:**
    
    Bash
    
    ```
    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    
    # For Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    
    ```
    
3.  **Install the required dependencies:**
    
    Bash
    
    ```
    pip install -r requirements.txt
    
    ```
    
4.  **Set up your environment variables:** Create a file named `.env` in the root of the project directory and add your FireCrawl API key:
    
    ```
    FIRECRAWL_API_KEY="your_firecrawl_api_key_here"
    
    ```
    

----------

## usage

### 1. Run the Server

Start the LitServe API server, which hosts the AI agents. The server will run on `http://127.0.0.1:8000`.

Bash

```
python server.py

```

### 2. Run the Client

In a new terminal window (with the virtual environment activated), use the `client.py` script to send a query to the server.

Bash

```
python client.py --query "What are the latest advancements in AI?"

```

The client will print the final, polished answer from the AI crew in JSON format.

----------

## ⚙️ How It Works

The project follows a simple yet powerful workflow:

1.  The **`client.py`** sends a user's query to the `/predict` endpoint on the **`server.py`**.
    
2.  The LitServe API receives the request and kicks off the **CrewAI crew**.
    
3.  The **`Senior Researcher`** agent receives the query as its first task. It uses the **`FireCrawlSearchTool`** or **`VectorDBSearchTool`** to gather relevant information.
    
4.  Once the research is complete, the findings are passed to the **`Senior Writer`** agent.
    
5.  The **`Senior Writer`** agent synthesizes the research into a clear, concise, and well-structured final answer.
    
6.  The final answer is sent back to the client as a JSON response.
    

----------

## 📂 Project Structure

```
├── .gitignore         # Specifies files for Git to ignore
├── client.py          # Command-line client to interact with the API
├── requirements.txt   # A list of all Python dependencies
├── server.py          # The main application server using LitServe and CrewAI
└── tools.py           # Defines custom tools for the CrewAI agents
```

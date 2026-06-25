# slashAsk

AI-Powered Multi-Document Question Answering System

## Features

- PDF Upload
- DOCX Upload
- Excel Upload
- CSV Upload
- FAISS Vector Search
- RAG Architecture
- FastAPI Backend
- Streamlit Frontend
- Groq LLM Integration
- Fully Dockerized for Easy Deployment

## Tech Stack

- Python
- FastAPI
- Streamlit
- FAISS
- Sentence Transformers
- Groq API
- Docker & Docker Compose

## Quick Start (Local)

1. Create a `.env` file in the root directory and add your `GROQ_API_KEY`:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```
2. Start the application locally using the provided script:
   ```bash
   python run.py
   ```
   This will start both the backend on port `8000` and the frontend on port `8501`, opening the browser automatically.

## Deployment (Docker)

The easiest way to deploy this application to a Cloud Provider or VPS (e.g., AWS EC2, DigitalOcean, Render) is by using the provided Docker Compose configuration.

1. Ensure **Docker** and **Docker Compose** are installed on your server.
2. Clone the repository and ensure your `.env` file contains the `GROQ_API_KEY`.
3. Run the following command in the project root to build and launch the services:
   ```bash
   docker-compose up -d --build
   ```
4. The application will be running and accessible via port `8501` (e.g. `http://your-server-ip:8501`).
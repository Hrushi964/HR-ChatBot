# Chat with PDF Application

This application allows users to chat with PDF documents using a local LLM (Mistral-7B) and provides holiday information through a SQLite database.

## Features

- Chat with PDF documents using Mistral-7B model
- Holiday information lookup
- Simple and intuitive web interface

## Deployment on Hugging Face Spaces

This application is configured to run on Hugging Face Spaces using Docker. To deploy:

1. Create a new Space on Hugging Face
2. Choose "Docker" as the SDK
3. Push your code to the Space repository
4. The application will automatically build and deploy

The application will be available at your Hugging Face Space URL.

## Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Access the application at `http://localhost:7860`

## Environment Variables

Create a `.env` file with the following variables:
```
MODEL_PATH=path/to/your/model.gguf
```

## Project Structure

- `app.py`: Main Flask application
- `main.py`: LLM chain initialization and PDF processing
- `holiday_db.py`: Holiday database operations
- `index.html`: Web interface
- `Dockerfile`: Docker configuration for Hugging Face Spaces
- `requirements.txt`: Python dependencies

## Dependencies

- Flask
- LangChain
- Llama-cpp-python
- PyPDF2
- SQLite3
- Other dependencies listed in requirements.txt 
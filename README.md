# PDF Chat Assistant

A web application that allows users to chat with their PDF documents and query holiday information.

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/<your-github-username>/pdf-chat-assistant.git
cd pdf-chat-assistant
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download required files:
   - Download the Mistral model from [here](https://huggingface.co/TheBloke/Mistral-7B-OpenOrca-GGUF/resolve/main/mistral-7b-openorca.Q4_0.gguf)
   - Place it in the project root directory
   - Add your PDF files to the project root directory

5. Run the application:
```bash
python app.py
```

6. Open your browser and go to:
```
http://localhost:5000
```

## Features

- Chat with PDF documents
- Query holiday information
- Support for multiple PDFs
- Modern web interface
- Holiday database with public and cultural holidays

## Deployment

This application is configured for deployment on Render.com. Follow these steps:

1. Create a Render.com account
2. Create a new Web Service
3. Connect your GitHub repository
4. Deploy!

## Environment Variables

Create a `.env` file with the following variables:
```
FLASK_APP=app.py
FLASK_ENV=production
PYTHON_VERSION=3.9.0
MODEL_PATH=./mistral-7b-openorca.Q4_0.gguf
``` 
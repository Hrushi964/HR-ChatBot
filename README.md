# Chat with PDF Application

This application allows users to chat with PDF documents using a local LLM (Mistral-7B) and provides holiday information through a SQLite database.

## Features

- Chat with PDF documents using Mistral-7B model
- Holiday information lookup
- Simple and intuitive web interface

## Deployment on Replit

This application is configured to run on Replit. To deploy:

1. Create a new Repl on Replit.com
2. Choose "Python" as your template
3. Import your code into the Repl
4. Add your environment variables in the Replit Secrets tab:
   - `MODEL_PATH`: Path to your model file
5. Click "Run" to start the application

The application will be available at your Replit URL.

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

4. Access the application at `http://localhost:8080`

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
- `.replit`: Replit configuration file
- `requirements.txt`: Python dependencies

## Dependencies

- Flask
- LangChain
- Llama-cpp-python
- PyPDF2
- SQLite3
- Other dependencies listed in requirements.txt 
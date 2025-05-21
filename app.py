from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from main import initialize_chain
from holiday_db import get_holidays_by_month, get_holidays_by_year, is_holiday
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize the chain when the app starts
answer_gen_chain = initialize_chain()

def process_holiday_query(question):
    # Check for specific date query (e.g., "is jan 1 2025 holiday")
    date_pattern = r'(?:is\s+)?(\w+)\s+(\d{1,2})(?:\s+(\d{4}))?\s+holiday'
    date_match = re.search(date_pattern, question.lower())
    if date_match:
        month, day, year = date_match.groups()
        year = year or datetime.now().year
        try:
            date = datetime.strptime(f"{year}-{month[:3]}-{day}", "%Y-%b-%d")
            holiday = is_holiday(date.strftime("%Y-%m-%d"))
            if holiday:
                return f"Yes, {date.strftime('%B %d, %Y')} is {holiday[0]}. {holiday[1]}"
            return f"No, {date.strftime('%B %d, %Y')} is not a holiday."
        except ValueError:
            return "I couldn't understand the date format. Please try again."

    # Check for month query (e.g., "holidays in jan")
    month_pattern = r'holidays\s+in\s+(\w+)(?:\s+(\d{4}))?'
    month_match = re.search(month_pattern, question.lower())
    if month_match:
        month, year = month_match.groups()
        year = year or datetime.now().year
        try:
            month_num = datetime.strptime(month[:3], "%b").month
            holidays = get_holidays_by_month(month_num, year)
            if holidays:
                response = f"Holidays in {month.capitalize()} {year}:\n"
                for date, name, desc in holidays:
                    response += f"- {datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')}: {name}\n"
                return response
            return f"No holidays found in {month.capitalize()} {year}"
        except ValueError:
            return "I couldn't understand the month format. Please try again."

    # Check for year query (e.g., "holidays in 2025")
    year_pattern = r'holidays\s+in\s+(\d{4})'
    year_match = re.search(year_pattern, question.lower())
    if year_match:
        year = year_match.group(1)
        holidays = get_holidays_by_year(year)
        if holidays:
            response = f"Holidays in {year}:\n"
            for date, name, desc in holidays:
                response += f"- {datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')}: {name}\n"
            return response
        return f"No holidays found in {year}"

    return None

@app.route('/')
def serve_index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        # First check if it's a holiday query
        holiday_response = process_holiday_query(question)
        if holiday_response:
            return jsonify({
                'answer': holiday_response,
                'sources': ['Holiday Database']
            })
        
        # If not a holiday query, use the LLM
        result = answer_gen_chain.invoke({"question": question})
        return jsonify({
            'answer': result['answer'],
            'sources': [doc.metadata.get('source', 'Unknown') for doc in result.get('source_documents', [])]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7860))
    app.run(host='0.0.0.0', port=port, debug=False) 
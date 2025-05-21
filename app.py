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
    q = question.lower().strip()
    # 1. Check for year query (e.g., "holidays in 2025", "holidays in 24")
    year_pattern = r'holidays\s+in\s+(\d{2,4})'
    year_match = re.search(year_pattern, q)
    if year_match:
        year = year_match.group(1)
        if len(year) == 2:
            year = '20' + year  # assume 20xx for 2-digit years
        holidays = get_holidays_by_year(year)
        if holidays:
            response = f"Holidays in {year}:\n"
            for date, name, desc in holidays:
                response += f"- {datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')}: {name}\n"
            return response
        return f"No holidays found in {year}"

    # 2. Check for month+year queries (e.g., "holidays in jan 2024", "holidays in 2024 jan")
    month_year_patterns = [
        r'holidays\s+in\s+(\w+)\s+(\d{2,4})',  # holidays in jan 2024
        r'holidays\s+in\s+(\d{2,4})\s+(\w+)'   # holidays in 2024 jan
    ]
    for pat in month_year_patterns:
        match = re.search(pat, q)
        if match:
            m, y = match.groups()
            # Try to parse which is month and which is year
            if m.isdigit():
                year = m if len(m) == 4 else '20' + m
                month = y
            else:
                year = y if len(y) == 4 else '20' + y if len(y) == 2 else y
                month = m
            try:
                # Accept both numeric and string months
                if month.isdigit():
                    month_num = int(month)
                else:
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

    # 3. Check for month-only queries (e.g., "holidays in jan", "holidays in 1")
    month_pattern = r'holidays\s+in\s+(\w+)'
    month_match = re.search(month_pattern, q)
    if month_match:
        month = month_match.group(1)
        year = datetime.now().year
        try:
            if month.isdigit():
                month_num = int(month)
            else:
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

    # 4. Check for specific date queries (e.g., "is jan 1 2025 holiday", "is 1 jan 2025 holiday", "is 1-1-2024 holiday")
    date_patterns = [
        r'(?:is\s+)?(\w+)\s+(\d{1,2})(?:\s+(\d{2,4}))?\s+holiday',  # is jan 1 2025 holiday
        r'(?:is\s+)?(\d{1,2})\s+(\w+)(?:\s+(\d{2,4}))?\s+holiday',  # is 1 jan 2025 holiday
        r'(?:is\s+)?(\d{1,2})[-/](\d{1,2})[-/](\d{2,4})\s+holiday'    # is 1-1-2024 holiday
    ]
    for pat in date_patterns:
        match = re.search(pat, q)
        if match:
            g = match.groups()
            try:
                if len(g) == 3:
                    if pat.startswith(r'(?:is\s+)?(\w+)'):
                        # jan 1 2025
                        month, day, year = g
                    elif pat.startswith(r'(?:is\s+)?(\d{1,2})\s+(\w+)'):
                        # 1 jan 2025
                        day, month, year = g
                    else:
                        # 1-1-2024
                        day, month, year = g
                    year = year or str(datetime.now().year)
                    if len(year) == 2:
                        year = '20' + year
                    if month.isdigit():
                        month_num = int(month)
                    else:
                        month_num = datetime.strptime(month[:3], "%b").month
                    date = datetime(int(year), int(month_num), int(day))
                    holiday = is_holiday(date.strftime("%Y-%m-%d"))
                    if holiday:
                        return f"Yes, {date.strftime('%B %d, %Y')} is {holiday[0]}. {holiday[1]}"
                    return f"No, {date.strftime('%B %d, %Y')} is not a holiday."
            except Exception:
                return "I couldn't understand the date format. Please try again."

    return None

@app.route('/')
def serve_index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')

@app.route('/ask', methods=['POST'])
def ask():
    print("ASK endpoint called")
    data = request.json
    print("Request data:", data)
    question = data.get('question', '')
    print("Question:", question)
    
    if not question:
        print("No question provided")
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        print("Checking for holiday query...")
        holiday_response = process_holiday_query(question)
        if holiday_response:
            print("Holiday response found:", holiday_response)
            return jsonify({
                'answer': holiday_response,
                'sources': ['Holiday Database']
            })
        
        print("Invoking answer_gen_chain...")
        result = answer_gen_chain.invoke({"question": question})
        print("Result:", result)
        return jsonify({
            'answer': result['answer'],
            'sources': [doc.metadata.get('source', 'Unknown') for doc in result.get('source_documents', [])]
        })
    except Exception as e:
        import traceback
        print("Error:", e)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False) 
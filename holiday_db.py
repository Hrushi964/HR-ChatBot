import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('holidays.db')
    c = conn.cursor()
    
    # Create holidays table
    c.execute('''
        CREATE TABLE IF NOT EXISTS holidays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            is_public BOOLEAN DEFAULT 1
        )
    ''')
    
    # Create indexes for faster queries
    c.execute('CREATE INDEX IF NOT EXISTS idx_date ON holidays(date)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_month ON holidays(strftime("%m", date))')
    c.execute('CREATE INDEX IF NOT EXISTS idx_year ON holidays(strftime("%Y", date))')
    
    conn.commit()
    conn.close()

def add_holiday(date, name, description="", is_public=True):
    conn = sqlite3.connect('holidays.db')
    c = conn.cursor()
    c.execute('INSERT INTO holidays (date, name, description, is_public) VALUES (?, ?, ?, ?)',
              (date, name, description, is_public))
    conn.commit()
    conn.close()

def get_holidays_by_month(month, year):
    conn = sqlite3.connect('holidays.db')
    c = conn.cursor()
    c.execute('''
        SELECT date, name, description 
        FROM holidays 
        WHERE strftime("%m", date) = ? AND strftime("%Y", date) = ?
        ORDER BY date
    ''', (f"{int(month):02d}", str(year)))
    holidays = c.fetchall()
    conn.close()
    return holidays

def get_holidays_by_year(year):
    conn = sqlite3.connect('holidays.db')
    c = conn.cursor()
    c.execute('''
        SELECT date, name, description 
        FROM holidays 
        WHERE strftime("%Y", date) = ?
        ORDER BY date
    ''', (str(year),))
    holidays = c.fetchall()
    conn.close()
    return holidays

def is_holiday(date):
    conn = sqlite3.connect('holidays.db')
    c = conn.cursor()
    c.execute('SELECT name, description FROM holidays WHERE date = ?', (date,))
    holiday = c.fetchone()
    conn.close()
    return holiday

# Initialize database with some sample data
def add_sample_holidays():
    holidays = [
        
    # 2024 - Public Holidays
    ("2024-01-01", "New Year's Day", "Public holiday"),
    ("2024-01-26", "Republic Day", "Public holiday"),
    ("2024-03-08", "Holi", "Public holiday"),
    ("2024-04-09", "Ram Navami", "Public holiday"),
    ("2024-05-01", "Labour Day", "Public holiday"),
    ("2024-08-15", "Independence Day", "Public holiday"),
    ("2024-10-02", "Gandhi Jayanti", "Public holiday"),
    ("2024-12-25", "Christmas Day", "Public holiday"),

    # 2024 - Cultural Holidays
    ("2024-01-14", "Makar Sankranti / Pongal", "Cultural holiday"),
    ("2024-03-08", "Mahashivratri", "Cultural holiday"),
    ("2024-03-29", "Good Friday", "Cultural holiday"),
    ("2024-04-10", "Eid-ul-Fitr", "Cultural holiday"),
    ("2024-04-21", "Mahavir Jayanti", "Cultural holiday"),
    ("2024-05-23", "Buddha Purnima", "Cultural holiday"),
    ("2024-06-17", "Eid-ul-Adha (Bakrid)", "Cultural holiday"),
    ("2024-07-17", "Muharram", "Cultural holiday"),
    ("2024-08-19", "Raksha Bandhan", "Cultural holiday"),
    ("2024-08-26", "Janmashtami", "Cultural holiday"),
    ("2024-09-07", "Ganesh Chaturthi", "Cultural holiday"),
    ("2024-09-16", "Milad-un-Nabi", "Cultural holiday"),
    ("2024-10-12", "Dussehra (Vijayadashami)", "Cultural holiday"),
    ("2024-11-01", "Diwali", "Cultural holiday"),
    ("2024-11-03", "Bhai Dooj", "Cultural holiday"),
    ("2024-11-07", "Chhath Puja", "Cultural holiday"),
    ("2024-11-15", "Guru Nanak Jayanti", "Cultural holiday"),

    # 2025 - Public Holidays
    ("2025-01-01", "New Year's Day", "Public holiday"),
    ("2025-01-26", "Republic Day", "Public holiday"),
    ("2025-03-25", "Holi", "Public holiday"),
    ("2025-03-29", "Ram Navami", "Public holiday"),
    ("2025-05-01", "Labour Day", "Public holiday"),
    ("2025-08-15", "Independence Day", "Public holiday"),
    ("2025-10-02", "Gandhi Jayanti", "Public holiday"),
    ("2025-12-25", "Christmas Day", "Public holiday"),

    # 2025 - Cultural Holidays
    ("2025-01-14", "Makar Sankranti / Pongal", "Cultural holiday"),
    ("2025-02-26", "Mahashivratri", "Cultural holiday"),
    ("2025-03-31", "Eid-ul-Fitr", "Cultural holiday"),
    ("2025-04-10", "Good Friday", "Cultural holiday"),
    ("2025-04-13", "Mahavir Jayanti", "Cultural holiday"),
    ("2025-05-12", "Buddha Purnima", "Cultural holiday"),
    ("2025-06-07", "Eid-ul-Adha (Bakrid)", "Cultural holiday"),
    ("2025-07-06", "Muharram", "Cultural holiday"),
    ("2025-08-09", "Raksha Bandhan", "Cultural holiday"),
    ("2025-08-16", "Janmashtami", "Cultural holiday"),
    ("2025-08-27", "Ganesh Chaturthi", "Cultural holiday"),
    ("2025-09-05", "Milad-un-Nabi", "Cultural holiday"),
    ("2025-10-01", "Dussehra (Vijayadashami)", "Cultural holiday"),
    ("2025-10-20", "Diwali", "Cultural holiday"),
    ("2025-10-22", "Bhai Dooj", "Cultural holiday"),
    ("2025-11-05", "Chhath Puja", "Cultural holiday"),
    ("2025-11-13", "Guru Nanak Jayanti", "Cultural holiday")


    ]
    
    conn = sqlite3.connect('holidays.db')
    c = conn.cursor()
    c.executemany('INSERT OR IGNORE INTO holidays (date, name, description) VALUES (?, ?, ?)', holidays)
    conn.commit()
    conn.close()

# Initialize database when module is imported
init_db()
add_sample_holidays() 
import sqlite3

# Connect to the database (or create it)
conn = sqlite3.connect('subscription_box.db')
cursor = conn.cursor()

# Create users table (only once)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        preferences TEXT
    )
''')

# Create products table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        tags TEXT
    )
''')

# Optional: Insert sample data
cursor.execute("INSERT INTO products (name, category, tags) VALUES (?, ?, ?)",
               ("Organic Green Tea", "beverage", "organic,tea,healthy"))

conn.commit()
conn.close()

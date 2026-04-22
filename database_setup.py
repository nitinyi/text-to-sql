import sqlite3

db = sqlite3.connect('ecommerce.db')
c = db.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand TEXT,
    price REAL NOT NULL,
    category_id INTEGER NOT NULL,
    stock_quantity INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories (category_id)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    FOREIGN KEY (product_id) REFERENCES products (product_id)
)
''')

db.commit()
db.close()
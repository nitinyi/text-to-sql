import sqlite3

db = sqlite3.connect('ecommerce.db')
c = db.cursor()

cats = [
    ('Groceries',),
    ('Personal Care',),
    ('Household',),
    ('Beverages',),
    ('Snacks',)
]
c.executemany("INSERT OR IGNORE INTO categories (name) VALUES (?)", cats)

c.execute("SELECT category_id, name FROM categories")
cat_ids = {name: cid for cid, name in c.fetchall()}

items = [
    ('Tata Salt', 'Tata', 28.00, cat_ids['Groceries'], 200),
    ('Fortune Sunflower Oil 1L', 'Fortune', 145.00, cat_ids['Groceries'], 80),
    ('Aashirvaad Atta 5kg', 'Aashirvaad', 210.00, cat_ids['Groceries'], 60),
    ('India Gate Basmati Rice 1kg', 'India Gate', 95.00, cat_ids['Groceries'], 120),
    ('Maggi Noodles 4 Pack', 'Maggi', 98.00, cat_ids['Snacks'], 150),
    ('Kissan Mixed Fruit Jam 500g', 'Kissan', 85.00, cat_ids['Groceries'], 90),
    ('Britannia Good Day Biscuits', 'Britannia', 30.00, cat_ids['Snacks'], 300),
    ('Parle-G Glucose Biscuits', 'Parle', 10.00, cat_ids['Snacks'], 500),
    ('Haldirams Aloo Bhujia 400g', 'Haldirams', 75.00, cat_ids['Snacks'], 110),
    ('Taj Mahal Tea 250g', 'Brooke Bond', 130.00, cat_ids['Beverages'], 70),
    ('Nescafe Classic Coffee 50g', 'Nescafe', 160.00, cat_ids['Beverages'], 45),
    ('Red Label Tea 500g', 'Brooke Bond', 240.00, cat_ids['Beverages'], 55),
    ('Coca Cola 750ml', 'Coca Cola', 40.00, cat_ids['Beverages'], 200),
    ('Thums Up 750ml', 'Thums Up', 40.00, cat_ids['Beverages'], 180),
    ('Patanjali Aloe Vera Gel 150ml', 'Patanjali', 65.00, cat_ids['Personal Care'], 130),
    ('Dettol Handwash 200ml', 'Dettol', 75.00, cat_ids['Personal Care'], 150),
    ('Santoor Sandal Soap 100g', 'Santoor', 35.00, cat_ids['Personal Care'], 250),
    ('Pears Pure & Gentle Soap', 'Pears', 55.00, cat_ids['Personal Care'], 200),
    ('Colgate Strong Teeth Paste 200g', 'Colgate', 85.00, cat_ids['Personal Care'], 180),
    ('Vim Dishwash Bar 250g', 'Vim', 20.00, cat_ids['Household'], 400),
    ('Surf Excel Matic Liquid 1L', 'Surf Excel', 290.00, cat_ids['Household'], 60),
    ('Harpic Bathroom Cleaner 500ml', 'Harpic', 110.00, cat_ids['Household'], 100),
    ('Odonil Room Freshner 50g', 'Odonil', 45.00, cat_ids['Household'], 150),
    ('Prestige Pressure Cooker 3L', 'Prestige', 1250.00, cat_ids['Household'], 20),
    ('Pigeon Non Stick Tawa', 'Pigeon', 450.00, cat_ids['Household'], 30),
    ('Bajaj LED Bulb 9W', 'Bajaj', 99.00, cat_ids['Household'], 120),
    ('Eveready AA Batteries 4 Pack', 'Eveready', 85.00, cat_ids['Household'], 80),
    ('Amul Butter 500g', 'Amul', 120.00, cat_ids['Groceries'], 100),
    ('Mother Dairy Full Cream Milk 1L', 'Mother Dairy', 60.00, cat_ids['Groceries'], 0),
    ('Yippee Noodles 4 Pack', 'Yippee', 85.00, cat_ids['Snacks'], 140)
]

c.executemany('''
INSERT INTO products (name, brand, price, category_id, stock_quantity)
VALUES (?, ?, ?, ?, ?)
''', items)

c.execute("SELECT product_id FROM products")
pids = [row[0] for row in c.fetchall()]

revs = [
    (pids[0], 5, 'Perfect salt, iodised.'),
    (pids[2], 4, 'Good quality atta.'),
    (pids[4], 5, 'Maggi is love.'),
    (pids[9], 5, 'Best tea.'),
    (pids[15], 4, 'Nice fragrance.'),
    (pids[20], 5, 'Cleans well.'),
    (pids[24], 4, 'Heats evenly.'),
    (pids[27], 5, 'Fresh butter.'),
    (pids[28], 3, 'Milk was okay.'),
    (pids[7], 5, 'Childhood favourite.')
]

c.executemany('''
INSERT INTO reviews (product_id, rating, comment) VALUES (?, ?, ?)
''', revs)

db.commit()
db.close()

print("Done.")
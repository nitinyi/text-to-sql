import sqlite3
import os
import re
import google.genai as genai
from flask import Flask, request, render_template_string


genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))


model_name = None
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods and "flash" in m.name:
        model_name = m.name
        break
model = genai.GenerativeModel(model_name)

prompt = """
Output ONLY the SQL query. No extra text.
Schema:
products(product_id, name, brand, price, category_id, stock_quantity)
categories(category_id, name)
reviews(review_id, product_id, rating)

Examples:
User: Find all Tata products
SQL: SELECT * FROM products WHERE brand = 'Tata';

User: Show all products under 100
SQL: SELECT name, price FROM products WHERE price < 100;

User: Show out of stock products
SQL: SELECT name FROM products WHERE stock_quantity = 0;

Question: %s
SQL:
"""

def ask(question):
    full = prompt % question
    reply = model.generate_content(full)
    text = reply.text.strip()
    text = text.replace("```sql", "").replace("```", "")
    match = re.search(r"SELECT .*?;", text, re.IGNORECASE | re.DOTALL)
    if match:
        sql = match.group(0).strip()
    else:
        sql = text.strip()
   
    sql = re.sub(r"brand\s*=\s*([a-zA-Z]+)", r"brand = '\1'", sql, flags=re.IGNORECASE)
    return sql

def run(sql):
    conn = sqlite3.connect("ecommerce.db")
    cur = conn.cursor()
    cur.execute(sql)
    cols = [d[0] for d in cur.description] if cur.description else []
    rows = cur.fetchall()
    conn.close()
    return cols, rows

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Store DB Chat</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f7fa;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .card {
            width: 100%;
            max-width: 1200px;
            background: white;
            border-radius: 24px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.08);
            padding: 32px;
        }
        h2 {
            font-size: 28px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 8px;
        }
        .subhead {
            color: #64748b;
            margin-bottom: 28px;
            font-size: 15px;
        }
        .search-form {
            display: flex;
            gap: 12px;
            margin-bottom: 32px;
        }
        .search-form input {
            flex: 1;
            padding: 16px 20px;
            font-size: 16px;
            border: 1.5px solid #e2e8f0;
            border-radius: 100px;
            outline: none;
            transition: border 0.15s, box-shadow 0.15s;
            background: #fafbfc;
        }
       
        .search-form button {
            padding: 16px 32px;
            font-size: 16px;
            font-weight: 500;
            color: white;
            background: #000000;
            border: none;
            border-radius: 100px;
            cursor: pointer;
            transition: background 0.15s;
        }
        
        .sql-box {
            background: #000000;
            color: #e2e8f0;
            padding: 16px 20px;
            border-radius: 16px;
            margin-bottom: 28px;
            font-family: 'SF Mono', 'Menlo', 'Monaco', 'Cascadia Code', monospace;
            font-size: 14px;
            overflow-x: auto;
            white-space: pre-wrap;
            word-break: break-all;
        }
        .sql-box code {
            color: #f3f3f3;
        }
        .error-box {
            background: #fee2e2;
            color: #b91c1c;
            padding: 16px 20px;
            border-radius: 16px;
            margin-bottom: 20px;
        }
        .results-header {
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            margin-bottom: 16px;
        }
        .results-header h3 {
            font-size: 18px;
            font-weight: 600;
            color: #1e293b;
        }
        .results-count {
            color: #64748b;
            font-size: 14px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        }
        th {
            text-align: left;
            padding: 14px 16px;
            background: #f8fafc;
            color: #334155;
            font-weight: 600;
            font-size: 14px;
            border-bottom: 1px solid #e2e8f0;
        }
        td {
            padding: 14px 16px;
            border-bottom: 1px solid #eef2f6;
            color: #1e293b;
        }
        tr:last-child td {
            border-bottom: none;
        }
      
        .no-results {
            color: #64748b;
            padding: 20px 0;
            text-align: center;
            background: #f8fafc;
            border-radius: 16px;
        }
        .footer-note {
            margin-top: 24px;
            font-size: 13px;
            color: #94a3b8;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>E-Commerce Product Search</h2>
        <h2>Text-to-SQL Assistant</h2>
        
        <div class="subhead">Ask questions in English & AI generates SQL queries instantly</div>
        
        <form method="POST" class="search-form">
            <input type="text" name="question" placeholder="e.g., products under 100 rupees" value="{{ question }}" autofocus>
            <button type="submit">Ask</button>
        </form>

        {% if sql %}
        <div class="sql-box">
            <code>{{ sql }}</code>
        </div>
        {% endif %}

        {% if error %}
        <div class="error-box">
             {{ error }}
        </div>
        {% elif rows %}
        <div class="results-header">
            <h3> Results</h3>
            <span class="results-count">{{ rows|length }} row(s)</span>
        </div>
        <table>
            <thead>
                <tr>
                    {% for col in columns %}
                    <th>{{ col }}</th>
                    {% endfor %}
                </tr>
            </thead>
            <tbody>
                {% for row in rows %}
                <tr>
                    {% for cell in row %}
                    <td>{{ cell }}</td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% elif question %}
        <div class="no-results">
            No products found for your query.
        </div>
        {% endif %}
        
        <div class="footer-note">
            Gemini • SQLite • Flask
        </div>
    </div>
</body>
</html>
"""

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    question = ""
    sql = ""
    columns = []
    rows = []
    error = ""

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if question:
            try:
                sql = ask(question)
                columns, rows = run(sql)
            except Exception as e:
                error = str(e)
                rows = []

    return render_template_string(HTML,
                                  question=question,
                                  sql=sql,
                                  columns=columns,
                                  rows=rows,
                                  error=error)

if __name__ == "__main__":
    app.run(debug=False, port=8000)

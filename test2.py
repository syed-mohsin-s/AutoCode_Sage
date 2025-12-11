# app.py
# INTENTIONAL_VULN: HARD_CODED_SECRET, SQL_INJECTION, STORED_XSS
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# INTENTIONAL_VULN: hard-coded secret
API_KEY = "supersecretapikey123"  # INTENTIONAL_VULN: HARD_CODED_SECRET

def get_db():
    conn = sqlite3.connect('test.db')
    return conn

@app.route("/search")
def search():
    q = request.args.get("q", "")
    # INTENTIONAL_VULN: SQL concatenation (SQL Injection)
    conn = get_db()
    cursor = conn.cursor()
    sql = "SELECT id, title FROM articles WHERE title LIKE '%" + q + "%';"
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    # INTENTIONAL_VULN: using render_template_string with user data (stored XSS risk when content comes from DB)
    html = "<h1>Search results</h1>"
    for r in results:
        html += "<div><strong>{}</strong>: {}</div>".format(r[0], r[1])
    return render_template_string(html)

if __name__ == "__main__":
    # create db for testing (unsafe convenience code)
    conn = sqlite3.connect('test.db')
    conn.execute("CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY, title TEXT);")
    conn.execute("INSERT INTO articles (title) VALUES ('Hello World');")
    conn.commit()
    conn.close()
    app.run(debug=True)

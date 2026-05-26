from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'eafit-en-secret-2025'

DB_CONFIG = {
    'host': '172.31.28.189',
    'user': 'eafit',
    'password': 'eafit2025',
    'database': 'registros',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db():
    return pymysql.connect(**DB_CONFIG)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        comuna = request.form.get('comuna', '')
        carrera = request.form.get('carrera', '')

        if not nombre or not comuna or not carrera:
            return 'Missing fields', 400

        try:
            conn = get_db()
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO registros (nombre, comuna, carrera, servidor) VALUES (%s, %s, %s, %s)",
                    (nombre, int(comuna), carrera, 'server1-en')
                )
                conn.commit()
            conn.close()
            return 'OK', 200
        except Exception as e:
            return str(e), 500

    return render_template('index.html')

@app.route('/health')
def health():
    return {'status': 'ok', 'server': 'server1-en', 'time': datetime.now().isoformat()}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

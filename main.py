from flask import Flask, request, redirect, jsonify
from flask_restful import Api, Resource
import sqlite3
import shortuuid
from flask_cors import CORS  # CORS eklenmiştir

app = Flask(__name__)
CORS(app)  # CORS eklenmiştir
api = Api(app)

# SQLite veritabanına bağlanma
def get_db_connection():
    conn = sqlite3.connect('url_shortener.db')
    conn.row_factory = sqlite3.Row
    return conn

# Veritabanında URL'leri saklamak için bir tablo oluşturma
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_url TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Uygulama başlangıcında veritabanını başlat
init_db()

class UrlShortener(Resource):
    def post(self):
        data = request.get_json()
        original_url = data.get('original_url')

        # Geçersiz URL kontrolü
        if not original_url.startswith(('http://', 'https://')):
            return jsonify({'error': 'Geçersiz URL'}), 400

        # URL'yi kısalt ve veritabanına ekle
        short_url = shortuuid.uuid()[:8]
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO urls (original_url, short_url) VALUES (?, ?)', (original_url, short_url))
        conn.commit()
        conn.close()

        return jsonify({'short_url': f'http://localhost:5000/{short_url}'})

class UrlRedirect(Resource):
    def get(self, short_url):
        # Veritabanında kısaltılmış URL'yi bul
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT original_url FROM urls WHERE short_url=?', (short_url,))
        result = cursor.fetchone()
        conn.close()

        if result:
            original_url = result[0]
            return redirect(original_url, code=302)
        else:
            return jsonify({'error': 'URL bulunamadı'}), 404

api.add_resource(UrlShortener, '/shorten')
api.add_resource(UrlRedirect, '/<string:short_url>')

if __name__ == '__main__':
    app.run(debug=True)
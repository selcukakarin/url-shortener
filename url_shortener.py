from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import shortuuid
from flask_cors import CORS
from functools import wraps
from flask_restx import Api, Resource, fields

app = Flask(__name__)
CORS(app)
api = Api(app, doc='/swagger/')

# Flask-Caching config
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# PostgreSQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Moneytolia123@postgres:5432/url_shortener'
# testler için yukarıdaki satırı comment'leyip aşağıdaki satırı comment out yap
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Moneytolia123@localhost:5432/url_shortener'
db = SQLAlchemy(app)

# model
class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(255), nullable=False)
    short_url = db.Column(db.String(8), nullable=False, unique=True)

# create db
with app.app_context():
    db.create_all()

def cache_by_original_url(f):
    """
    original_url baz alınarak cache için key oluşturma
    """
    @wraps(f)
    def decorated_function(original_url, *args, **kwargs):
        cache_key = f'{original_url}_shorten_url'

        # cache'ten veri kontrolü
        result = cache.get(cache_key)

        # cache'te yoksa yeni short_url oluştur.
        if result is None:
            while True:
                # uuid ile unique short_url oluştur
                short_url = shortuuid.uuid()[:8]

                # yeni oluaşn short_url db'de var mı?
                existing_url = Url.query.filter_by(short_url=short_url).first()

                # db'de yoksa yeni ekle
                if not existing_url:
                    db.session.add(Url(original_url=original_url, short_url=short_url))
                    db.session.commit()
                    result = short_url
                    break

            # cache'e set et
            cache.set(cache_key, result, timeout=300)

        return result

    return decorated_function

# url kısaltma fonksiyonu
@cache_by_original_url
def shorten_url(original_url):
    while True:
        short_url = shortuuid.uuid()[:8]

        existing_url = Url.query.filter_by(short_url=short_url).first()

        if not existing_url:
            db.session.add(Url(original_url=original_url, short_url=short_url))
            db.session.commit()
            return short_url

# index sayfası
@app.route('/')
def index():
    return "URL Shortener API"

# Flask-Restx Namespace oluşturun
ns = api.namespace('shorten', description='URL Shortener Operations')

# Swagger modelini tanımlayın
shorten_model = api.model('Shorten', {
    'original_url': fields.String(required=True, description='The original URL to be shortened.')
})

# Flask-Restx Resource'u oluşturun
class ShortenResource(Resource):
    @api.expect(shorten_model)
    @api.response(200, 'Shortened URL successfully generated.')
    @api.response(400, 'Invalid URL.')
    def post(self):
        """
        Shorten a URL.
        """
        data = api.payload
        original_url = data.get('original_url')

        # url'in geçersiz olup olmadığını kontrol et
        if not original_url.startswith(('http://', 'https://')):
            return {'error': 'Geçersiz URL'}, 400

        short_url = shorten_url(original_url)
        return {'short_url': f'http://localhost:5000/{short_url}'}

api.add_resource(ShortenResource, '/shorten')

class RedirectResource(Resource):
    @api.response(302, 'Redirect to the original URL.')
    @api.response(404, 'URL not found.')
    def get(self, short_url):
        """
        Redirect to the original URL.
        """
        url_entry = Url.query.filter_by(short_url=short_url).first()

        if url_entry:
            return redirect(url_entry.original_url, code=302)
        else:
            return {'error': 'URL bulunamadı'}, 404

api.add_resource(RedirectResource, '/<string:short_url>')

# kısaltılmış url'i get et
@app.route('/<string:short_url>')
def redirect_to_original(short_url):
    """
        API endpoint to redirect to the original URL.
        ---
        parameters:
          - name: short_url
            in: path
            type: string
            required: true
            description: The shortened URL.
        responses:
          302:
            description: Redirect to the original URL.
          404:
            description: URL not found.
        """
    with app.app_context():
        url_entry = Url.query.filter_by(short_url=short_url).first()

        if url_entry:
            return redirect(url_entry.original_url, code=302)
        else:
            return jsonify({'error': 'URL bulunamadı'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
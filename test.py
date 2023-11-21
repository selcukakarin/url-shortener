import unittest
from flask import json
from url_shortener import app, db, Url

class UrlShortenerTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Moneytolia123@postgresql:5432/url_shortener'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_shorten_url(self):
        with app.app_context():
            url_to_shorten = "https://www.moneytolia.com/"
            response = self.app.post('/shorten', json={'original_url': url_to_shorten})
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertIn('short_url', data)

    def test_redirect_to_original(self):
        with app.app_context():
            original_url = "https://www.moneytolia.com/"
            url_entry = Url(original_url=original_url, short_url="abc123")
            db.session.add(url_entry)
            db.session.commit()

            response = self.app.get('/abc123')
            self.assertEqual(response.status_code, 302)
            self.assertIn('Location', response.headers)
            self.assertEqual(response.headers['Location'], original_url)

    def test_shorten_invalid_url(self):
        with app.app_context():
            invalid_url = "not_a_valid_url"
            response = self.app.post('/shorten', json={'original_url': invalid_url})
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data)

    def test_redirect_to_nonexistent_url(self):
        with app.app_context():
            response = self.app.get('/nonexistenturl')
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 404)
            self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()

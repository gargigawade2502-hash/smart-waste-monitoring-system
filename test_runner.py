import unittest
from run import app, db
from app.models import User, Bin, Vehicle, Alert, CollectionRequest

class SystemTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        
    def test_routes(self):
        # Home
        res = self.app.get('/')
        self.assertEqual(res.status_code, 302)
        
        # Login page
        res = self.app.get('/login')
        self.assertEqual(res.status_code, 200)
        
        # Log in as admin
        res = self.app.post('/login', data=dict(username='admin', password='admin123'), follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Dashboard', res.data)
        
        # Check all main routes
        routes = ['/dashboard', '/bins', '/alerts', '/collections', '/vehicles', '/analytics', '/incremental_development', '/about', '/reports']
        for route in routes:
            res = self.app.get(route)
            self.assertEqual(res.status_code, 200)
            
        # Check bin details for B001
        with app.app_context():
            b = Bin.query.first()
            if b:
                res = self.app.get(f'/bin/{b.id}')
                self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()

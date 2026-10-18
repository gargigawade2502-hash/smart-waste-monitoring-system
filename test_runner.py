

import os
import tempfile
import unittest

from werkzeug.security import generate_password_hash
from run import app, db
from app.models import User, Bin


class SystemTests(unittest.TestCase):

    def setUp(self):
        # Create a separate temporary database for testing
        self.db_file = tempfile.NamedTemporaryFile(
            suffix=".db",
            delete=False
        )
        self.db_file.close()

        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            "sqlite:///" + self.db_file.name.replace("\\", "/")
        )

        # Activate Flask application context
        self.ctx = app.app_context()
        self.ctx.push()

        # Initialize test database tables
        db.drop_all()
        db.create_all()

        # Create test administrator
        admin = User(
            username="admin",
            password_hash=generate_password_hash("admin123"),
            role="admin",
            name="Test Admin"
        )

        db.session.add(admin)
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        # Clean up database while the app context is active
        try:
            db.session.remove()
            db.drop_all()
            db.engine.dispose()
        finally:
            self.ctx.pop()

            # Delete temporary database file
            if os.path.exists(self.db_file.name):
                os.remove(self.db_file.name)

    def test_routes(self):
        # Home page should redirect unauthenticated users
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

        # Login page should load
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)

        # Log in using the test administrator
        response = self.client.post(
            "/login",
            data={
                "username": "admin",
                "password": "admin123"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dashboard", response.data)

        # Check application routes
        routes = [
            "/dashboard",
            "/bins",
            "/alerts",
            "/collections",
            "/vehicles",
            "/analytics",
            "/incremental_development",
            "/about",
            "/reports"
        ]

        for route in routes:
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertEqual(
                    response.status_code,
                    200,
                    f"Route failed: {route}"
                )

        # Test individual bin details if a bin exists
        bin_item = db.session.query(Bin).first()

        if bin_item:
            response = self.client.get(f"/bin/{bin_item.id}")
            self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main(verbosity=2)

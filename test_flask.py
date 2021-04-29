from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Clears out database and set up a default user at the beginning of test"""
        Post.query.delete()
        User.query.delete()

        user = User(first_name="Test",
                    last_name="User",
                    image_url="https://coursereport-s3-production.global.ssl.fastly.net/uploads/school/logo/352/original/rslogo.png")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

        post = Post(post_title="Test Post Title 1",
                    post_content="meow meow meow",
                    post_user_id=user.id)
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_redirect(self):
        """Test redirect when user goes to root page"""
        with app.test_client() as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 302)

    def test_list_users(self):
        """Test to see if list users route works"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("For user listing test", html)

    def test_show_new_user_form(self):
        """Test to see if new user form shows up"""
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("For testing user form.", html)

    def test_post_new_user_form(self):
        """Test to see if a user can create a new user"""
        with app.test_client() as client:
            d = {"first-name": "Test", "last-name": "User2", "image-url": ""}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test User2</a></li>", html)

    def test_delete_user(self):
        """Test to see if a user can delete a user"""
        with app.test_client() as client:

            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Test User</a></li>", html)


    def test_show_new_post_form(self):
        """Test to see if new post form shows up"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("For testing post form.", html)

    def test_post_new_post_form(self):
        """Test to see if a user can create a new post"""
        with app.test_client() as client:
            d = {"post-title": "Test Post Title 2", "post-content": "test test test"}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test post form submission", html)
            self.assertIn("Test Post Title 2", html)

    def test_delete_post(self):
        """Test to see if a user can delete a post"""
        with app.test_client() as client:

            resp = client.post(f"/posts/{self.post_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Test Post Title 1", html)

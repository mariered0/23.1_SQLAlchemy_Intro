from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for User."""

    def setUp(self):
        """Clean up any existing users."""

        User.query.delete()
        user = User(first_name="firstname", last_name="lastname")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_users(self):
        """Test /users route."""
        with app.test_client() as client:

            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'{self.user.first_name} {self.user.last_name}', html)

    def test_new_user(self):
        """Test /users/new route."""
        with app.test_client() as client:

            resp = client.post('/users/new', data={'first_name': 'Test', 'last_name': 'Test', 'image_url': 'https://cdn-icons-png.flaticon.com/512/1246/1246351.png?w=826'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Test', html)

    def test_user_page(self):
        """Test /users/user_id route."""
        with app.test_client() as client:

            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h1>{self.user.first_name} {self.user.last_name}</h1>', html)
            # self.assertIn(self.title, html)

    def test_user_delete(self):
        """Test /users/user_id/delete route"""
        with app.test_client() as client:

            resp = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f'{self.user.first_name} {self.user.last_name}', html)

class PostsModelTestCase(TestCase):
    """Tests for model for Posts."""

    def setUp(self):
        """Clean up any existing pets."""

        User.query.delete()
        Post.query.delete()
        user = User(first_name="firstname", last_name="lastname")
        db.session.add(user)
        db.session.commit()


        post = Post(title='test', content='test', user_id=user.id)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.user = user
        self.post = post
        self.title = post.title
        self.content = post.content

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_posts(self):
        """Test post list in the user detail page."""
        with app.test_client() as client:

            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'{self.title}', html)

    def test_new_post(self):
        """Test the route to create a new post."""
        with app.test_client() as client:

            resp = client.post(f'/users/{self.user_id}/posts/new', data={'title': 'New Post', 'content': 'New Content'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('New Post', html)

    def test_post_page(self):
        """Test /users/user_id route."""
        with app.test_client() as client:

            resp = client.get(f'/posts/{self.post.id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h1>{self.title}</h1>', html)
            self.assertIn(f'<p class="mb-3">{self.content}</p>', html)

    def test_post_delete(self):
        """Test /users/user_id/delete route"""
        with app.test_client() as client:

            resp = client.post(f'/posts/{self.post.id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f'{self.post.title}', html)
    

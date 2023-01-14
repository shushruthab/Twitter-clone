"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User, Likes, Follows
from bs4 import BeautifulSoup

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        self.u1 = User.signup("asdasd", "test1@test.com", "password", None)
        self.u1_id = 2050
        self.u1.id = self.u1_id
        self.u2 = User.signup("bhai", "test2@test.com", "password", None)
        self.u2_id = 2056
        self.u2.id = self.u2_id
        self.u3 = User.signup("someone", "test3@test.com", "password", None)
        self.u4 = User.signup("elsef", "test4@test.com", "password", None)

        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_users_index(self):
        with self.client as c:
            resp = c.get("/users")

            self.assertIn("@testuser", str(resp.data))
            self.assertIn("@asdasd", str(resp.data))
            self.assertIn("@bhai", str(resp.data))
            self.assertIn("@someone", str(resp.data))
            self.assertIn("@elsef", str(resp.data))

    def test_user_show(self):
        with self.client as c:
            resp = c.get(f"/users/{self.testuser_id}")

            self.assertEqual(resp.status_code, 200)

            self.assertIn("@testuser", str(resp.data))

    def setup_likes(self):
        m1 = Message(text="asdfsdf dsffd", user_id=self.testuser_id)
        m2 = Message(text="Esfdgfdg sdfsdf", user_id=self.testuser_id)
        m3 = Message(id=5678, text="sdfsreec", user_id=self.u1_id)
        db.session.add_all([m1, m2, m3])
        db.session.commit()

        l1 = Likes(user_id=self.testuser_id, message_id=5678)

        db.session.add(l1)
        db.session.commit()

    def test_add_like(self):
        m = Message(id=5901, text="The round is flat", user_id=self.u1_id)
        db.session.add(m)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.post("/messages/5901/like", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            likes = Likes.query.filter(Likes.message_id==5901).all()
            self.assertEqual(len(likes), 1)
            self.assertEqual(likes[0].user_id, self.testuser_id)

    def setup_followers(self):
        f1 = Follows(user_being_followed_id=self.u1_id, user_following_id=self.testuser_id)
        f2 = Follows(user_being_followed_id=self.u2_id, user_following_id=self.testuser_id)
        f3 = Follows(user_being_followed_id=self.testuser_id, user_following_id=self.u1_id)

        db.session.add_all([f1,f2,f3])
        db.session.commit()


    def test_show_following(self):

        self.setup_followers()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.get(f"/users/{self.testuser_id}/following")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("@asdasd", str(resp.data))
            self.assertIn("@bhai", str(resp.data))
            self.assertNotIn("@someone", str(resp.data))
            self.assertNotIn("@elsef", str(resp.data))


    def test_unauthorized_followers_page_access(self):
        self.setup_followers()
        with self.client as c:

            resp = c.get(f"/users/{self.testuser_id}/followers", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("@asdasd", str(resp.data))
            self.assertIn("Access unauthorized", str(resp.data))

"""Seed file to make sample data for users db."""

from models import User, db, Post
from app import app

# Create all tables
# db.drop_all()
db.create_all()

# If table isn't empty, empty it
# User.query.delete()

# Add users
# marie = User(first_name='Marie', last_name='Hank')
# colt = User(first_name='Colt', last_name='Steele')
# steven = User(first_name='Steven', last_name='Hank', image_url='https://cdn-icons-png.flaticon.com/512/1246/1246314.png?w=826')

# Add new objects to session, so they'll persist
# db.session.add(marie)
# db.session.add(colt)
# db.session.add(steven)

# Commit--otherwise, this never gets saved!
# db.session.commit()

# Add posts
marie_post1 = Post(title='First Post!', content='Oh, hi!', user_id=1)
marie_post2 = Post(title='Second Post!', content='Oh, hi!', user_id=1)
marie_post3 = Post(title='Third Post!', content='Oh, hi!', user_id=1)
colt_post1 = Post(title='First Post!', content='Oh, hi!', user_id=2)
colt_post2 = Post(title='Second Post!', content='Oh, hi!', user_id=2)
colt_post3 = Post(title='Third Post!', content='Oh, hi!', user_id=2)
steven_post1 = Post(title='First Post!', content='Oh, hi!', user_id=3)
steven_post2 = Post(title='Second Post!', content='Oh, hi!', user_id=3)
steven_post3 = Post(title='Third Post!', content='Oh, hi!', user_id=3)

# Add new posts to session.
db.session.add_all([marie_post1, marie_post2, marie_post3, colt_post1, colt_post2, colt_post3, steven_post1, steven_post2, steven_post3])

#Commit
db.session.commit()


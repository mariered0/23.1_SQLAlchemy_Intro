"""Seed file to make sample data for users db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
marie = User(first_name='Marie', last_name='Hank')
colt = User(first_name='Colt', last_name='Steele')
steven = User(first_name='Steven', last_name='Hank', image_url='https://cdn-icons-png.flaticon.com/512/1246/1246314.png?w=826')

# Add new objects to session, so they'll persist
db.session.add(marie)
db.session.add(colt)
db.session.add(steven)

# Commit--otherwise, this never gets saved!
db.session.commit()

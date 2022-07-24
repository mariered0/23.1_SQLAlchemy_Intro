"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def show_home():
    """Redirect to the list."""
    return redirect('/users')


@app.route('/users')
def list_users():
    """List all users."""

    users = User.query.all()
    return render_template('list.html', users=users)


@app.route('/users/new')
def show_create_user_page():
    """Show a page to create user."""
    return render_template('create_user.html')


@app.route('/users/new', methods=['POST'])
def create_user():
    """Get new user data and display the list of users afterwards. """
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about a single user."""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show edit page."""
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def save_user(user_id):
    """Show details about a single user."""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete user and show the user list."""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


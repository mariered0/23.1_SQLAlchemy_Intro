"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post, Tag

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

    return render_template('edit_user.html', user=user)

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

#Posts route

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    """Show a page to create a new post."""

    user = User.query.get(user_id)
    tags = Tag.query.all()

    return render_template('new_post.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def show_new_post(user_id):
    """Handle new posts and show user detail page."""

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tag")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(
    title = request.form['title'],
    content = request.form['content'], user=user, tags=tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post."""

    post = Post.query.get_or_404(post_id)

    return render_template('post_details.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Show a page to edit post."""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def save_post(post_id):
    """handle edit post and save."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist("tag")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete post and show the user details page."""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/tags')
def list_tag():
    """Show list of tags."""

    tags = Tag.query.all()
    return render_template('tag_list.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Show posts with the tag."""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag_details.html', tag=tag)

@app.route('/tags/new')
def show_create_tag_page():
    """Show a page to create a new tag."""

    return render_template('new_tag.html')

@app.route('/tags/new', methods=['POST'])
def create_tag():
    """Create a new tag."""

    new_tag = Tag(name = request.form['tag'])

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_page(tag_id):
    """Show a pege to edit a tag."""
    
    tag = Tag.query.get_or_404(tag_id)

    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    """Update the tag and show the tag detail page."""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['tag']
    
    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Delete tag and show the tag list."""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')






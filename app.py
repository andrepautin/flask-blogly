"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()


@app.route("/")
def redirect_to_users():
    """When user goes to root, redirect them to list of users"""
    return redirect("/users")


@app.route("/users")
def list_users():
    """Lists all users"""
    users = User.query.all()
    return render_template("users_listing.html", users=users)


@app.route("/users/new", methods=["GET", "POST"])
def show_new_user_form():
    """When user goes on page, show new user form. Allows user to create new user."""
    if (request.method == "POST"):
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        image_url = request.form['image-url']

        user = User(first_name=first_name,
                    last_name=last_name,
                    image_url=image_url)
        db.session.add(user)
        db.session.commit()

        return redirect("/users")
    else:
        return render_template("new_user_form.html")


@app.route("/users/<int:user_id>")
def show_user_details(user_id):
    """Shows the user details page"""
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
def edit_user(user_id):
    """If a user goes to page, shows edit user form. Allows user to edit user information"""
    user = User.query.get_or_404(user_id)
    if (request.method == "POST"):
        user.first_name = request.form['first-name']
        user.last_name = request.form['last-name']
        user.image_url = request.form['image-url']
        db.session.commit()
        
        return redirect("/users")
    else:
        return render_template("user_edit.html", user=user)


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """User can delete user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new", methods=["GET", "POST"])
def show_post_form(user_id):
    """Shows form to create new posts"""
    user = User.query.get_or_404(user_id)
    if (request.method == "POST"):
        post_title = request.form['post-title']
        post_content = request.form['post-content']

        post = Post(post_title=post_title,
                    post_content=post_content,
                    post_user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return render_template("post_detail.html", user=user, post=post)
    else:
        return render_template("new_post_form.html", user=user)


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_detail.html", post=post)

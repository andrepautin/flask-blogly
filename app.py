"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag


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
    """When user goes on page, show new user form.
       Allows user to create new user."""
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
        return render_template("user_new_form.html")


@app.route("/users/<int:user_id>")
def show_user_details(user_id):
    """Shows the user details page"""
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
def edit_user(user_id):
    """If a user goes to page, shows edit user form.
       Allows user to edit user information"""
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
def handle_post_form(user_id):
    """Shows form to create new posts and handles submitting a new post"""
    user = User.query.get_or_404(user_id)
    if (request.method == "POST"):
        post_title = request.form['post-title']
        post_content = request.form['post-content']
        tags = Tag.query.all()
        post = Post(post_title=post_title,
                    post_content=post_content)
        user.posts.append(post)
        db.session.commit()
        for tag in tags:
            if tag.name in request.form:
                posttag = PostTag(tag_id=tag.id, post_id=post.id)
                db.session.add(posttag)
        db.session.commit()
        return render_template("post_detail.html", user=user, post=post)
        # redirect after a post to user profile
    else:
        tags = Tag.query.all()
        return render_template("post_new_form.html", user=user, tags=tags)


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Shows post"""
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    return render_template("post_detail.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def handle_post_edit(post_id):
    """Show edit form for post or submit edits"""
    post = Post.query.get_or_404(post_id)
    if (request.method == "POST"):
        post.post_title = request.form['post-title']
        post.post_content = request.form['post-content']
        tags = Tag.query.all()
        for tag in tags:
            if tag.name in request.form:
                posttag = PostTag(tag_id=tag.id, post_id=post_id)
                db.session.add(posttag)
        db.session.commit()
        return redirect(f"/posts/{post_id}")
    else:
        tags = Tag.query.all()
        return render_template("post_edit.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Deletes a post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/users")


@app.route("/tags")
def list_tags():
    """Lists all tags"""
    tags = Tag.query.all()
    return render_template("tag_listing.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def show_tag_details(tag_id):
    """Show details of one tag lists posts that have that tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag_detail.html", tag=tag)


@app.route("/tags/new", methods=["GET", "POST"])
def handle_new_tag_form():
    """Shows tag form and handles adding a new tag"""
    if (request.method == "POST"):
        tag_name = request.form['tag-name']

        tag = Tag(name=tag_name)
        db.session.add(tag)
        db.session.commit()
        return redirect("/tags")
    else:
        return render_template("tag_create.html")


@app.route("/tags/<int:tag_id>/edit", methods=["GET", "POST"])
def handle_tag_edit_form(tag_id):
    """Shows edit form and handles tag edit"""
    tag = Tag.query.get_or_404(tag_id)
    if (request.method == "POST"):
        tag.name = request.form['tag-name']
        db.session.commit()
        return redirect("/tags")
    else:
        return render_template("tag_edit.html", tag=tag)


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Deletes a tag"""
    tag = Tag.query.get_or_404(tag_id)
    PostTag.query.filter_by(tag_id=tag_id).delete()
    db.session.commit()
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")

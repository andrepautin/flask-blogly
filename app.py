"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User


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
    return redirect("/users")


@app.route("/users")
def list_users():
    users = User.query.all()
    return render_template("users-listing.html", users=users)


@app.route("/users/new", methods=["GET", "POST"])
def show_new_user_form():
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
        return render_template("user-form.html")


@app.route("/users/<int:user_id>")
def show_user_details(user_id):
    """Shows the user details page"""
    user = User.query.get_or_404(user_id)
    return render_template("user-detail.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if (request.method == "POST"):
        user.first_name = request.form['first-name']
        user.last_name = request.form['last-name']
        user.image_url = request.form['image-url']
        db.session.commit()
        
        return redirect("/users")
    else:
        return render_template("user-edit.html", user=user)

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

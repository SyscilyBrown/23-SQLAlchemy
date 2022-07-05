"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    """redirect to list of users """
    return redirect("/users")

@app.route('/users')
def all_users():
    """Shows all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods = ["GET"])
def user_new_form():
    """Creae new user"""
    return render_template('/users/new.html')


@app.route('/users/new', methods=["POST"])
def new_users():
    """Form submission for creating new user"""
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'])

    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_users(user_id):
    """Show user info"""
    user = User.query.get_or_404(user_id)
    return render_template('/users/show.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_users(user_id):
    """Edit user """
    user = User.query.get_or_404(user_id)
    return render_template('/users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods = ["POST"])
def update_users(user_id):
    """Update user"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name'],
    user.last_name = request.form['last_name'],
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods = ["POST"])
def delete_users(user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    return redirect('/users')




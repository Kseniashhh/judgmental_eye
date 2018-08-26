"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/register")
def signup_page():
    """ Sign up page """

    return render_template("registration.html")

@app.route("/user_added")
def user_signsUp():
    """ Register new user, ignore existing"""

    email = request.args.get("email") 
    pswd = request.args.get("password")


    user_exists = if_user_exists(email)

    if user_exists == None:
        user_added = add_user(email, pswd)
        user_exists = if_user_exists(email)
        session['user'] = user_exists[0]
        flash("User was successfully Signed Up")
        return redirect("/")
    else:  
        session['user'] = user_exists[0]
        print(session)
        flash("This user is aleady registered and logged in now")
        return redirect("/")



def if_user_exists(email):
    """ Given email address checks if user already exists"""

    QUERY = """
        SELECT user_id, email
        FROM users
        WHERE email = :email
        """

    db_cursor = db.session.execute(QUERY, {'email': email})
    row = db_cursor.fetchone()
    print(row)

    return row




@app.route("/")
def user_logOut():
    """ log out current user """
    print(session)
    if session['user']:
        session.pop('user')
        flash("User is logged out")
        return redirect("/")
    else:
        flash("User is not logged in")
        return redirect("/")









def add_user(email, password):
    """ Given email and password add new user to users table"""

    QUERY = """
        INSERT INTO users (email, password)
        VALUES (:email, :password)
        """

    db_cursor = db.session.execute(QUERY, {'email': email, 
                                        'password': password})

    db.session.commit()



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

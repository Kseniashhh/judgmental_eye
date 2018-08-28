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

######################################################


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


######################################################

@app.route("/movies")
def movie_list():
    """Show list of movies."""

    movies = Movie.query.all()
    return render_template("movie_list.html", movies=movies)


######################################################


@app.route("/movies/<movie_id>")
def movie_details(movie_id):
    """ Show movie details """

    
    movie = Movie.query.get(movie_id)
    

    movies_rating = rating_details(movie.movie_id)

    avg_movie_score = avg_rating_details_by_movie(movie.movie_id)

    return render_template("movie_details.html", movies_rating=movies_rating,movie=movie, average = avg_movie_score)


def rating_details_by_movie(movie_id):
    """ Show all rating for specific movie"""



    QUERY = """
        SELECT score
        FROM ratings
        WHERE movie_id = :movie_id
        """

    db_cursor = db.session.execute(QUERY, {'movie_id': movie_id})

    rows = db_cursor.fetchall()

    return rows

def avg_rating_details_by_movie(movie_id):
    """Average rating for specific movie"""



    QUERY = """
        SELECT AVG(score)
        FROM ratings
        WHERE movie_id = :movie_id
        """

    db_cursor = db.session.execute(QUERY, {'movie_id': movie_id})

    avg = db_cursor.fetchone()

    return avg


######################################################


@app.route("/register")
def signup_page():
    """ Sign up page """

    return render_template("registration.html")

######################################################

@app.route("/user_added")
def user_signsUp():
    """ Register new user, ignore existing"""

    email = request.args.get("email") 
    pswd = request.args.get("password")
    

    user_exists = if_user_exists(email)

    if user_exists == None:
        add_user(email, pswd)
        user_exists = if_user_exists(email)
        session['user'] = user_exists[0]
        flash("User was successfully Signed Up")
        return redirect("/")
    else:  
        flash("This user is aleady registered. Please log in")
        return redirect("/login")




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




def add_user(email, password):
    """ Given email and password add new user to users table"""

    QUERY = """
        INSERT INTO users (email, password)
        VALUES (:email, :password)
        """

    db_cursor = db.session.execute(QUERY, {'email': email, 
                                        'password': password})

    db.session.commit()

###############################################################



@app.route("/login")
def login_page():
    """ Log in page """

    return render_template("login.html")


################################################################


@app.route("/login_user")
def user_login():
    """ Logs user in """

    email = request.args.get("email") 
    pswd = request.args.get("password")

    user_exists = if_user_exists(email)

    if user_exists == None:
        flash("This user is not registered, please sign up")
        return redirect("/register")
    else:  
        session['user'] = user_exists[0]
        flash("This user is successfully logged in")
        return redirect("/login")


###############################################################


@app.route("/logout")
def user_logOut():
    """ log out current user """
    
    if 'user' not in session:
        flash("User is not logged in")
        return redirect("/")
        
    else:
        session.pop('user')
        flash("User is logged out")
        return redirect("/")



################################################################


@app.route("/users/<user_id>")
def user_details(user_id):
    """ Show user details """

    

    QUERY = """
        SELECT user_id, age, zipcode
        FROM users
        WHERE user_id = :user_id
        """

    db_cursor = db.session.execute(QUERY, {'user_id': user_id})

    user_info = db_cursor.fetchone()

    movies_rating = rating_details(user_info[0])

    return render_template("user_details.html", user_info=user_info, movies_rating=movies_rating)

##Another way to right a function above

    # user = User.query.get(user_id)
    # print(user)

    # movies_rating = rating_details(user.user_id)

    # and pass an object and call columns as methods


def rating_details(user_id):
    """ Show all movied rated by this user"""



    QUERY = """
        SELECT movies.title, ratings.score
        FROM ratings
        LEFT JOIN movies ON ratings.movie_id = movies.movie_id
        WHERE ratings.user_id = :user_id
        """

    db_cursor = db.session.execute(QUERY, {'user_id': user_id})

    rows = db_cursor.fetchall()

    return rows



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

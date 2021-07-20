"""Flask app for flask-notes"""


from flask import Flask, render_template, redirect, session
from models import db, connect_db, User
from forms import RegisterUserForm, LoginUserForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'bababooey'

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    ''' Redirects user to register page. '''
    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def register_page():
    ''' Displays regiser user form and handles
        form submission. '''
    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(
            username,
            password,
            email,
            first_name,
            last_name
        )

        db.session.add(user)
        db.session.commit()

        session['user'] = username
        return redirect("/secret")

    else:
        return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    ''' Displays login user form and handles
        form submission '''
    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['user'] = username
            return redirect(f"/users/{username}")
        else:
            form.username.errors = ["Wrong username/password combination"]
    else:
        return render_template("login.html", form=form)
    
@app.route('/users/<username>')
def secret_page(username):
    """If the user is logged in, let them see this page,
    otherwise redirect to login"""
    # breakpoint()
    if "user" not in session:
        # flash("You must be logged in to view!")
        return redirect("/login")
    elif session.get('user') != username:
        return redirect(f"/users/{session['user']}")
        
    user = User.query.get_or_404(username)
    return render_template("user_info.html", user=user)
    
@app.route('/logout')
def logout_user():
    """logs the user out and redirects"""
    session.pop("user", None)
    return redirect("/")
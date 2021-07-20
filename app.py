"""Flask app for Cupcakes"""


from flask import Flask, render_template, redirect
from models import db, connect_db, User
from forms import RegisterUserForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'bababoeey'

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name)

        db.session.add(user)
        db.session.commit()
        return redirect("/secret")

    else:
        return render_template("register.html", form=form)
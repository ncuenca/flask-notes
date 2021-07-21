"""Flask app for flask-notes"""


from flask import Flask, render_template, redirect, session
from models import db, connect_db, User, Note
from forms import RegisterUserForm, LoginUserForm, NoteForm

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

############## USER ROUTES ##################
@app.route('/register', methods=['GET','POST'])
def register_page():
    ''' Displays regiser user form and handles
        form submission. '''

    if "user" in session:
        return redirect(f"/users/{session['user']}")

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
        return redirect(f"/users/{username}")

    else:
        return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    ''' Displays login user form and handles
        form submission '''

    if "user" in session:
        return redirect(f"/users/{session['user']}")

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
            return render_template("login.html", form=form)
    else:
        return render_template("login.html", form=form)
    
@app.route('/users/<username>')
def secret_page(username):
    """If the user is logged in, let them see this page,
    otherwise redirect to login"""
    if "user" not in session:
        return redirect("/login")
    elif session['user'] != username:
        return redirect(f"/users/{session['user']}")
        
    user = User.query.get_or_404(username)
    return render_template("user_info.html", user=user)

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    ''' Delete user and all of user's notes from database. '''
    if "user" not in session:
        return redirect("/login")
    elif session.get('user') != username:
        return redirect(f"/users/{session['user']}")

    user = User.query.get_or_404(username)

    for note in user.notes:
        db.session.delete(note)
    db.session.delete(user)
    db.session.commit()

    session.pop("user", None)

    return redirect('/')
    
@app.route('/logout', methods=['POST'])
def logout_user():
    """logs the user out and redirects"""
    session.pop("user", None)
    return redirect("/")



############## USER-NOTES ROUTES ##################

@app.route('/users/<username>/notes/add', methods=['GET','POST'])
def add_note(username):
    ''' Displays add note form and handles
        form submission '''

    if "user" not in session:
        # flash("You must be logged in to view!")
        return redirect("/login")
    elif session.get('user') != username:
        return redirect(f"/users/{session['user']}")

    form = NoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(title=title, content=content, owner=username)

        db.session.add(note)
        db.session.commit()
        
        return redirect(f'/users/{username}')
        
    else:
        return render_template("add_note.html", form=form)
        
        
############## NOTES ROUTES ##################

@app.route('/notes/<int:note_id>/update', methods=['GET','POST'])
def update_note(note_id):
    """Display a form to edit a note on GET
    Update a note and redirect to /users/<username> on POST
    """
    note = Note.query.get_or_404(note_id)
    
    if "user" not in session:
        return redirect("/login")
    elif session.get('user') != note.owner:
        return redirect(f"/users/{session['user']}")

    form = NoteForm(title=note.title, content=note.content)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note.title = title
        note.content = content

        db.session.commit()
        
        return redirect(f'/users/{session["user"]}')
        
    else:
        return render_template("edit_note.html", form=form)
        
@app.route('/notes/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):

    note = Note.query.get_or_404(note_id)
    
    if "user" not in session:
        return redirect("/login")
    elif session.get('user') != note.owner:
        return redirect(f"/users/{session['user']}")
    
    db.session.delete(note)
    db.session.commit()
    return redirect(f"/users/{session['user']}")
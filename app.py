"""Flask app for Cupcakes"""


from flask import Flask, render_template, redirect
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def register_page():
    
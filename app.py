from flask import Flask,render_template,url_for,request, redirect,session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import bcrypt
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

# loading env and secret key
load_dotenv()
app.secret_key =os.getenv('SECRET')

db = SQLAlchemy(app)

# user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80))

    def __init__(self,name,email,password) -> None:
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_pw(self,password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def __repr__(self):
        return '<User %r>' % self.name
           

@app.route('/notfound')
def notfound():
    return render_template('notfound.html')


# home /dashboard route
@app.route('/')
def index():
    if 'email' in session and session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('index.html',user=user)
    return redirect('/login')


#login route
@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_pw(password):
            session['email'] = email
            return redirect('/')
        else:
            return redirect('/notfound')

    return render_template('login.html')


#register route

@app.route('/register',methods=["POST","GET"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        new_user=User(name=name,email=email,password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        except:
            return "There was a problem adding your task"
    return render_template('register.html')

# logout route

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)
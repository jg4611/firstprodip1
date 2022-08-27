from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create first instance
app = Flask(__name__)

# create a secret key
app.config['SECRET_KEY'] = 'mysupersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_BINDS'] = {'hobbies': 'sqlite:///hobbies.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

# initialise the db
db = SQLAlchemy(app)

# create Users model


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # create a string

    def __repr__(self):
        return '<Name %r>' % self.name

# create Hobby model


class Hobby(db.Model):
    __bind_key__ = 'hobbies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    hobby = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # create a string

    def __repr__(self):
        return '<Name %r>' % self.name

# create a form class


class NamerForm(FlaskForm):
    name = StringField("What's your name: ", validators=[DataRequired()])
    email = StringField("What's your email: ", validators=[DataRequired()])
    address = StringField("What's your address: ", validators=[DataRequired()])
    submit = SubmitField("submit")

# create another form class


class HobbyForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[DataRequired()])
    hobby = StringField("Hobby: ", validators=[DataRequired()])
    submit = SubmitField("submit")

# create user form


class UserForm(FlaskForm):
    name = StringField("Name ", validators=[DataRequired()])
    email = StringField("Email ", validators=[DataRequired()])
    submit = SubmitField("submit")


# create add_user route and function
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash('User added successfully')
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)

# create add_hobby route and function


@app.route('/hobby/add', methods=['GET', 'POST'])
def add_hobby():
    name = None
    email = None
    hobby = None
    form = HobbyForm()
    if form.validate_on_submit():
        hobby = Hobby.query.filter_by(name=form.name.data).first()
        if hobby is None:
            hobby = Hobby(name=form.name.data,
                          email=form.email.data, hobby=form.hobby.data)
            db.session.add(hobby)
            db.session.commit()
        name = form.name.data
        email = form.email.data
        hobby = form.hobby.data
        form.name.data = ''
        form.email.data = ''
        form.hobby.data = ''
        flash('Hobby added successfully')
    hobby_lists = Hobby.query.order_by(Hobby.date_added)
    return render_template("add_hobby.html", form=form, name=name, email=email, hobby=hobby, hobby_lists=hobby_lists)

# define another form route


@app.route('/hobby', methods=['GET', 'POST'])
def hobby():
    name = None
    email = None
    hobby = None
    form = HobbyForm()
    # validate form
    if form.validate_on_submit():
        flash('Congrats! You are now added to our database.')
        name = form.name.data
        email = form.email.data
        hobby = hobby.form.data
        form.name.data = ''
        form.email.data = ''
        hobby.form.data = ''
    return render_template("hobby.html", name=name, email=email, hobby=hobby, form=form)


# define form route
@app.route('/details', methods=['GET', 'POST'])
def details():
    name = None
    email = None
    address=None
    form = NamerForm()
    # validate form
    if form.validate_on_submit():
        flash('Congrats! Your basic details are now added to our database.')
        name = form.name.data
        email = form.email.data
        address = form.address.data
        form.name.data = ''
        form.email.data = ''
        form.address.data=''
    return render_template("details.html", form=form, name=name, email=email, address=address)


# create decorator/index
@app.route('/')
def index():
    flash('Welcome buddy!')
    return render_template("index.html")


@app.route('/user/<name>')
def user(name):
    msg = "Don't worry. We are going to have a <strong>gala </strong>time."
    choc_no = [4, 3, 6, 5, 7, 9, 8]
    return render_template("user.html", user_name=name, msg=msg, choc_no=choc_no)


# invalid url error
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# internal server error


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


# autoupdate
if __name__ == '__main__':
    app.run(debug=True)

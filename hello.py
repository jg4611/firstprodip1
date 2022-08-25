from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

#create first instance
app=Flask(__name__)

#create a secret key
app.config['SECRET_KEY']='mysupersecretkey'

#create a form class
class NamerForm(FlaskForm):
  name=StringField("What's your name",validators=[DataRequired()])
  submit=SubmitField("submit")
  
#define form route
@app.route('/name', methods=['GET','POST'])
def name():
  name=None
  form=NamerForm()
  #validate form
  if form.validate_on_submit():
    name=form.name.data
    #form.name.data=''
  return render_template("name.html",name=name,form=form)  
  

#create decorator/index
@app.route('/')
def index():
  return render_template ("index.html")

@app.route('/user/<name>')
def user(name):
  msg="Don't worry. We are going to have a <strong>gala </strong>time."
  choc_no=[4,3,6,5,7,9,8]
  return render_template("user.html",user_name=name,msg=msg,choc_no=choc_no)

#invalid url error
@app.errorhandler(404)
def page_not_found(e):
  return render_template("404.html"),404

#internal server error
@app.errorhandler(500)
def page_not_found(e):
  return render_template("500.html"),500

#autoupdate
if __name__ == '__main__':
    app.run(debug=True)
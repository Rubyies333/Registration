
from flask import Flask, render_template, flash,redirect
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField,SubmitField
from wtforms .validators import DataRequired, Email, Regexp,Length
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app=Flask(__name__)
app.config['SECRET_KEY']="key"
app.config['SQLALCHEMY_DATABASE_URI']="postgresql+psycopg2://neondb_owner:npg_R3lNdWM4XvCf@ep-hidden-meadow-apm0117s.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
db=SQLAlchemy(app)

class Registration(FlaskForm):
    name=StringField("Name", validators=[DataRequired()])
    mobile=TelField("Mobile", validators=[DataRequired(),Length(min=11,max=11, message="Phone number must contain 11 digits starting with 0."),Regexp(r"^0\d{10}$",message="Must contain 11 digits starting with a 0.")])
    email=EmailField("Email", validators=[DataRequired(), Email()])
    address=StringField("Address", validators=[DataRequired()])
    city=StringField("Town/City",validators=[DataRequired()])
    postcode=StringField("Postcode",validators=[DataRequired()])

    button=SubmitField("Register")

class Register(db.Model):
    __tablename__="People_registered"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(50))
    mobile=db.Column(db.String(11))
    email=db.Column(db.String(100))
    address=db.Column(db.String(100))
    city=db.Column(db.String(50))
    postcode=db.Column(db.String(10))
    

@app.route("/",methods=['POST','GET'])
def home():
    reg=Registration()
    if reg.validate_on_submit():
        name=reg.name.data
        mobile=reg.mobile.data
        email=reg.email.data 
        address=reg.address.data
        city=reg.city.data
        postcode=reg.postcode.data
        person=Register(name=name,mobile=mobile,email=email,address=address,city=city,postcode=postcode )
        
        db.session.add(person)
        db.session.commit()
        flash("Sucessfully registered!")
        return redirect("/")

    return render_template("hello.html", form=reg)

#@app.route("/register_person",methods=['POST'])
#def register_person():
    #reg=Registration()
    

if __name__=='__main__':
    with app.app_context():
        db.create_all() 

    app.run(debug=True)
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_account.sqlite3'
app.secret_key = 'kashyapabhishek22dhgxbn'

db = SQLAlchemy(app)


class StudentAccount(db.Model):
    id = db.Column('student', db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    gender = db.Column(db.String(6))
    country = db.Column(db.String(50))
    email = db.Column(db.String(30))
    create_password = db.Column(db.String(20))
    confirm_password = db.Column(db.String(20))

    def __init__(self, first_name, last_name, gender, country, email, create_password, confirm_password):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.country = country
        self.email = email
        self.create_password = create_password
        self.confirm_password = confirm_password


db.create_all()


student = StudentAccount('first_name', 'last_name', 'gender', ' country', 'email@gmail.com', 'create_password', 'confirm_password')
db.session.add(student)
db.session.commit()


@app.route('/')
def homepage():
    print(StudentAccount.query.filter_by(email='something@gmail.com').first().first_name)
    return "done"


if __name__ == "__main__":
    app.run(debug=True)
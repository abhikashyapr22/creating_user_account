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


@app.route('/')
def homepage():
    return render_template("homepage.html")


@app.route('/create_account', methods=['POST', 'GET'])
def create_account():
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        gender = request.form['gender']
        country = request.form['country']
        email = request.form['email']
        create_password = request.form['psw1']
        confirm_password = request.form['psw2']

        try:
            request.form['privacy']
        except:
            flash("Please accept privacy policy!")
            return redirect(url_for('homepage'))

        if StudentAccount.query.filter_by(email='email@gmail.com').first():
            flash("User already exists! Try some different email")
            return redirect(url_for('homepage'))

        elif create_password != confirm_password:
            flash("Passwords do not match! Please try again!")
            return redirect(url_for('homepage'))

        else:
            try:
                student = StudentAccount(first_name, last_name, gender, country, email, create_password, confirm_password)
                db.session.add(student)
                db.session.commit()
                print(StudentAccount.query.all())
            except Exception as e:
                flash(f'{e}')
                return redirect(url_for('homepage'))

            db.close()
            return render_template("data_received.html", data=first_name)
    else:
        return redirect(url_for('homepage'))


if __name__ == "__main__":
    app.run(debug=True)

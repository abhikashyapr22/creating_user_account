from flask import Flask, render_template, request
import mysql.connector as connection

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    return render_template("homepage.html")


@app.route('/create_account', methods=['POST'])
def create_account():
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
        return render_template('homepage.html', data='Please accept privacy policy! ')

    try:
        mydb = connection.connect(host='localhost', user='root', passwd='Abhishek@1067', database='mysql_python')
        cursor = mydb.cursor()
    except Exception as e:
        return e

    try:
        cursor.execute(f"SELECT count(*) FROM user_accounts where Email = '{email}' limit 1")
    except:
        return render_template('homepage.html', data='Please check your connection')

    if cursor.fetchall()[0][0]:
        return render_template('homepage.html', data='User already exists! Try some different user name')

    elif create_password != confirm_password:
        return render_template('homepage.html', data='Passwords do not match! Please try again')

    else:
        sql = "INSERT INTO user_accounts " \
              "(First_Name, Last_Name, Gender, Country, Email, Create_password, Confirm_password) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s)"

        values = (first_name, last_name, gender, country, email, create_password, confirm_password)
        try:
            cursor.execute(sql, values)
            mydb.commit()
        except Exception as e:
            return e

        mydb.close()
        return render_template("data_received.html", data=first_name)


if __name__ == "__main__":
    app.run(debug=True)

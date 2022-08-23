from flask import Flask, render_template, request
import pymongo

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
        client = pymongo.MongoClient(
            "mongodb://root:root@cluster0-shard-00-00.juny6.mongodb.net:27017,"
            "cluster0-shard-00-01.juny6.mongodb.net:27017,"
            "cluster0-shard-00-02.juny6.mongodb.net:27017/?ssl=true&replicaSet=atlas-av6fij-shard-0&authSource=admin"
            "&retryWrites=true&w=majority")
    except:
        return render_template('homepage.html', data='Unable to connect to database! ')

    database = client['user_database']
    collection = database['user_accounts']

    data = {
        'First Name': first_name,
        'Last Name': last_name,
        'Gender': gender,
        'Country': country,
        'Email': email,
        'Create Password': create_password,
        'Confirm Password': confirm_password
    }

    try:
        query = {"Email": email}
        x = collection.find_one(query)
    except:
        return render_template('homepage.html', data='Please check your connection')

    if x:
        return render_template('homepage.html', data='User already exists! Try some different user name')

    elif create_password != confirm_password:
        return render_template('homepage.html', data='Passwords do not match! Please try again')

    else:
        try:
            collection.insert_one(data)
            return render_template("data_received.html", data=first_name)
        except Exception as e:
            return str(e)


if __name__ == "__main__":
    app.run(debug=True)

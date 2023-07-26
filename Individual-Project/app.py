from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask import session as login_session
import pyrebase
import requests

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
config = {
  'apiKey': "AIzaSyDDpiKeJxo3YLGV3CzQT2X-KYe8NWhjS5c",
  'authDomain': "crunch-23428.firebaseapp.com",
  'databaseURL': "https://crunch-23428-default-rtdb.europe-west1.firebasedatabase.app",
  'projectId': "crunch-23428",
  'storageBucket': "crunch-23428.appspot.com",
  'messagingSenderId': "240183649113",
  'appId': "1:240183649113:web:002c3fd716809e8dd4a248",
  'measurementId': "G-RMKWGRZKGK"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/')
def start():
   return render_template('index.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form["Email"]
        password = request.form["Password"]
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            login_session['user'] = user
            return redirect(url_for('home'))
        except:   
            error = "Failed to login. Please check your email and password."
            return redirect(url_for('signin'))
    return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        username = request.form['username']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {'email': email, 'password': password, 'name': full_name, 'username': username}
            db.child('Users').child(UID).set(user)
            return redirect(url_for('home'))
        except:
            error = "failed to signup"
    return render_template("signup.html")

def fetch_random_dad_joke():
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()  # Extract the JSON data
            joke = data["joke"]     # Get the joke from the JSON data
            return joke
        else:
            return "Failed to fetch a dad joke. Please try again later."
    except requests.exceptions.RequestException as e:
        return "An error occurred: " + str(e)


@app.route('/get_random_dad_joke')
def get_random_dad_joke():
    joke = fetch_random_dad_joke()
    return jsonify({"joke": joke})

@app.route('/home', methods=['POST', 'GET'])
def home():
    joke_response = fetch_random_dad_joke()
    joke = joke_response
    user = login_session['user']
    UID = user['localId']


    return render_template("home.html", joke = joke)

@app.route('/users_jokes')
def jokeses():
    joke_response = fetch_random_dad_joke()
    joke = joke_response
    users_jokes = {'joke': joke}
    return render_template('your_jokes.html', jokess = users_jokes)
#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)
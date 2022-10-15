from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def home():
    return render_template('landing.html')


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/logout")
def logout():
    return render_template('landing.html')


# add a user to the db
@app.route("/addUser", methods=['POST'])
def addUser():
    return render_template('home.html')


if __name__ == '__name__':
    app.run(debug=True, port=5000)
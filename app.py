from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

user_id = ""


# users model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.id


@app.route("/")
def home():
    if user_id == "":
        return render_template('landing.html')
    else:
        user = Users.query.get(user_id)
        return render_template('userHP.html', user=user)


@app.route("/login")
def login():
    print(user_id, "Login route user_id")
    return render_template('login.html')


@app.route("/loginUser", methods=['POST', 'GET'])
def loginUser():
    user_email = request.form['email']
    user_password = request.form['password']
    user = Users.query.filter_by(email=user_email).first()
    user_id = user.id

    try:
        if user.password == user_password:
            print(user_id, "/loginUser route")
            return render_template('userHP.html', user=user)
        else:
            return "Passwords do not match!!"
    except:
        return redirect("/")


# Update User
# @app.route("/update/<int:_id>", methods=['POST', 'GET'])
# def update(_id):
#     user_to_update = Users.query.get_or_404(_id)
#     return "User logged in"

@app.route("/logout")
def logout():
    return render_template('landing.html')


@app.route("/createUser")
def createUser():
    return render_template('createUser.html')


# add a user to the db
@app.route("/addUser", methods=['POST', 'GET'])
def addUser():
    if request.method == "POST":
        user_name = request.form['name']
        user_email = request.form['email']
        user_password = request.form['password']
        user = Users(name=user_name, email=user_email, password=user_password)

        # add to db
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/addUser')
        except:
            return "There was an error adding the user!"
    else:
        allUsers = Users.query.order_by(Users.created_at)
        return render_template('userHP.html', users=allUsers)


if __name__ == '__name__':
    app.run(debug=True, port=5000)

import os

from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']

        if not first_name:
            flash('First name is required!')
        elif not last_name:
            flash('Last name is required!')
        elif not email:
            flash('Email is required!')
        elif not phone_number:
            flash('Phone number is required!')
        else:
            new_user = User(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfully!')
            return redirect(url_for('index'))

    return render_template('add_user.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
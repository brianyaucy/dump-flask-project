from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from io import BytesIO
from .sec_modules.email_checking import isEmailValid
from .sec_modules.password_checking import password_complexity
import os, base64, onetimepass, pyqrcode

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        otp_secret = base64.b32encode(os.urandom(15)).decode('utf-8')

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash('Error occurs! Error Code: 1', category='error')
            print('Error - 1 - Email has already been registered!')
        elif username_exists:
            flash('Error occurs! Error Code: 2', category='error')
            print('Error - 2 - The username has been taken')
        elif password != password2:
            flash("Password doesn't match!", category='error')
            print("Error - User passwords do not match")
        elif not password_complexity(password):
            flash("Password complexity fails!", category='error')
            print("Error - Password complexity fails")
        elif not isEmailValid(email):
            flash("Invalid email!", category='error')
            print("Error - Invalid email provided")
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'), otp_secret=otp_secret)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("User created!")
            return redirect(url_for("auth.two_factor_setup", username=username))
    return render_template("register.html", user=current_user)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        otp = request.form.get('otp')
        user = User.query.filter_by(email=email).first()
        if user:
            if (    check_password_hash(user.password, password)
                and onetimepass.valid_totp(otp, user.otp_secret)
               ):
                flash("Login successful!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Login Error!", category='error')
        else:
            flash("Login Error!", category='error')
    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out!", category="success")
    return redirect(url_for("views.home"))

@auth.route("/two_factor_setup")
@login_required
def two_factor_setup():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    otp_secret = user.otp_secret
    logout_user()
    totp_uri = f'otpauth://totp/DamnDumpSite:{username}?secret={otp_secret}&issuer=DamnDumpSite'
    qrcode = pyqrcode.create(totp_uri)
    stream = BytesIO()
    qrcode.svg(stream, scale=5)
    qr = stream.getvalue().decode('utf-8')
    return render_template('two-factor-setup.html', user=current_user, qr=qr, otp_secret=otp_secret), 200, {
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }

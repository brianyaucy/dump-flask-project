from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from . import db
from OTXv2 import OTXv2
import base64 as b64

security = Blueprint("security", __name__)

@security.route("/base64", methods=['GET', 'POST'])
@login_required
def base64():
    if request.method == "POST":
        r_method = request.form.get("submit_button")
        text_input = request.form.get('text')
        if r_method == "encode":
            final_result = b64.b64encode(text_input.encode('utf-8')).decode()
        else:
            final_result = b64.b64decode(text_input.encode('utf-8')).decode()
    else:
        final_result = ""
    return render_template("base64.html", user=current_user, result=final_result)

# @security.route("/ip-checker")
# @login_required
# def ip_checker():
#     otx = OTXv2(API_KEY, server=OTX_SERVER)
from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from . import db
from .sec_modules.timeline_checking import date_check, time_check

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

@views.route("/profile")
def profile():
    return "profile"

@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get("text")
        if not text:
            flash("Post content cannot be EMPTY!", category="error")
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post has been saved successfully!", category="success")
            return redirect(url_for("views.home"))
    return render_template("create_post.html", user=current_user)

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post doesn't exist", category="error")
    elif current_user.id != post.author:
        flash("You're not authorized to delete this post!", category="error")
    elif current_user.id == post.author:
        db.session.delete(post)
        db.session.commit()
        flash(f"The post (id: {post.id}) has been deleted.", category="success")
    else:
        flash("Something went wrong.", category="error")
    return redirect(url_for("views.home"))

@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("No such user!", category="error")
        return redirect(url_for("views.home"))
    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)

@views.route("/create-comment/<post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    comment = request.form.get("text")
    if not comment:
        flash("Empty input!", category="error")
    else:
        post = Post.query.filter_by(id=post_id)
        if not post:
            flash(f"This post (id={post_id}) doesn't exist!", category="error")
        else:
            comment = Comment(text=comment, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash("Comment successfully posted!", category="success")
    return redirect(url_for("views.home"))

@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash(f"Comment ID {comment_id} does't exist!", category="error")
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash("Don't hack!", category="error")
    elif current_user.id == comment.author or current_user.id == comment.post.author:
        db.session.delete(comment)
        db.session.commit()
        flash(f"Comment ID {comment_id} has been successfully removed.", category="success")
    else:
        flash("Unknown error!", category="error")
    return redirect(url_for("views.home"))

@views.route("/like-post/<post_id>")
@login_required
def like_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()
    if not post:
        flash(f"Post ID {post_id} does't exist!", category="error")
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    return redirect(url_for("views.home"))

@views.route("/timeline", methods=['GET', 'POST'])
@login_required
def timeline():
    if request.method == "POST":
        input_text = request.form.get("text")
        tz = request.form.get("timezone")
        print(tz)
        events_list = input_text.split("\n")
        events_list = list(filter(None, events_list))
        dict_events_list = []
        for event in events_list:
            tmp = event.split("|")
            keys = [ "date", "time", "host", "actor", "victim", "title", "desc" ]
            tmp_dict = {}
            for i in range(len(keys)):
                try:
                    tmp_dict[keys[i]] = tmp[i].strip()
                except IndexError:
                    tmp_dict[keys[i]] = "N/A"
                except:
                    tmp_dict[keys[i]] ="Unknown"
            if not date_check(tmp_dict["date"]):
                flash("Date Format Error - Should be in YYYY-mm-dd format", category="error")
                error_flag = 1
            elif not time_check(tmp_dict["time"]):
                flash("Time Format Error - Should be in hh:mm:ss format", category="error")
                error_flag = 1
            else:
                error_flag = 0
            if error_flag == 1:
                return render_template("timeline.html", user=current_user, input_text=input_text)
            tmp_dict["timezone"] = tz
            dict_events_list.append(tmp_dict)
        dates = list(set([ obj["date"] for obj in dict_events_list ]))
        dates.sort(reverse=True)
        timeline_items = []
        for date in dates:
            tmp_list = [ event for event in dict_events_list if event["date"] == date ]
            trim_tmp_list = [ { k:v for k,v in sub.items() if k != "date" } for sub in tmp_list ]
            trim_tmp_list = sorted(trim_tmp_list, key=lambda k:k['time'], reverse=True)
            timeline_items.append({ date: trim_tmp_list })
            print(timeline_items)
        return render_template("timeline.html", user=current_user, input_text=input_text, timeline_items=timeline_items)
    return render_template("timeline.html", user=current_user)
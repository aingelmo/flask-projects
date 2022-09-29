from flask import Blueprint, flash, redirect, render_template, url_for
from flask_dance.consumer import oauth_authorized
from flask_login import current_user, login_user, logout_user
from sqlalchemy.orm.exc import NoResultFound

from website.forms import LoginForm, RegistrationForm
from website.google import bp as blueprint
from website.models import OAuth, User, db
from website.views import get_top_menu_items

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        flash("Already registered.", category="warning")
        return redirect(url_for("views.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("views.index"))

    return render_template(
        "auth/register.html", form=form, top_menu_items=get_top_menu_items("/")
    )


@bp.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        flash("Already logged in.", category="warning")
        return redirect(url_for("views.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            error = "Invalid username or password"

        login_user(user, remember=form.remember_me.data)

    return render_template(
        "auth/login.html", form=form, top_menu_items=get_top_menu_items("/")
    )


@bp.route("logout")
def logout():
    logout_user()
    flash("Logged out successfully!", category="success")
    return redirect(url_for("views.index"))


@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in.", category="error")
        return False

    resp = blueprint.session.get("/oauth2/v2/userinfo")
    if not resp.ok:
        flash("Failed to fetch user info.", category="error")
        return False

    user_info = resp.json()
    user_id = user_info["id"]

    query = OAuth.query.filter_by(provider=blueprint.name, provider_user_id=user_id)
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, provider_user_id=user_id, token=token)

    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in.")
    else:
        user = User(email=user_info["email"], username=user_info["name"])
        oauth.user = user
        db.session.add_all([user, oauth])
        db.session.commit()
        login_user(user)
        flash("Successfully signed in.")

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False

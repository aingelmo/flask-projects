import settings
from flask_dance.contrib.google import make_google_blueprint

bp = make_google_blueprint(
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    scope=[
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ],
    offline=True,
    reprompt_consent=True,
)

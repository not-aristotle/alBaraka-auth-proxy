from datetime import datetime

from rproxy.ext import db


class UserSession(db.Model):
    __tablename__ = "user_session"
    __table_args__ = (
        db.UniqueConstraint(
            "access_token",
            "refresh_token",
            name="user_session_access_token_refresh_token_key",
        ),
    )

    user_session_id = db.Column(db.Integer, primary_key=True)
    user_token = db.Column(db.String(128), unique=True, nullable=False)
    access_token = db.Column(db.String(128), nullable=False)
    refresh_token = db.Column(db.String(128), nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
    activated = db.Column(db.DateTime, nullable=False)

    def __init__(
        self,
        user_token: "str",
        access_token: "str",
        refresh_token: "str",
        expires: "datetime",
        activated: "datetime",
    ):
        self.user_token = user_token
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires = expires
        self.activated = activated

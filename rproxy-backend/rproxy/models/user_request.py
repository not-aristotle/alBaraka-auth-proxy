from rproxy.ext import db


class UserRequest(db.Model):
    __tablename__ = "user_request"

    user_request_id = db.Column(db.Integer, primary_key=True)
    api_method = db.Column(db.String(32), nullable=False)
    api_endpoint = db.Column(db.String(1024), nullable=False)
    request_body = db.Column(db.String, nullable=False)
    response_status = db.Column(db.Integer, nullable=False)
    response_body = db.Column(db.String, nullable=False)

    def __init__(
        self,
        api_method: "str",
        api_endpoint: "str",
        request_body: "str",
        response_status: "int",
        response_body: "str",
    ):
        self.api_method = api_method
        self.api_endpoint = api_endpoint
        self.request_body = request_body
        self.response_status = response_status
        self.response_body = response_body

from base64 import b64encode
from datetime import datetime

from flask import request, jsonify, current_app
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import requests
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

from rproxy.api.v1.proxy.blueprint import bp
from rproxy.ext import db
from rproxy.models import UserSession, UserRequest


@bp.route("/<path:api_endpoint>", methods=("POST",))
def proxy(api_endpoint: "str"):
    try:
        api_endpoint_prefix, api_endpoint_body = api_endpoint.split(
            "/", maxsplit=1
        )
    except ValueError:
        api_endpoint_prefix, api_endpoint_body = api_endpoint, ""
    try:
        user = (
            db.session.query(UserSession.access_token)
            .filter(
                UserSession.user_token == request.headers["Token"],
                UserSession.activated
                > datetime.utcnow() - current_app.config["USER_TOKEN_TTL"],
            )
            .one()
        )
    except (KeyError, NoResultFound, MultipleResultsFound):
        return (
            jsonify(
                {"success": False, "messages": {"_schema": ["Invalid Token"]}}
            ),
            200,
        )

    api_endpoint = "{}/{}/{}".format(
        current_app.config["API_ENDPOINT"],
        api_endpoint_prefix,
        api_endpoint_body,
    )
    headers = {
        "Authorization": "Bearer {}".format(user.access_token),
    }
    if "Content-Type" in request.headers:
        headers["Content-Type"] = request.headers["Content-Type"]
    data = request.get_data() or None
    if api_endpoint_prefix in {
        "accounts",
        "moneytransfers",
        "loans",
        "creditcards",
        "investments",
    }:
        message = user.access_token.encode()
        if data:
            message += data
        h = SHA256.new(message)
        signer = PKCS1_v1_5.new(current_app.config["PRIVATE_KEY"])
        headers["sign"] = b64encode(signer.sign(h)).decode()
    response = requests.request(
        request.method,
        api_endpoint,
        headers=headers,
        data=data,
        timeout=current_app.config["API_TIMEOUT"],
    )
    db.session.add(
        UserRequest(
            request.method,
            api_endpoint,
            data.decode() if data else "",
            response.status_code,
            response.text,
        )
    )
    db.session.commit()
    return (
        response.text,
        response.status_code,
        {"Content-Type": response.headers["Content-Type"]},
    )

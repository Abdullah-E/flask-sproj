"""API Management"""

import logging
import os
import firebase_admin
from core.api.api_handyman import handyman
from flask import Flask, request
from core.api import utils


"""
    --- --- --- --- --- --- --- --- --- --- --- ---
    Flask app setup
    --- --- --- --- --- --- --- --- --- --- --- ---
"""

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True

app.register_blueprint(handyman)

cred = firebase_admin.credentials.Certificate(
    "./core/api/firebase-credentials.json")
# cred = firebase_admin.credentials.Certificate(
#     "./core/api/firebase-credentials.json")
firebase_admin.initialize_app(cred)

# 200 OK
# The request succeeded. The result meaning of "success" depends on the HTTP method:

# 201 Created
# The request succeeded, and a new resource was created as a result.
# This is typically the response sent after POST requests, or some PUT requests.

# 400 Bad Request
# The server cannot or will not process the request due to something
# that is perceived to be a client error (e.g., malformed request syntax,
# invalid request message framing, or deceptive request routing).

# 401 Unauthorized
# Although the HTTP standard specifies "unauthorized", semantically this response means
# "unauthenticated". That is, the client must authenticate itself to get the requested response.

# 404 Not Found
# The server cannot find the requested resource. In the browser, this means the URL is
# not recognized. In an API, this can also mean that the endpoint is valid but the resource
# itself does not exist. Servers may also send this response instead of 403 Forbidden to hide
# the existence of a resource from an unauthorized client. This response code is probably the most
# well known due to its frequent occurrence on the web.

# 500 Internal Server Error
# The server has encountered a situation it does not know how to handle.

PREFIX = "/api/v1"


@app.route(PREFIX)
def base():
    """base endpoint"""

    return utils.Response(message="Welcome to the backend", status_code=200).__dict__


@app.errorhandler(utils.CustomException)
def handle_exceptions(e: utils.CustomException):
    payload = {
        "message": e.message,
        "event_code": e.event_code.name,
    }

    return payload, e.status_code

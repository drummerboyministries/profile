import base64, json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from flask import redirect, session, url_for, request

from .app import app
from . import model

oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


@app.route("/")
def home():
    return redirect("/self")


@app.route("/self")
def self():
    if session and session.get("user"):
        resp = json.dumps(session.get("user"), indent=4)
    else:
        resp = "Please log in at <a href='/login'>/login</a>"
    return resp


@app.route("/user/<username>", methods=["GET"])
def get_user(username):
    return json.dumps(model.get_user(username))


@app.route("/user/<username>", methods=["DELETE"])
def delete_user(username):
    if model.delete_user(username):
        return "Success", 200
    else:
        return "Failure", 500


@app.route("/user/<username>", methods=["POST", "PUT"])
@app.route("/user", methods=["POST", "PUT"])
@app.route("/user/", methods=["POST", "PUT"])
def update_user(username=None):
    json_username = request.json.get("username", username)
    if json_username and username and json_username != username:
        return "Username in URL does not match username in JSON", 400
    elif not username:
        if not (username := json_username):
            return "Username not provided", 400
    return model.add_fields(username, request.json)


@app.route("/image/<image_id>")
def image(image_id):
    if image_id == "trees.png" or image_id == "smily_face.png":
        return json.dumps(
            {
                "image_id": image_id,
                "image": base64.b64encode(
                    open("static/" + image_id, "rb").read()
                ).__str__(),
            }
        )
    return json.dumps({"image_id": image_id, "image": "not found"})


@app.route("/check-connections")
def ping():
    if model.ping():
        return "Success", 200
    else:
        return "Failure", 500


@app.route("/reset")
def reset():
    model.drop_users()
    return "Success", 200


if __name__ == "__main__":
    app.run(debug=True)

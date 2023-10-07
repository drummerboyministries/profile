import base64, json
from os import environ as env
from urllib.parse import quote_plus, urlencode
import uuid

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


def get_session_sub():
    if (
        session
        and (user := session.get("user"))
        and (userinfo := user.get("userinfo"))
        and (sub := userinfo.get("sub"))
    ):
        return sub
    return None


@app.route("/self")
def self():
    if sub := get_session_sub():
        if profile := model.get_user(auth0_subject=sub):
            resp = json.dumps(profile)
        else:
            resp = 'Create new profile for the logged in user? <form action="/user/force" method="POST"><button type="submit">Create</button></form>'
        # resp = "Logged in subject: \"" + sub + "\"<br>"
    else:
        resp = "Please log in at <a href='/login'>/login</a>"
    return resp


@app.route("/user/<username>", methods=["GET"])
def get_user(username):
    return "profile: " + json.dumps(model.get_profile(username)) + f'</br><form action="/user/{username}/claim" method="POST"><button type="submit">Claim</button></form>'


@app.route("/user/<username>", methods=["DELETE"])
def delete_user(username):
    if model.delete_user(username):
        return "Success", 200
    else:
        return "Failure", 500


@app.route("/user", methods=["POST", "PUT"])
@app.route("/user/", methods=["POST", "PUT"])
@app.route("/user/force", methods=["POST", "PUT"], defaults={"claim": True})
@app.route("/user/<username>", methods=["POST", "PUT"])
@app.route("/user/<username>/claim", methods=["POST", "PUT"], defaults={"claim": True})
def update_user(username:str="", claim=False):
    """
    Creates a user with the specified username, generating a UUID for the
    username if none is provided.
    """
    if claim and not (active_user := get_session_sub()):
        return (
            'Cannot claim profile without logging in </br> <a href="login">Log in </a>',
            400,
        )
    add_dict = {"auth0_sub": active_user} if claim else {}

    if request.content_type == "application/json":
        if json_username := request.json.get("username", username):
            if username and not (json_username == username):
                return "Username in URL does not match username in JSON", 400
            elif not username:
                username = json_username # Promote josn_username to username

        # update the rest of the fields to whatever else is in the json request
        add_dict.update(request.json)
    if not username:  # and json_username is false-y, by implication
        username = uuid.uuid4().__str__()
    # Therefore, username is set

    try:
        resp = model.add_fields(username, add_dict)
    except model.ForbiddenError as e:
        return str(e), 400
    return json.dumps(resp)


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

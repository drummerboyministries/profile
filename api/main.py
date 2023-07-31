import base64, json

import flask

app = flask.Flask(__name__)

@app.route('/')
def help():
    return 'Get a user by going to /user/<username>'


@app.route('/user/<username>')
def user(username):
    return json.dumps({'username': username,
                       'profile_pic': '/image/simly_face.png',
                       'background_pic': '/image/trees.png',
                       'bio': 'I like the color green and long walks on the beach. My favorite food is pizza. I have a dog named Spot.'})

@app.route('/image/<image_id>')
def image(image_id):
    if image_id == "trees.png" or image_id == "smily_face.png":
        return json.dumps({'image_id': image_id,
                       'image': base64.b64encode(open("static/"+image_id, 'rb').read()).__str__()
                       })
    return json.dumps({'image_id': image_id, 'image': 'not found'})


if __name__ == '__main__':
    app.run(debug=True)
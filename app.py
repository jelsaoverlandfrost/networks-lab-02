from flask import Flask, jsonify, abort, request, Response
from functools import wraps
import json

# This is the server API. Run this script before you run the client script.
# Done by Mao Liyan Frosty 1002190 & Yang Lei 1002361

app = Flask(__name__)

json_file = open("pillar.json", 'r')
pillar_json = json.load(json_file)
pillar_json = pillar_json["pillar"]


# Root
@app.route('/')
def api_root():
    return 'Welcome to SUTD CourseList!'


# Authentication Checker
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    users = {'admin': 'password', 'user1': "123456", 'user2': '234567'}
    if username in users.keys():
        if password == users[username]:
            return True
    else:
        return False


# Make the checking a wrapper, so it could be applied to functions easily
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


# Show all pillar information
@app.route('/pillar', methods=['GET'])
def pillar():
    return jsonify({'name': pillar_json})


# Show a specific pillar information
@app.route('/pillar/<pillar_name>', methods=['GET'])
@requires_auth
def get_pillar(pillar_name):
    pillar = []
    for pillars in pillar_json:
        if pillars['name'] == pillar_name:
            pillar = pillars
    if len(pillar) == 0:
        abort(404)
    return jsonify({'pillar': pillar})


# Get different mimetype of the pillar information
@app.route('/pillar/<pillar_name>/info/<mime_type>', methods=['GET'])
@requires_auth
def get_text_with_format(pillar_name, mime_type):
    pillar = []
    for pillars in pillar_json:
        if pillars["name"] == pillar_name:
            pillar = pillars
        if len(pillar) == 0:
            abort(404)
        else:
            track_info = ""
            if mime_type == "info.json":
                return jsonify({'pillar': pillar})
            elif mime_type == "info.txt":
                for tracks in pillar['track']:
                    track_info = track_info + tracks['tname'] + ", "
                return "Your pillar is " + pillar_name + ", and it includes tracks: " + track_info
            else:
                abort(404)


# Get track information
@app.route('/pillar/<pillar_name>/<track_name>', methods=['GET'])
def get_track(pillar_name, track_name):
    pillar = []
    for pillars in pillar_json:
        if pillars['name'] == pillar_name:
            pillar = pillars
    if len(pillar) == 0:
        abort(404)
    else:
        track = []
        for tracks in pillar['track']:
            if tracks['tname'] == track_name:
                track = tracks
        if len(track) == 0:
            abort(404)
        return jsonify({'track': track})


# Add a new pillar
@app.route('/pillar', methods=['POST'])
@requires_auth
def create_pillar():
    if not request.json or not 'name' in request.json:
        abort(400)
    pillar = {
        "name": request.json['name'],
        "id": pillar_json[-1]['id'] + 1
    }
    pillar_json.append(pillar)
    with open("pillar.json", "w") as f:
        json.dump({"pillar": pillar_json}, f)
    return jsonify({'new_pillar': pillar}), 201


# Sends 401 if fail to authenticate
def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


# Delete a pillar with authentication
@app.route('/pillar/<pillar_name>', methods=['DELETE'])
def delete_pillar(pillar_name):
    pillar = []
    for pillars in pillar_json:
        if pillars['name'] == pillar_name:
            pillar = pillars
    if len(pillar) == 0:
        abort(404)
    pillar_json.remove(pillar)
    with open("pillar.json", "w") as f:
        json.dump({"pillar": pillar_json}, f)
    return jsonify({'pillar': pillar})


if __name__ == '__main__':
    app.run()

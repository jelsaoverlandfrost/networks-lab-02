from flask import Flask, jsonify, abort, request
import json

app = Flask(__name__)


json_file = open("pillar.json", 'r')
Pillar = json.load(json_file)
Pillar = Pillar["pillar"]


# Root
@app.route('/')
def api_root():
    return 'Welcome to SUTD CourseList!'


@app.route('/pillar', methods=['GET'])
def pillar():
    return jsonify({'name': Pillar})


@app.route('/pillar/<pillar_name>', methods=['GET'])
def get_pillar(pillar_name):
    pillar = []
    for pillars in Pillar:
        if pillars['name'] == pillar_name:
            pillar = pillars
    if len(pillar) == 0:
        abort(404)
    return jsonify({'pillar': pillar})


@app.route('/pillar/<pillar_name>/<track_name>', methods=['GET'])
def get_track(pillar_name, track_name):
    pillar = []
    for pillars in Pillar:
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


@app.route('/pillar', methods=['POST'])
def create_pillar():
    if not request.json or not 'name' in request.json:
        abort(400)
    pillar = {
        "name": request.json['name'],
        "id": Pillar[-1]['id'] + 1
    }
    Pillar.append(pillar)
    with open("pillar.json", "w") as f:
        json.dump({"pillar": Pillar}, f)
    return jsonify({'new_pillar': pillar}), 201


@app.route('/pillar/<pillar_name>', methods=['DELETE'])
def delete_pillar(pillar_name):
    pillar = []
    for pillars in Pillar:
        if pillars['name'] == pillar_name:
            pillar = pillars
    if len(pillar) == 0:
        abort(404)
    Pillar.remove(pillar)
    with open("pillar.json", "w") as f:
        json.dump({"pillar": Pillar}, f)
    return jsonify({'pillar': pillar})

if __name__ == '__main__':
    app.run()

from flask import Flask, request, jsonify
from amazonzero.test import hello_world

import pickle
import boto3
import numpy as np
from io import BytesIO
from amazonzero.board import Board
from amazonzero.player import ForestPlayer, HeuristicPlayer, Predictor, Actor

app = Flask(__name__)

def get_player(mode):
    if mode == "heuristic":
        actor = Actor()
        hp = HeuristicPlayer(actor)
        return hp
    elif mode == "forest":
        # Load the model
        s3 = boto3.resource('s3')
        with BytesIO() as data:
            s3.Bucket("game-of-amazons").download_fileobj("models/rfg3_3000pg.pkl", data)
            data.seek(0)    # move back to the beginning after writing
            model = pickle.load(data)

        # Create the player
        predictor = Predictor(model, max_mem=1_000)
        actor = Actor()
        fp = ForestPlayer(predictor, actor)
        return fp
    else:
        raise Exception("No such mode exists!")


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        print(request.json)
        boardstate = request.json.get('boardstate')
        mode = request.json.get('mode')
        if not boardstate:
            return "Request must contain json with 'boardstate'", 403

        # Create a board
        boardstate = np.array(boardstate)
        width = len(boardstate)
        n_amazons = sum(sum(np.array(boardstate) == 1))
        b = Board(width, n_amazons)
        b.matrix = boardstate

        p = get_player(mode)

        next_boardstate = p.move(b)

        return_data = {
            "next_boardstate": next_boardstate.tolist()
        }
        return jsonify(return_data)
    else:
        return "send a boardstate mate"

@app.route('/move', methods=['GET'])
def move():
    return jsonify(hello_world())

@app.route('/test', methods=['GET'])
def test():
    return "hello from test"

if __name__ == '__main__':    
    # listen on all IPs 
    app.run(host='0.0.0.0')
from flask import Flask, request, render_template, abort, jsonify, after_this_request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import random, string
import os

from db_helper import DB
import hmms_helper as hm
from validator import validate_json, validate_schema, validate_token
import re
from models import *
from config import *

PORT = 5000
ADDR = "0.0.0.0"

app = Flask(__name__)
CORS(app)

# Helping functions
def parse_results(results):
    rt = []
    scores = []
    for r in results:
        if str(r.score) == "-inf":
            r.score = 1
        scores.append(r.score)

    smin = min(scores)
    smin = (smin * -1) + 1
    scores = []
    for r in results:
        if r.score == 1:
            r.score = 0
        else:
            r.score += smin
        scores.append(r.score)

    smax = max(scores)
    for r in results:
        if r.score != 0:
            r.score = r.score * 95 / smax

    return results



# Main App route:
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template("index.html")


@app.route('/ajax/get_models', methods=["GET"])
def get_models():
    try:
        db = DB()
        models = db.get_models()
        return jsonify({"models" : [m.serialize() for m in models]}), 200
    except Exception as e:
        print(e)
        abort(500)


@app.route('/ajax/get_model/<int:model_id>', methods=["GET"])
def get_model(model_id):
    try:
        db = DB()
        model = db.get_model_by_id(model_id)
        if model:
            return jsonify({"model" : model.serialize()}), 200
        else:
            return jsonify({"error" : "Model not found"}), 400
    except Exception as e:
        print(e)
        abort(500)


@app.route('/ajax/get_binaries', methods=["GET"])
def get_binaries():
    try:
        db = DB()
        binaries = db.get_binaries()
        return jsonify({"binaries" : [b.serialize() for b in binaries]}), 200
    except Exception as e:
        print(e)
        abort(500)


@app.route('/ajax/get_binary/<int:binary_id>', methods=["GET"])
def get_binary(binary_id):
    try:
        db = DB()
        binary = db.get_binary_by_id(binary_id)
        if binary:
            return jsonify({"binary" : binary.serialize()}), 200
        else:
            return jsonify({"error" : "binary not found"}), 400
    except Exception as e:
        print(e)
        abort(500)


@app.route('/ajax/get_results/<int:binary_id>', methods=["GET"])
def get_results(binary_id):
    try:
        db = DB()
        rt = []
        binary = db.get_binary_by_id(binary_id)
        results = db.get_results_by_binary_id(binary.id)

        if len(results) != 0:
            results = parse_results(results)
            for r in results:
                m = db.get_model_by_id(r.model)
                rt.append({"model" : m.name, "score" : str(int(r.score))})

        return jsonify({"results" : rt, "analyzed" : binary.analyzed}), 200
    except Exception as e:
        print(e)
        abort(500)


@app.route('/ajax/get_jobs', methods=["GET"])
def get_jobs():
    try:
        db = DB()
        jobs = db.get_jobs()
        return jsonify({"jobs" : [j.serialize() for j in jobs]}), 200
    except Exception as e:
        print(e)
        abort(500)


@app.route('/ajax/get_running_jobs', methods=["GET"])
def get_running_jobs():
    try:
        db = DB()
        jobs = db.get_running_jobs()
        return jsonify({"jobs" : [j.serialize() for j in jobs]}), 200
    except Exception as e:
        print(e)
        abort(500)


@app.route('/ajax/create_model', methods=["POST"])
@validate_json
def create_model():
    try:
        db = DB()
        data = request.get_json(silent = True) # name, desc, benign
        model = db.add(Model(data["name"], data["desc"], data["benign"]))
        if model:
            return jsonify({"model_id" : model.id}), 200
        else:
            return jsonify({"error" : "model couldn't be created"}), 400
    except Exception as e:
        print(e)
        abort(500)


@app.route('/ajax/upload_model_file/<int:model_id>', methods=["POST"])
def upload_model_file(model_id):
    try:
        db = DB()
        model = db.get_model_by_id(model_id)
        if not model:
            return jsonify({"error" : "Model not found"}), 400
        file = request.files['file']
        if file and file.filename:
            file.save(os.path.join(FILE_UPLOAD_FOLDER, model.filename+".zip"))
            hm.create_model(model.id)

        return jsonify({}), 200
    except Exception as e:
        print(e)
        abort(500)


@app.route('/ajax/create_binary', methods=["POST"])
@validate_json
def create_binary():
    try:
        db = DB()
        data = request.get_json(silent = True) # name, desc, benign
        binary = db.add(Binary(data["name"]))
        if binary:
            return jsonify({"binary_id" : binary.id}), 200
        else:
            return jsonify({"error" : "binary entry couldn't be created"}), 400
    except Exception as e:
        print(str(e))
        abort(500)


@app.route('/ajax/upload_binary_file/<int:binary_id>', methods=["POST"])
def upload_binary_file(binary_id):
    try:
        db = DB()
        binary = db.get_binary_by_id(binary_id)
        if not binary:
            return jsonify({"error" : "Binary not found"}), 400
        file = request.files['file']
        if file and file.filename:
            file.save(os.path.join(FILE_UPLOAD_FOLDER, binary.filename+".bin"))
            hm.analyze_binary(binary.id)
        return jsonify({}), 200
    except Exception as e:
        print(e)
        abort(500)


if __name__ == '__main__':
   app.run(host=ADDR, port=PORT)

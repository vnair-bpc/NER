from flask import Flask, jsonify, request
from Bio_Epidemiology_NER.bio_recognizer import ner_prediction
import logging
import json
import sys

app = Flask(__name__)
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)

# Load the configuration from the JSON file
with open("config.json", "r") as config_file:
    config_data = json.load(config_file)


def validate_api_key(request):
    code = request.args.get("code")
    if code == config_data["extractner"]["code"]:
        return True
    else:
        return False

@app.route("/extractner", methods=["GET"])
def extractner():    
    if not validate_api_key(request):
        return jsonify("Authorization Failed"), 401
    
    req_body = request.json
    doc = req_body.get('doc')
    try:
        results = ner_prediction(corpus=doc, compute='cpu')
        data_dict = results.to_dict(orient='records')
        json_output = json.dumps(data_dict, indent=4)
        return json_output,200
    except Exception as e:
        return str(e),500
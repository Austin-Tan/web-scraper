from flask import Flask, jsonify, request, send_from_directory
import subprocess
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

VISUALIZER_DIR = ROOT / "visualizer"
DATA_DIR = ROOT / "data"

CONFIG_PATH = DATA_DIR / "config.json"
CSV_PATH = DATA_DIR / "output.csv"

app = Flask(__name__, static_folder=str(VISUALIZER_DIR), static_url_path="")


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/data")
def get_data():
    return send_from_directory(DATA_DIR, "output.csv")


@app.route("/config", methods=["GET", "POST"])
def config():
    if request.method == "GET":
        if CONFIG_PATH.exists():
            return jsonify(json.loads(CONFIG_PATH.read_text()))
        return jsonify({})

    # POST: update config
    CONFIG_PATH.write_text(json.dumps(request.json, indent=2))
    return jsonify({"status": "saved"})


@app.route("/run", methods=["POST"])
def run_pipeline():
    subprocess.run(["python", "src/run.py"], check=True)
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)

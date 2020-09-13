import base64
from dotenv import load_dotenv
from flask import Flask, request, url_for, redirect
import os
import requests
import json

load_dotenv()

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def upload():
    headers = {"app_id": os.environ["APP_ID"], "app_key": os.environ["APP_KEY"]}
    payload = {
        "src": f'data:image/jpg;base64,{base64.b64encode(request.files["file"].read()).decode()}'
    }

    mathpix = requests.post(
        "https://api.mathpix.com/v3/text", headers=headers, json=payload
    ).json()

    r = requests.get(
        f"https://latex.codecogs.com/png.latex?\\bg_white \\LARGE {mathpix['latex_styled']}"
    )
    with open(f"static/{mathpix['request_id']}.png", "wb") as f:
        f.write(r.content)

    return redirect(url_for("static", filename=f"{mathpix['request_id']}.png"))

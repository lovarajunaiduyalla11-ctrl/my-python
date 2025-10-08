import os
import yaml
from flask import Flask, render_template

CONFIG_PATH = "config.yaml"

def load_config():
    cfg = {
        "title": "My Example Site",
        "message": "Hello — edit config.yaml or set env vars to customize!",
        "image": "/static/logo.png"
    }
    # Try file
    try:
        with open(CONFIG_PATH, "r") as f:
            file_cfg = yaml.safe_load(f) or {}
            cfg.update(file_cfg)
    except FileNotFoundError:
        pass

    # Allow env var overrides
    cfg["title"] = os.getenv("SITE_TITLE", cfg["title"])
    cfg["message"] = os.getenv("SITE_MESSAGE", cfg["message"])
    cfg["image"] = os.getenv("SITE_IMAGE", cfg["image"])
    return cfg

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    config = load_config()
    return render_template("index.html", **config)

if __name__ == "__main__":
    cfg = load_config()
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)

from flask import Flask
from flask_cors import CORS
from .notes.blueprint_notes import blueprint_notes

app = Flask(__name__)
CORS(app)
app.register_blueprint(blueprint_notes, url_prefix="/api/v1/notes")

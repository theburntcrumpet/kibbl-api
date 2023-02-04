from flask import Flask, jsonify
import sys
from .notes.blueprint_notes import blueprint_notes

app = Flask(__name__)
app.register_blueprint(blueprint_notes, url_prefix="/api/v1/notes")

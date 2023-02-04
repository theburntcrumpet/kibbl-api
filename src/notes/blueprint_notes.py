from flask import Blueprint, jsonify, request, make_response
from .cache_service import search_notes, index_notes
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import time

BASE_DIRECTORY = "/app/notes"

# define the blueprint
blueprint_notes = Blueprint(name="blueprint_notes", import_name=__name__)
notes = []


@blueprint_notes.route('/', methods=['GET'])
def list_notes():
    query = request.args.get('q', "")
    return jsonify([note["file"] for note in search_notes(query, notes)])


@blueprint_notes.route("/data")
def get_note():
    file = request.args.get('f', None)
    if file is None:
        return ""
    with open(BASE_DIRECTORY+file, "rb") as f:
        response = make_response(f.read(), 200)
        response.mimetype = "text/plain"
        return response

def index_notes_job():
    global notes
    start = time.time()
    notes = index_notes(BASE_DIRECTORY)
    print(f"Indexed {len(notes)} notes in {time.time()-start:.2f} seconds")


sched = BackgroundScheduler(daemon=True)
sched.add_job(index_notes_job, 'interval', minutes=5,
              next_run_time=datetime.now())
sched.start()

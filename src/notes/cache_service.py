import glob
import re
from blooms import blooms
from hashlib import sha256
import time


def bloom_from_string(bs):
    bloom = blooms(768)
    for w in bs.split(" "):
        bloom @= (sha256(w.encode()).digest())
    return bloom


def check_string_in_bloom(s, b):
    return sha256(s.encode()).digest() @ b


def check_strings_in_bloom(sa, b):
    for s in sa:
        if not check_string_in_bloom(s, b):
            return False
    return True


def index_notes(base_path="/home/matthew"):
    # Get all markdown files
    md_files = glob.glob(f"{base_path}/**/*.md", recursive=True)
    notes = []
    for filename in md_files:
        with open(filename, "r") as open_file:
            f = " ".join(open_file.readlines()).lower().strip()
            f = re.sub("[^a-zA-Z0-9\s]", '', f)
        bloom = bloom_from_string(f)
        notes.append({"file": filename.replace(
            base_path, "", 1), "filter": bloom})
    return notes


def search_notes(query, notes):
    qs = query.lower()
    qs = re.sub("[^a-zA-Z0-9\s]", '', qs)
    query_words = qs.split(" ")
    filename_matches = []
    content_matches = []
    for note in notes:
        if qs in note["file"].lower():
            filename_matches.append(note)
            continue

        for query_word in query_words:
            if query_word in note["file"]:
                filename_matches.append(note)
                break

        if check_strings_in_bloom(query_words, note["filter"]):
            content_matches.append(note)
    return filename_matches + content_matches


if __name__ == "__main__":
    start = time.time()
    notes = index_notes()
    print(f"Indexed {len(notes)} files in {time.time()-start} seconds")
    start = time.time()
    results = search_notes("kevin", notes)
    print(f"Took {time.time() - start}, returned {len(results)}")
    print([f["file"] for f in results])

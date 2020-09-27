#  __  __ ____   ______ ____
#  \ \/ // __ \ / ____// __ \
#   \  // /_/ // __/  / /_/ /
#   / // ____// /___ / _, _/
#  /_//_/    /_____//_/ |_|
#
#  By Davidson Gonçalves
#  github.com/davidsongoap/yper

import json
import pickle

import requests


def fetch_words(n_paragraphs, min_words, max_words):
    text_type = "giberish"  # lorem / giberish
    link = f"https://www.randomtext.me/api/{text_type}/p-{n_paragraphs}/{min_words}-{max_words}"
    resp = requests.get(link)
    r = json.loads(resp.content.decode())
    words = r["text_out"].replace("<p>", "") \
                         .replace("</p>", "") \
                         .replace(".", "") \
                         .replace(",","") \
                         .lower().split()

    # remove duplicate words
    words = list(set(words))
    return words


def check_internet():
    try:
        import httplib
    except ModuleNotFoundError:
        import http.client as httplib
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False


def load_scores(filename):
    try:
        scores = pickle.load(open(filename, "rb"))
    except FileNotFoundError:
        save_scores([], filename)
        return load_scores()
    return scores

def save_scores(scoreboard, filename):
    pickle.dump(scoreboard, open(filename, "wb"))

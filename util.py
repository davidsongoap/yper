#  __  __ ____   ______ ____
#  \ \/ // __ \ / ____// __ \
#   \  // /_/ // __/  / /_/ /
#   / // ____// /___ / _, _/
#  /_//_/    /_____//_/ |_|
#
#  By Davidson Gonçalves
#  github.com/davidsongoap

import requests
import json

def fetch(n_paragraphs, min_words, max_words):
    text_type = "giberish" # lorem / giberish
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
    except:
        import http.client as httplib
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False

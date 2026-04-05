import json
import time
import urllib.parse
import urllib.request
from urllib.error import HTTPError

query = "multicomponent diffusion in silicate melts"

url = "https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode({
    "query": query,
    "limit": 3,
    "fields": "title,abstract,year,authors"
})

req = urllib.request.Request(
    url,
    headers={
        "User-Agent": "myapp/0.1",
        # Add this only if you get an API key later:
        # "x-api-key": "YOUR_SEMANTIC_SCHOLAR_KEY"
    }
)

for attempt in range(5):
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        print(json.dumps(data, indent=2)[:4000])
        break
    except HTTPError as e:
        if e.code == 429 and attempt < 4:
            wait = 2 ** attempt
            print(f"Rate limited. Retrying in {wait} seconds...")
            time.sleep(wait)
        else:
            raise
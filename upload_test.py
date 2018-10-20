
import requests
import json

URL = "http://localhost:5000"
content = "Hello internet!"

r = requests.post(
    URL + "/upload-text",
    data = {
        "filename": "some.txt",
        "data":content
    })

hashcode = r.json()["hashcode"]
r = requests.get(URL + "/files/" + hashcode)
assert(r.content == content)

print("PASS")

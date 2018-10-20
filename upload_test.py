
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


coffeefile = open('coffee.png', 'rb')
files = {'coffee.png': coffeefile}

r = requests.post(
    URL + "/upload-file",
    files = files)

hashcode = r.json()["hashcode"]
print(hashcode)


coffeefile = open('coffee.png', 'rb')
files = {'coffee.png': coffeefile}

r = requests.post(
    URL + "/upload-files",
    files = files)

hashcodes = r.json()["hashcodes"]
print(hashcodes)

assert(hashcodes[0] == hashcode)
print("PASS")

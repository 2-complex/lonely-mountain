import implementation
import json
import database
import os


if os.path.isfile("temp.db"):
    os.remove("temp.db")

db = database.Database("sqlite:///temp.db")
impl = implementation.Implementation(db.models, db.session)

print("PASS")


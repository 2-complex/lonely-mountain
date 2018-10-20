import database
import datetime
import time

db = database.Database("sqlite:///testing.db")

now = datetime.datetime.utcnow()
a_long_time_ago = now - datetime.timedelta(days=10)

def make_current(file):
    file.timestamp = now

def display(file):
    print file
    with open("cleanup.log.txt", "a") as f:
        f.write(str(file) + "\n")

def update_null_timestamps():
    files_with_no_timestamp = db.models.File.query.filter_by(timestamp=None).all()
    map( make_current, files_with_no_timestamp )
    db.session.commit()

def delete_old_files():
    old_files = db.models.File.query.filter(db.models.File.timestamp < a_long_time_ago).all()
    map( display, old_files )
    map( db.session.delete, old_files )
    db.session.commit()

while True:
    update_null_timestamps()
    delete_old_files()
    time.sleep(60*60)


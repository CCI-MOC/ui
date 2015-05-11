rm db.sqlite3
python manage.py syncdb
python manage.py loaddata inital_data.json

rm db.sqlite3
python manage.py syncdb
# python manage.py loaddata initial_data.json
python manage.py loaddata service_list.json
python manage.py loaddata projects.json
python manage.py loaddata users.json


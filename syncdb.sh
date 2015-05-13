rm db.sqlite3
python manage.py syncdb
<<<<<<< HEAD
python manage.py loaddata inital_data.json
=======
python manage.py loaddata service_list.json
python manage.py loaddata projects.json
python manage.py loaddata users.json
>>>>>>> lucasRefactor

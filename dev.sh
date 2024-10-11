source .venv/bin/activate
cd mysite
pip install -r requirements.txt
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
cd ..

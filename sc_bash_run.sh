#!/bin/bash

# для bash | запуск через ./bash_run.sh
source venv/bin/activate
cd project && python manage.py tailwind start && python manage.py runserver

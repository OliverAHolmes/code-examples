setup: 
	uv venv && source .venv/bin/activate
	uv sync && cd app && python manage.py migrate     


run:
	cd app && python3 manage.py runserver       

create_superuser:
	cd app && python manage.py createsuperuser


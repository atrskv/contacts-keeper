dev:
	flask --app app:create_app run --debug --port 8000

prod:
	flask --app app:create_app run --port 8000

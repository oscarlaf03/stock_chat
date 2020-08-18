runserver:
	gunicorn --worker-class eventlet -w 1 server:app --bind=0.0.0.0:5000 --access-logfile - --log-level=debug

runworker:
	python3 bot_q.py
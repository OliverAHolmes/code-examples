dev:
	@echo "Starting Django, FastAPI, and React in tmux session..."
	tmux new-session -d -s dev 'cd backend && source .venv/bin/activate && cd app && python manage.py runserver'
	tmux split-window -h -t dev:0 'cd micro-service && source .venv/bin/activate && uvicorn main:app --reload --port 8001'
	tmux split-window -v -t dev:0 'cd frontend && deno run dev'
	tmux select-layout -t dev:0 tiled
	tmux attach-session -t dev

make_keys:
	@echo "Generating key..."
	cd backend/app && openssl genrsa -out private_key.pem 2048 && openssl rsa -in private_key.pem -pubout -out public_key.pem
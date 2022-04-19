run:
	python main.py
beauty:
	isort .
	black .
	flake8 .  --exit-zero

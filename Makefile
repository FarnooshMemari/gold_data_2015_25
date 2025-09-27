install:
	pip install --upgrade pip && \
	pip install -r requirements.txt

format:
	black .

lint:
	lint:
	flake8 --ignore=E501,W503 analysing_gold_data.py

clean:
	rm -rf __pycache__ .pytest_cache .coverage

# 'all' runs everything in sequence
all: install format lint clean

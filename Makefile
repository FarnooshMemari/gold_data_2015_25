install:
	pip install --upgrade pip && \
	pip install -r requirements.txt

format:
	black *.py

lint:
	flake8 analysing_gold_data.py

clean:
	rm -rf __pycache__ .pytest_cache .coverage

# 'all' runs everything in sequence
all: install format lint clean

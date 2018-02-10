.PHONY: clean test lint

clean:
	find . -name "*.pyc" -exec rm {} \;
test:
	python -m pytest -s
lint:
	flake8
	mypy src

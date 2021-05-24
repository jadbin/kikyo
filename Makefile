build:
	pip install -e .

clean:
	@rm -rf build dist *egg-info
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete

.PHONY: build clean upload

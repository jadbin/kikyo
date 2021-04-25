build:
	pip install -e .

clean:
	@rm -rf build dist *egg-info
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete

upload:
	twine upload dist/* --repository-url https://pypi.kdsec.org/

.PHONY: build clean upload

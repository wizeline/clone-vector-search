lint:
	@pip install black isort flake8
	@echo "\n--->Sorting imports"
	@isort .
	@echo "\n----->Formating code"
	@black .
	@echo "\n------>Linting code"
	@flake8 .
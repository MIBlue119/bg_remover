.DEFAULT_GOAL := help
.PHONY:  install test linter-pylint linter-flake8 docstyle 

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Install requirements
	pip install -r requirements.txt

pyinstall_windows: ## [windows] Package the app with pyinstaller 
	pyinstaller app_windows.spec -y --onedir --windowed

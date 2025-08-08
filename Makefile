# Makefile

.DEFAULT_GOAL := help

version = "0.1.0"


help:
	@echo "AVAILABLE COMMANDS"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf " \033[36m%-30s\033[0m %s\n", $$1, $$2}'

bake: ## Setup UV environment and install base dependencies
	@echo "🍰 Setting up your Python UV environment..."
	@uv add loguru || exit 1
	@uv add --group test pytest pytest-cov hypothesis || exit 1
	@uv add --group dev radon cloc black ruff ty || exit 1
	@git init . || exit 1
	@echo "✅ Environment setup complete! Time to code."

run: ## Launch the main Python application (Streamlit)
	@echo "🚀 Running the Rostr extraction..."
	@uv run main.py || { echo "❌ Application failed to run."; exit 1; }

reqs: ## Export dependencies to requirements.txt
	@echo "📦 Generating requirements.txt..."
	@uv pip freeze > requirements.txt || { echo "❌ Failed to generate requirements.txt"; exit 1; }
	@echo "✅ requirements.txt created."

lock: ## Update uv.lock file
	@echo "🔒 Locking dependencies..."
	@uv lock || { echo "❌ Failed to update uv.lock"; exit 1; }
	@echo "✅ uv.lock updated."

cloc: ## Count lines of code using cloc (must be installed first)
	@echo "📊 Counting lines of code..."
	@uv run cloc --exclude-dir .venv,.DS_Store --exclude-ext gif,pyc . || { echo "❌ cloc failed"; exit 1; }

quality: ## Check code quality metrics with radon
	@echo "🧹 Analyzing code quality metrics..."
	@uv run radon cc mi hal . -a -na -s || { echo "❌ radon failed"; exit 1; }

format: ## Format code with black and ruff
	@echo "🎨 Formatting code..."
	@uv run black . || { echo "❌ black formatting failed"; exit 1; }
	@uv run ruff check -e --fix . || { echo "❌ ruff formatting failed"; exit 1; }

type: ## Perform static type checking with ty astral tool
	@echo "🔍 Running mypy type checking..."
	# @uv run mypy ./src || { echo "❌ mypy found issues"; exit 1; }
	@uv run ty check || { echo "❌ mypy found issues"; exit 1; }

clean: ## @deprecated: Clean unwanted files (Windows)
	@echo "🧹 Cleaning up the repository (Windows)..."
	@powershell -Command "Get-ChildItem -Path . -Include '__pycache__', '.pytest_cache', '.ipynb_checkpoints', '.DS_Store', '*.egg-info', 'pip-wheel-metadata', 'tmp*', '.cache', '.mypy_cache', 'htmlcov', 'generated' -Recurse -Force | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue" || { echo "❌ Cleanup failed (directories)"; exit 1; }
	@powershell -Command "Get-ChildItem -Path . -Include '*.pyc', '*.pyo', '*~', '.*~', '.coverage', '.coverage.*' -Recurse -Force | Remove-Item -Force -ErrorAction SilentlyContinue" || { echo "❌ Cleanup failed (files)"; exit 1; }
	@powershell -Command "Write-Host '✅ Repository cleaned (Windows)!' -ForegroundColor Green"

uclean: ## @deprecated: Clean unwanted files (Linux/MacOS)
	@echo "🧹 Cleaning up the repository (Linux/MacOS)..."
	@find . -type d \( -name '__pycache__' -o -name '.pytest_cache' -o -name '.ipynb_checkpoints' -o -name '*.egg-info' -o -name 'pip-wheel-metadata' -o -name 'tmp*' -o -name '.cache' -o -name '.mypy_cache' -o -name 'htmlcov' -o -name 'generated' \) -exec rm -rf {} + || { echo "❌ Cleanup failed (directories)"; exit 1; }
	@find . -type f \( -name '*.py[co]' -o -name '*~' -o -name '.*~' -o -name '.coverage' -o -name '.coverage.*' -o -name '.DS_Store' \) -exec rm -f {} + || { echo "❌ Cleanup failed (files)"; exit 1; }
	@echo "✅ Repository cleaned (Linux/MacOS)!"
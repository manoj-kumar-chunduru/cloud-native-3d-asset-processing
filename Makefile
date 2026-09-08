install:
	python -m pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check .

run:
	uvicorn asset_platform.api:app --reload

benchmark:
	python benchmarks/run_benchmark.py

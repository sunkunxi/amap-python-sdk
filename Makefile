lint:
	poetry run ruff format
	poetry run ruff check --fix
	poetry run mypy

# 运行测试
test:
	pytest -s .

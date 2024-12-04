.PHONY: dev
dev: uv
	uv sync --dev

.PHONY: install
install: uv
	uv sync
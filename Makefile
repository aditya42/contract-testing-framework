.PHONY: install clean lint consumer provider-api provider contract-test test

install:
	python -m pip install --upgrade pip
	python -m pip install -e ".[dev]"

clean:
	rm -rf pacts reports .pytest_cache .coverage htmlcov
	mkdir -p pacts reports

lint:
	ruff check src tests

consumer:
	pytest tests/consumer -m consumer_contract --html=reports/consumer-contract.html --self-contained-html

provider-api:
	pytest tests/provider/test_provider_api.py -m provider_api --html=reports/provider-api.html --self-contained-html

provider:
	pytest tests/provider/test_user_provider_contract.py -m provider_contract --html=reports/provider-contract.html --self-contained-html

contract-test: clean lint consumer provider-api provider

test: contract-test

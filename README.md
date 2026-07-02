# Python Contract Testing Framework

A GitHub-ready consumer-driven contract testing framework built with **Pact V4**, **pytest**, and **FastAPI**.

## What it validates

The consumer defines the smallest API contract it depends on. Pact starts a mock provider, verifies the real consumer client, and writes a JSON contract. Provider verification then replays every interaction against the running FastAPI service and fails if the implementation is incompatible.

Included cases:

1. `GET /users/123` returns an existing user with the required field types.
2. `GET /users/999` returns the expected `404` error contract.
3. `POST /users` accepts the required request body and returns `201` with a compatible user response.
4. Direct provider smoke tests cover health, not-found behavior, and creation.

## Project structure

```text
contract-testing-framework/
├── .github/workflows/contract-tests.yml
├── pacts/                              # generated Pact JSON contracts
├── reports/                            # generated pytest HTML reports
├── src/contract_framework/
│   ├── consumer/client.py              # real consumer HTTP client
│   └── provider/
│       ├── app.py                      # sample FastAPI provider
│       └── repository.py               # deterministic test data store
├── tests/
│   ├── consumer/
│   │   ├── conftest.py
│   │   └── test_user_consumer_contract.py
│   └── provider/
│       ├── conftest.py
│       ├── test_provider_api.py
│       └── test_user_provider_contract.py
├── Makefile
└── pyproject.toml
```

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
make install
```

Run the entire quality gate:

```bash
make contract-test
```

The sequence is intentional:

```text
consumer tests -> generate Pact JSON -> provider smoke tests -> provider verification
```

Run stages separately:

```bash
make consumer
make provider-api
make provider
```

## Expected result

```text
3 consumer contract tests passed
3 provider API tests passed
1 provider verification test passed
```

The generated contract is written to:

```text
pacts/user-consumer-user-provider.json
```

HTML reports are written under `reports/`.

## Adding another endpoint

1. Add the endpoint call to the production consumer client.
2. Add one consumer interaction using `upon_receiving`, `given`, `with_request`, and `will_respond_with`.
3. Add or reuse a provider-state handler so verification data is deterministic.
4. Run `make contract-test` and commit the application change, not the generated local reports.

## Production extension with Pact Broker or PactFlow

For multiple repositories, publish consumer contracts to a Pact Broker and let provider pipelines fetch and verify them. Add `can-i-deploy` before deployment to prevent releasing incompatible consumer/provider versions. Keep broker credentials in GitHub Actions secrets rather than source control.

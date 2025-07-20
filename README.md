# Python Load Tests

## Links

- [Locust Report on GitHub Pages](https://nikita-filonov.github.io/python-load-tests/16393567752/)
- [GitHub Actions CI/CD](https://github.com/Nikita-Filonov/python-load-tests/actions)

## Overview

This project showcases a fully structured and production-ready framework for performance testing of REST APIs using
[Locust](https://locust.io/) and Python. It is designed with scalability, extensibility, and CI/CD integration in mind —
making it suitable both for local test runs and automated pipelines in real-world projects.

Unlike minimal Locust demos, this project demonstrates how to build an engineering-grade solution that can:

- validate **system performance** under realistic and repeatable loads,
- simulate different types of **user behavior scenarios**,
- prepare consistent test data through **API-level seeding**,
- run tests in CI pipelines and publish **shareable HTML reports** automatically.

This framework can serve as a **reference architecture** for teams working with microservices, fintech APIs, or any
backend requiring performance validation.

The project implements key engineering principles:

- 🧱 **Modular architecture.** Each component is isolated: [API clients](./clients), [routing](./tools/routes.py),
  [seeders](./seeds), user logic, and [Locust](https://locust.io/) scenarios live in their own layers. This allows
  reuse, testing in isolation, and faster onboarding.
- 🔄 **Realistic test data generation via seeding.** The system uses actual API calls to prepare data before tests (no DB
  hacks). This ensures full alignment with production business logic and avoids test pollution.
- ⚙️ **Typed HTTP clients with metric instrumentation.** Based on [HTTPX](https://www.python-httpx.org/)
  and [pydantic](https://docs.pydantic.dev/latest/), each client includes [event hooks](./clients/event_hooks.py) to
  report response times and errors directly into Locust metrics. No manual timers or wrappers needed.
- 📦 **Strict environment configuration.** All base URLs, timeouts, and environment-specific parameters are managed via
  [.env](./.env) and validated using [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/).
- 🚀 **Scenario-driven test execution.** Each load test is encapsulated in a folder with a versioned `.conf` file and
  scenario code. Scenarios are easily selectable and traceable, ideal for version control and team collaboration.
- 📊 **HTML reporting with GitHub Pages support.** Each CI run generates an
  interactive [Locust HTML report](https://nikita-filonov.github.io/python-load-tests/16393567752/), published to
  GitHub Pages for easy sharing and comparison between runs.
- 🔁 **Clear separation of concerns.** Business logic is encapsulated in [clients](./clients/operations_client.py); load
  orchestration lives in [TaskSets](./tools/locust/task_set.py); data generation is isolated
  in [seeders](./seeds/builder.py). This improves readability, test stability, and long-term maintainability.

The API under test is the [FakeBank API](https://sampleapis.com/api-list/fakebank), which simulates banking operations
such as transactions and account history. This makes the project ideal for demo environments, educational purposes, or
CI/CD experiments without relying on production services.

---

## Stack and Features

- [Locust](https://locust.io/) — Load testing framework written in Python.
- [HTTPX](https://www.python-httpx.org/) — High-performance HTTP client with async support.
- [Pydantic](https://docs.pydantic.dev/) — Data validation and serialization.
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) — Typed config via `.env`.
- [Faker](https://faker.readthedocs.io/en/master/) — Randomized test data generator.
- [GitHub Actions](https://github.com/features/actions) — CI/CD pipeline with headless test execution and report
  publishing.

---

## Directory Structure

- [clients/](./clients) — API clients using HTTPX + Locust hooks
- [schema/](./schema) — Pydantic models for request/response
- [tools/](./tools) — Fakers, routing, base user classes
- [seeds/](./seeds) — Seeding logic for generating realistic data
- [scenarios/](./scenarios) — Load test scenarios (with and without seeding)
- [.github/](./.github/workflows/load-tests.yaml) — GitHub Actions workflow

---

## Setup Instructions

### Prerequisites

Ensure that you have the following installed on your system:

- Python 3.11 or later
- pip (Python package manager)
- Git

### Installation

Clone the repository and navigate to the project directory:

```shell
git clone https://github.com/Nikita-Filonov/python-load-tests.git
cd python-load-tests
```

Create and activate a virtual environment:

```shell
python -m venv venv # Create virtual environment
source venv/bin/activate # Activate on macOS/Linux
venv\Scripts\activate # Activate on Windows
```

Install dependencies:

```shell
pip install --upgrade pip # Upgrade pip to the latest version
pip install -r requirements.txt # Install required dependencies
```

---

## Running Locust Tests Locally

You can run any scenario using its `.conf` file:

```bash
locust --config=./scenarios/get_operation_with_seeds/v1.0.conf
```

Or, to run interactively:

```bash
locust -f ./scenarios/get_operation_with_seeds/scenario.py
```

### Example scenario includes:

- [get_operation_with_seeds](./scenarios/get_operation_with_seeds/scenario.py): reuses prepared test data (realistic
  load).
- [get_operation_without_seeds](./scenarios/get_operation_without_seeds/scenario.py): creates data on the fly (less
  efficient).

---

## Seeding (Test Data Preparation)

The project uses a builder-based seeding approach via real API calls, preserving business logic. To generate test data
before the load test:

```python
from seeds.builder import get_seeds_builder
from seeds.dumps import save_seeds_result
from seeds.schema.plan import SeedsPlan, SeedOperationsPlan

builder = get_seeds_builder()
result = builder.build(SeedsPlan(operations=SeedOperationsPlan(count=20)))

save_seeds_result(result=result, scenario="load-testing-scenario-name")
```

---

## Running in CI/CD

[GitHub Actions](https://github.com/Nikita-Filonov/python-load-tests/actions) is used for headless execution and
automated publishing.

### Manual Trigger

Go
to [Actions](https://github.com/Nikita-Filonov/python-load-tests/actions) →
[Load Tests](https://github.com/Nikita-Filonov/python-load-tests/actions/workflows/load-tests.yaml) →
Run Workflow and select a scenario.

### Publishing Reports

Each Locust HTML report is:

- Saved in [reports/<run_id>/index.html](https://github.com/Nikita-Filonov/python-load-tests/tree/gh-pages/16391655925)
- Uploaded as an artifact
- Published to [gh-pages](https://github.com/Nikita-Filonov/python-load-tests/tree/gh-pages) for persistent access

### Accessing Reports

After each CI run, you can:

- View HTML reports via GitHub
  Pages → [https://<your-user>.github.io/python-load-tests/<run_id>/](https://nikita-filonov.github.io/python-load-tests/16393581176/)
- [Download artifacts from GitHub Actions interface](https://github.com/Nikita-Filonov/python-load-tests/actions/runs/16393581176)

---

## Summary

This project provides a production-grade framework for performance testing RESTful APIs using Locust and Python. Unlike
simplistic examples or ad-hoc scripts, this solution is designed with scalability, modularity, and automation at its
core.

It includes:

- ⚙️ **Typed and configurable API clients.** Built on top of httpx, all clients are designed for reuse, support
  timeouts, base URLs, and inject performance metrics via event hooks. The client layer is strongly typed using Pydantic
  models, ensuring contract integrity and maintainability.
- 📦 **Scenario-based architecture.** Load tests are organized as standalone, versioned scenarios with declarative
  configuration (`.conf` files), making it easy
  to develop, isolate, and benchmark different use cases under load. Each scenario follows consistent structure and
  behavior.
- 📈 **Realistic and reusable test data via API-based seeding.** Instead of mocking data or injecting it directly into
  databases, the framework provides a clean, API-level seeding
  mechanism. It respects the domain logic of the system under test and allows you to preload consistent user and
  operation data into the system — and reuse it across test runs.
- 🔁 **Separation of load generation and business logic.** Load profiles (via Locust’s TaskSet/SequentialTaskSet) are
  clearly
  separated from client logic and data generation. This
  separation of concerns improves test clarity and promotes reuse across teams and use cases.
- 🔗 **Full CI/CD integration with GitHub Actions.** The framework supports headless execution in CI, generates reports
  automatically, and publishes them to GitHub Pages.
  This allows effortless sharing of test results with stakeholders or embedding them into your quality gates.
- 📊 **Historical report access via GitHub Pages.** Each test run generates a full HTML report using Locust’s built-in
  visualization, saved per-run and published
  automatically. You can track regressions or improvements over time.

### Why It Matters

Most performance testing frameworks are either too academic or too coupled to a specific stack. This project
demonstrates how to design a maintainable, versioned, and extensible solution — with clear upgrade paths, CI
compatibility, and production-level realism in data and execution.

It’s well-suited for:

- QA engineers building repeatable performance tests
- Backend engineers validating load assumptions pre-release
- SRE/DevOps teams integrating load tests into CI pipelines
- Educators and course authors teaching real-world performance testing
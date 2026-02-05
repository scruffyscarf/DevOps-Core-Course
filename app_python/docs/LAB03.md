# Lab 3 — Continuous Integration (CI/CD)

![CI](https://github.com/scruffyscarf/DevOps-Core-Course/actions/workflows/python-ci.yml/badge.svg)

[![Coverage Status](https://coveralls.io/repos/github/scruffyscarf/DevOps-Core-Course/badge.svg?branch=lab03)](https://coveralls.io/github/scruffyscarf/DevOps-Core-Course?branch=lab03)

## Testing Framework
**pytest** was chosen because:
- Simple and readable syntax
- Powerful fixtures
- Industry standard for Python projects
- Excellent CI integration

### Test Structure
Covered endpoints:
- `GET /` — response structure and required fields
- `GET /health` — service health status

## Run tests

```bash
cd app_python
pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest
coverage run -m pytest
coverage report
```

## Result

```bash
======================================================================= test session starts =======================================================================
platform darwin -- Python 3.14.2, pytest-9.0.2, pluggy-1.6.0
rootdir: /Users/scruffyscarf/DevOps-Core-Course/app_python
collected 2 items                                                                                                                                                 

tests/test_health_endpoint.py .                                                                                                                             [ 50%]
tests/test_main_endpoint.py .                                                                                                                               [100%]

======================================================================== 2 passed in 0.15s ========================================================================
```

## Versioning Strategy
**Semantic Versioning (SemVer)** was chosen:
- It is more informative about the compatibility of changes
- It's easier to track dependencies between versions
- Standard practice in the Docker ecosystem

[Docker Image](https://hub.docker.com/r/scruffyscarf/info-service-python/tags)

## CI Workflow Triggers
The Python CI workflow runs on:
- `push` to `master`, `lab01`, `lab02`, `lab03`
- only when files in `app_python/**` change
- `pull_request` affecting `app_python/**`

## Versioning Strategy
**Calendar Versioning (CalVer)** was chosen:
- Aligns well with continuous delivery
- Simple and predictable
- Avoids manual semantic version bumps

## CI Best Practices

- **Dependency caching** - speeds up CI by reusing installed Python packages.

- **Path-based triggers** - prevents unnecessary workflow runs in monorepo setup.

- **Fail-fast testing** - coverage threshold prevents merging poorly tested code.

- **Separate jobs**  - improves clarity and parallel execution.

## Caching Results
- First run: ~1 minute
- Cached run: 23 seconds

### Snyk Security Scan
- Scans both runtime and dev dependencies
- No critical vulnerabilities found
- Workflow fails automatically on detected issues

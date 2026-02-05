# Lab 3 — Continuous Integration (CI/CD)

![CI](https://github.com/scruffyscarf/DevOps-Core-Course/actions/workflows/go-ci.yml/badge.svg)

[![Coverage Status](https://coveralls.io/repos/github/scruffyscarf/DevOps-Core-Course/badge.svg?branch=lab03)](https://coveralls.io/github/scruffyscarf/DevOps-Core-Course?branch=lab03)

## Run tests

```bash
cd app_go
go test ./...
```

## Result

```bash
ok      info-service    0.867s
```

## Versioning Strategy
**Semantic Versioning (SemVer)** was chosen:
- It is more informative about the compatibility of changes
- It's easier to track dependencies between versions
- Standard practice in the Docker ecosystem

[Docker Image](https://hub.docker.com/r/scruffyscarf/info-service-go/tags)

## CI Workflow Triggers
The Go CI workflow runs on:
- `push` to `master`, `lab01`, `lab02`, `lab03`
- only when files in `app_go/**` change
- `pull_request` affecting `app_go/**`

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

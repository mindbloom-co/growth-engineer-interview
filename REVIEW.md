# Review guidance

Guidance for code review in this repository. The repository-specific rules at the end
take precedence over the general checklist where they are more specific.

## How to review

- Judge the change by its actual runtime behavior. Read the surrounding code, callers,
  and existing tests before raising a finding, and confirm the flagged path is reachable.
- Ground convention findings in a concrete source in this repository (a doc, a config
  file, or an established pattern in nearby code) and name it. When the repository is
  silent, present the finding as general best practice; do not invent house rules.
- Prioritize issues that affect correctness, security and privacy, data integrity,
  contracts, and test confidence. Describe a concrete failure scenario (the input, state,
  or sequence that breaks) and a direction for the fix.
- Skip formatting and style nits that a configured formatter or linter already enforces.
  Do not request broad rewrites unless the diff introduces a real risk.
- Call out verification gaps: changed behavior that no test, check, or documented manual
  step exercises.

## What to check

- **Correctness:** edge cases (empty or missing data, partial failures, unexpected
  states); existing behavior preserved unless the change intends otherwise; explicit
  date, timezone, currency, and unit handling.
- **Error handling:** failures surface at the right boundary; errors are not swallowed
  silently; retries, fallbacks, and defaults do not hide data corruption or user-visible
  failure; user-facing messages are accurate.
- **Security and authorization:** sensitive operations are authorized; inputs are
  validated before database, shell, template, or API use; secrets and tokens are never
  logged, committed, or returned to clients; trust boundaries are not widened by new
  network calls, file access, or dependencies.
- **Privacy and health data (PHI/PII):** Mindbloom handles patient health information.
  Flag any change that sends patient identifiers, contact details, clinical or treatment
  data, or free-form user input to logs, analytics, monitoring, error reports, URLs, or
  third parties, or that widens who can read it. Prefer data minimization and the
  redaction patterns already used in the repository.
- **Performance:** N+1 or unbounded queries and loops, unpaginated requests, repeated
  expensive work, unnecessary rerenders or bundle growth.
- **Concurrency and state:** races, duplicate submissions, retry behavior, idempotency,
  and partial writes.
- **Contracts and compatibility:** API, event, schema, and package-interface changes stay
  backwards-compatible, or every caller is updated; validation and serialization match
  the contract.
- **Tests:** changed behavior and risky edge cases are covered; tests assert observable
  behavior rather than mock calls; missing tests are called out when the risk justifies
  them.
- **Maintainability:** existing naming, layering, and module boundaries are followed; no
  dead code or stale comments; new abstractions remove real duplication or complexity.
- **Dependencies:** new packages are justified and maintained; version and lockfile
  changes are intentional; license and runtime footprint are acceptable.

## Repository-specific rules

This repository is a small Flask mock API (`app.py`) used for the growth engineering
interview exercise. It serves synthetic data only and stores nothing.

- **The API shape is the exercise contract:** `GET /availability` returns
  `{"appointments": [{"id", "starts_at"}]}` with randomized US/Pacific times, and
  `POST /reserve` validates `name`, `email`, `phone`, and `appointment_id` (a UUID),
  returns `409` when `?conflict=true`, and reports failures as `{"error": ...}`. Flag
  changes to routes, fields, status codes, or error shapes unless they are clearly
  intentional and reflected in `test_app.py`.
- **Synthetic data only:** flag any change that persists or logs submitted names, emails,
  or phone numbers, calls real Mindbloom services, or introduces real patient data or
  credentials.
- **CORS:** CORS is enabled for the whole app via `flask-cors`. Keep that consistent with
  the API serving only synthetic data.
- **Tests:** `./run_tests` runs `python -m unittest discover .`. Validation and
  status-code changes should be covered in `test_app.py`.
- **Deployment and dependencies:** the `Procfile` runs `gunicorn app:app`, and
  `requirements.txt` pins versions. Dependency changes should be intentional and keep the
  exercise lightweight.

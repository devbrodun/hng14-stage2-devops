# FIXES.md — Bug Report

All bugs found in the starter repo `chukwukelu2023/hng14-stage2-devops`, with
file path, line number, description of the problem, and what was changed.

---

## Fix 1

- **File:** `api/main.py`
- **Line:** 8
- **Problem:** `redis.Redis(host="localhost", ...)` — hardcoded to `localhost`.
  Inside Docker, the Redis container is reachable by its Compose service name
  (`redis`), not `localhost`. `localhost` inside the API container refers to the
  API container itself, so every Redis call would raise a `ConnectionRefusedError`.
- **Fix:** Changed to `host=os.environ.get("REDIS_HOST", "redis")`.

---

## Fix 2

- **File:** `api/main.py`
- **Line:** 8
- **Problem:** The `.env` file committed to the repo set `REDIS_PASSWORD`, but
  the `redis.Redis(...)` constructor had no `password=` argument. Any Redis
  instance started with `requirepass` would reject every connection from the API
  with an `NOAUTH` error.
- **Fix:** Added `password=os.environ.get("REDIS_PASSWORD", None)` to the
  `redis.Redis()` call.

---

## Fix 3

- **File:** `api/main.py`
- **Line:** (missing — endpoint did not exist)
- **Problem:** No `/health` HTTP endpoint existed. The Docker `HEALTHCHECK`
  instruction and `docker-compose.yml`'s `depends_on: condition: service_healthy`
  both require a working health check. Without it, the API container never
  transitions to the `healthy` state and all dependent services (worker, frontend)
  hang indefinitely at startup.
- **Fix:** Added `GET /health` that calls `r.ping()` and returns `{"status": "ok"}`.

---

## Fix 4

- **File:** `api/main.py` line 12 vs `worker/worker.py` line 20
- **Problem:** The API pushed jobs onto a Redis list key called `"job"` (singular)
  with `r.lpush("job", job_id)`, while the worker popped from `"jobs"` (plural)
  with `r.brpop("jobs", ...)`. The two services were writing to and reading from
  completely different keys — jobs were submitted and stored but the worker never
  saw them. Status would remain `"queued"` forever.
- **Fix:** Standardised both to use `"jobs"`.

---

## Fix 5

- **File:** `worker/worker.py`
- **Line:** 5
- **Problem:** Same `localhost` Redis hardcoding as the API. Same root cause:
  the worker container cannot reach Redis via `localhost`.
- **Fix:** Changed to `host=os.environ.get("REDIS_HOST", "redis")`.

---

## Fix 6

- **File:** `worker/worker.py`
- **Line:** 5
- **Problem:** `REDIS_PASSWORD` was never read or passed to the Redis client in
  the worker — same issue as Fix 2, causing `NOAUTH` errors.
- **Fix:** Added `password=os.environ.get("REDIS_PASSWORD", None)`.

---

## Fix 7

- **File:** `worker/worker.py`
- **Line:** (missing — no signal handling existed)
- **Problem:** The worker had no `SIGTERM` handler. When Docker stops the
  container (`docker stop`), it sends `SIGTERM`. Python's default response is to
  raise `SystemExit` immediately — a job being processed mid-flight is abandoned
  and its status stays `"queued"` forever, leaving the queue in an inconsistent
  state.
- **Fix:** Added `signal.signal(SIGTERM, handle_signal)` and `signal.signal(SIGINT,
  handle_signal)` with a `shutdown` flag, so the worker finishes its current job
  cleanly before exiting.

---

## Fix 8

- **File:** `frontend/app.js`
- **Line:** 6
- **Problem:** `API_URL = "http://localhost:8000"` — same container networking
  problem. The frontend container cannot reach the API container via `localhost`.
- **Fix:** Changed to `const API_URL = process.env.API_URL || 'http://api:8000'`.

---

## Fix 9

- **File:** `frontend/app.js`
- **Line:** (missing — endpoint did not exist)
- **Problem:** No `/health` endpoint, so the frontend container's `HEALTHCHECK`
  would always fail, preventing `depends_on: condition: service_healthy` from
  working.
- **Fix:** Added `app.get('/health', (req, res) => res.json({ status: 'ok' }))`.

---

## Fix 10

- **File:** `api/requirements.txt`, `worker/requirements.txt`
- **Line:** All lines
- **Problem:** No version pins on any packages (`fastapi`, `uvicorn`, `redis`).
  Unpinned dependencies make builds non-reproducible — a breaking change in any
  upstream package will silently break a future build with no code change.
- **Fix:** Pinned all packages to specific tested versions
  (`fastapi==0.111.0`, `uvicorn[standard]==0.29.0`, `redis==5.0.4`).

---

## Fix 11

- **File:** `api/.env` (the file itself)
- **Line:** All lines
- **Problem:** A real `.env` file containing an actual Redis password
  (`REDIS_PASSWORD=supersecretpassword123`) was committed to the repository.
  Secrets in git history are permanently exposed — even after deletion, they
  remain in `git log` and are accessible to anyone who forks or clones the repo.
  This is a critical security violation.
- **Fix:** Deleted `api/.env`, added `.env` and `api/.env` to `.gitignore`,
  and created `.env.example` with placeholder values documenting all required
  variables.

---

## Fix 12 (Dockerfiles — did not exist in starter)

- **File:** `api/Dockerfile`, `worker/Dockerfile`, `frontend/Dockerfile`
- **Problem:** No Dockerfiles existed. Without them, the app cannot be
  containerised.
- **Fix:** Created production-quality Dockerfiles for all three services using
  multi-stage builds, non-root users, working `HEALTHCHECK` instructions, and no
  secrets or `.env` files copied into any image.

# Job Processing System (Frontend + API + Worker + Redis)

## Overview

This project is a distributed job processing system consisting of:

* Frontend (Node.js): Handles job submission and status tracking
* API (FastAPI): Manages job creation and status retrieval
* Worker (Python): Processes jobs asynchronously
* Redis: Acts as the shared queue and datastore

---

## Prerequisites

Ensure the following are installed:

* Docker (>= 24.x)
* Docker Compose (>= v2)
* Git

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd <repo-folder>
```

---

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` if needed.

---

### 3. Build and Start Services

```bash
docker-compose up --build
```

---

### 4. Verify Services

Check containers:

```bash
docker ps
```

Expected:

* frontend (port 3000)
* api (port 8000 internal)
* worker
* redis

---

### 5. Test the System

Submit a job:

```bash
curl -X POST http://localhost:3000/jobs
```

Check status:

```bash
curl http://localhost:3000/jobs/<job_id>
```

---

## Expected Behavior

* Job is created successfully
* Worker processes job asynchronously
* Status updates from "pending" → "completed"

---

## Shutdown

```bash
docker-compose down
```

---

## Notes

* Redis is not exposed externally
* All services communicate via internal Docker network
* All configuration is environment-driven


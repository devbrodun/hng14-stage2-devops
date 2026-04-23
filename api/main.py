from fastapi import FastAPI
import redis
import uuid
import os

app = FastAPI()

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())

    try:
        r.lpush("job", job_id)

        r.hset(f"job:{job_id}", mapping={
            "status": "queued"
        })

        return {
            "job_id": job_id,
            "status": "queued"
        }

    except Exception as e:
        return {
            "error": "failed to create job",
            "details": str(e)
        }


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")

    if not status:
        return {
            "error": "not found",
            "job_id": job_id
        }

    return {
        "job_id": job_id,
        "status": status
    }

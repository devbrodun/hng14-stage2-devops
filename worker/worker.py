import redis
import time
import os
import signal

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

QUEUE = "job"
running = True


def shutdown(signum, frame):
    global running
    print("Shutting down worker gracefully...")
    running = False


signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)


def process_job(job_id):
    print(f"Processing job: {job_id}")

    try:
        # mark processing
        r.hset(f"job:{job_id}", "status", "processing")

        time.sleep(2)  # simulate work

        # mark completed
        r.hset(f"job:{job_id}", "status", "completed")

        print(f"Done: {job_id}")

    except Exception as e:
        print(f"Job failed: {e}")

        # mark failed state
        r.hset(f"job:{job_id}", "status", "failed")


print("Worker started... waiting for jobs")

while running:
    try:
        job = r.brpop(QUEUE, timeout=5)

        if job:
            _, job_id = job
            process_job(job_id)

    except redis.exceptions.ConnectionError:
        print("Redis connection lost. Retrying...")
        time.sleep(2)

    except Exception as e:
        print(f"Unexpected error: {e}")
        time.sleep(2)

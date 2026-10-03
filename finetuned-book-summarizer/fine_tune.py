import os
import time
from openai import OpenAI

client = OpenAI()
training_file_path = os.getenv("TRAINING_FILE", "data/train.jsonl")

with open(training_file_path, "rb") as file:
    uploaded = client.files.create(file=file, purpose="fine-tune")

job = client.fine_tuning.jobs.create(
    training_file=uploaded.id,
    model=os.getenv("BASE_MODEL", "gpt-3.5-turbo"),
)

while job.status not in {"succeeded", "failed", "cancelled"}:
    print(job.status)
    time.sleep(5)
    job = client.fine_tuning.jobs.retrieve(job.id)

print(job.status)
if job.status != "succeeded":
    raise RuntimeError(f"Fine-tune did not succeed: {job.status}")

print(f"CUSTOM_MODEL_ID={job.fine_tuned_model}")

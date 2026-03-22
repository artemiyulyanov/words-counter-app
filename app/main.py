from fastapi import FastAPI, UploadFile
from uuid import uuid4
from app.tasks import process_file_task
from app.infrastructure.s3 import S3Service
from celery.result import AsyncResult
from app.tasks import celery

app = FastAPI()
s3 = S3Service()

@app.post("/public/report/export")
async def export(file: UploadFile):
    key = f"uploads/{uuid4()}.txt"

    # сразу в S3 (без сохранения на диск)
    s3.upload_fileobj(file.file, key)

    task = process_file_task.delay(key)

    return {"task_id": task.id}


@app.get("/tasks/{task_id}")
def get_status(task_id: str):
    task = AsyncResult(task_id, app=celery)

    if task.status == "SUCCESS":
        result_key = task.result
        url = s3.generate_presigned_url(result_key)

        return {
            "status": "done",
            "download_url": url
        }

    return {"status": task.status}
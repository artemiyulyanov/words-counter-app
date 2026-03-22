import os

from celery import Celery
from uuid import uuid4
from app.infrastructure.s3 import S3Service
from app.infrastructure.normalizer import MorphNormalizer
from app.infrastructure.excel import ExcelExporter
from app.utils.process_file import ProcessFileUtil

import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL")

celery = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

@celery.task
def process_file_task(input_key: str):
    s3 = S3Service()

    local_input = f"/tmp/{uuid4()}.txt"
    local_output = f"/tmp/{uuid4()}.xlsx"

    s3.download_file(input_key, local_input)

    file_processor = ProcessFileUtil(
        MorphNormalizer(),
        ExcelExporter()
    )
    file_processor.execute(local_input, local_output)

    output_key = f"results/{uuid4()}.xlsx"
    with open(local_output, "rb") as f:
        s3.upload_fileobj(f, output_key)

    return output_key
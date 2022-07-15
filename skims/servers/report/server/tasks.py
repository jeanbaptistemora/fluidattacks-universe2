from .celery import app


@app.task(serializer="json", name="process-skims-result")
def hello(task_id: str) -> str:
    return f"process execution {task_id}"

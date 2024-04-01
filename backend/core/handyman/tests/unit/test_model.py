import pytest
from core.handyman.domain import model as mdl

def test_task_create(seed_task):
    task: mdl.Task = seed_task()

    assert task.status == mdl.TaskStatus.PENDING


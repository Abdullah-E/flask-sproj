from datetime import datetime
from uuid import uuid4
import pytest
from core.entrypoint.uow import FakeUnitOfWork, UnitOfWork
from core.handyman.domain import model as mdl


def test_handyman_repository(seed_handyman):
    for uow in [UnitOfWork(), FakeUnitOfWork()]:
        handyman: mdl.Handyman = seed_handyman()
        if uow.__class__.__name__ == "UnitOfWork":
            uow.cursor.execute(
                "alter table handymen drop constraint handymen_user_id_fkey cascade;"
            )
        with pytest.raises(Exception, match="Handyman not found."):
            uow.handymen.get(user_id=str(uuid4()))

        uow.handymen.add(handyman=handyman)
        fetched_handyman: mdl.Handyman = uow.handymen.get(user_id=handyman.user_id)

        assert fetched_handyman == handyman

        handyman.address = "New Address"
        handyman.category = mdl.HandymanCategory.ELECTRICIAN
        handyman.sub_categories.update([mdl.ElectricianCategory.WIRING, mdl.ElectricianCategory.UPS_INSTALLATION])
        handyman.about = "New About"
        handyman.status = True

        uow.handymen.save(handyman=handyman)
        fetched_handyman = uow.handymen.get(user_id=handyman.user_id)

        assert fetched_handyman == handyman

def test_task_repository(seed_task):
    for uow in [UnitOfWork(), FakeUnitOfWork()]:
        task: mdl.Task = seed_task()
        if uow.__class__.__name__ == "UnitOfWork":
            uow.cursor.execute(
                "alter table tasks drop constraint tasks_user_id_fkey cascade;"
            )
            uow.cursor.execute(
                "alter table tasks drop constraint tasks_handyman_id_fkey cascade;"
            )
        with pytest.raises(Exception, match="Task not found."):
            uow.tasks.get(task_id=str(uuid4()))

        uow.tasks.add(task=task)
        fetched_task: mdl.Task = uow.tasks.get(task_id=task.id)

        assert fetched_task == task

        task.address = "New Address"
        task.category = mdl.HandymanCategory.ELECTRICIAN
        task.description = "New Description"
        task.budget = 1000
        task.duration = 2
        task.date = datetime.now()
        task.time = datetime.now()
        task.status = mdl.TaskStatus.COMPLETED
        task.sub_categories.update([mdl.ElectricianCategory.WIRING, mdl.ElectricianCategory.UPS_INSTALLATION])

        uow.tasks.save(task=task)
        fetched_task = uow.tasks.get(task_id=task.id)

        assert fetched_task == task
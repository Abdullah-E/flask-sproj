from datetime import datetime
from uuid import uuid4

import pytest
from core.entrypoint.uow import FakeUnitOfWork, UnitOfWork
from core.authentication.adapters import repository as repo
from core.authentication.domain import model as mdl


def test_user_repository(seed_user):
    user: mdl.User = seed_user()

    for uow in [UnitOfWork(), FakeUnitOfWork()]:
        with pytest.raises(Exception, match="User not found."):
            uow.users.get(user_id=str(uuid4()))

        uow.users.add(user=user)
        fetched_user: mdl.User = uow.users.get(user_id=user.id)

        assert fetched_user == user

        user.cnic = "1234567890123"
        user.email = "24100163@lums.edu.pk"
        user.first_name = "Malik"
        user.last_name = "Ammar"
        user.gender = mdl.Gender.OTHER

        uow.users.save(user=user)
        fetched_user: mdl.User = uow.users.get(user_id=user.id)

        assert fetched_user == user

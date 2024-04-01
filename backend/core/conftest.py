import os
from uuid import uuid4
import pytest
from datetime import datetime
from core.authentication.domain import model as auth_mdl
from core.handyman.domain import model as handy_mdl

@pytest.fixture
def seed_user():
    def _seed_user() -> auth_mdl.User:
        return auth_mdl.User(
            id=str(uuid4()),
            first_name="Malik",
            last_name="Moaz",
            cnic="6110171505115",
            gender=auth_mdl.Gender.MALE,
            phone_number="03034952255",
            email="mlkmoaz@gmail.com",
            otp="1234",
            phone_number_verified=False,
        )
    return _seed_user

@pytest.fixture
def seed_handyman():
    def _seed_handyman() -> handy_mdl.Handyman:
        return handy_mdl.Handyman(
            id=str(uuid4()),
            user_id=str(uuid4()),
            category=handy_mdl.HandymanCategory.PLUMBER,
            sub_categories=set([handy_mdl.PlumberCategory.WATER_LINE_REPAIR, handy_mdl.PlumberCategory.DRAIN_CLEANING]),
            about="I am a plumber",
            address="Lahore",
            status=False,
        )
    return _seed_handyman

@pytest.fixture
def seed_task():
    def _seed_task() -> handy_mdl.Task:
        return handy_mdl.Task(
            id=str(uuid4()),
            user_id=str(uuid4()),
            handyman_id=str(uuid4()),
            category=handy_mdl.HandymanCategory.PLUMBER,
            sub_categories=set([handy_mdl.PlumberCategory.WATER_LINE_REPAIR, handy_mdl.PlumberCategory.DRAIN_CLEANING]),
            description="Water line repair",
            address="Lahore",
            budget=500,
            duration=1,
            date=datetime.now(),
            time=datetime.now(),
            status=handy_mdl.TaskStatus.PENDING,
        )
    return _seed_task
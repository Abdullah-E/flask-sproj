"""Commands for the authentication entrypoint."""
from typing import Optional, Tuple

from core.authentication.domain import model as auth_mdl
from core.entrypoint.uow import AbstractUnitOfWork
from uuid import NAMESPACE_OID, uuid5
import firebase_admin
import firebase_admin
from random import randint

from firebase_admin import auth


def create_user(
    phone_number: str,
    email: str,
    password: str,
    uow: AbstractUnitOfWork,
):
    user_created = bool()
    firebase_uuid = str()

    try:
        user_record = firebase_admin.auth.create_user(
            email=email,
            email_verified=False,
            phone_number=phone_number,
            password=password,
            disabled=False,
        )
        firebase_uuid = user_record.uid
        user_created = True
    except Exception as e:
        raise e

    if user_created:
        uuid = str(uuid5(NAMESPACE_OID, firebase_uuid))
        user = auth_mdl.User(
            id=uuid,
            phone_number=phone_number,
            email=email,
            services=[],
            first_name=None,
            last_name=None,
            cnic=None,
            gender=auth_mdl.Gender.OTHER,
            otp=str(randint(1000, 9999)),
        )
        uow.users.add(user)
    else:
        # firebase_uuid = str(uuid5(NAMESPACE_OID, firebase_uuid))
        firebase_admin.auth.delete_users([firebase_uuid])

    # if user already exists, send otp

    # else delete user from firebase and send error

    return 201, uuid, True


def update_user(
    user_id: str,
    user_info: dict,
    uow: AbstractUnitOfWork,
):
    user = uow.users.get(user_id=user_id)
    user.update_user(user_info=user_info)
    uow.users.save(user=user)
    return 200, user, True

"""Handyman Specific API Endpoints"""

from flask import Blueprint, request
from core.entrypoint.uow import UnitOfWork
from core.api import utils
from uuid import uuid4
from datetime import datetime
from core.authentication.entrypoint import commands as auth_cmd
from core.handyman.entrypoint import commands as handy_cmd
from core.handyman.domain import model as handy_mdl
from core.handyman.entrypoint import queries as handy_qry

handyman = Blueprint("handyman", __name__, url_prefix="/api/v1")


@handyman.route("/create-user", methods=["POST"])
@utils.handle_missing_payload
def create_user():
    """Create a new user account"""
    req = request.get_json(force=True)
    uow = UnitOfWork()
    try:
        _, uuid, _ = auth_cmd.create_user(
            phone_number=req["phone_number"],
            email=req["email"],
            password=req["password"],
            uow=uow,
        )
        uow.commit_close_connection()
    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="User created successfully",
        status_code=201,
        data=uuid
    ).__dict__

@handyman.route("/create-handyman", methods=["POST"])
@utils.handle_missing_payload
def create_update_handyman():
    """Create/Update a handyman account"""
    req = request.get_json(force=True)
    uow = UnitOfWork()
    try:
        handy_cmd.create_handyman(
            id=str(uuid4()),
            user_id=req["uid"],
            category=req["category"],
            sub_categories=req["sub_categories"],
            about=req["about"],
            address=req["address"],
            status=False,
            uow=uow,
        )
        uow.commit_close_connection()
    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="Handyman created successfully",
        status_code=201,
    ).__dict__

@handyman.route("/update-user", methods=["POST"])
# @utils.authenticate_token
def update_user():
    """Update User"""
    req = request.get_json(force=True)
    uow = UnitOfWork()
    try:
        auth_cmd.update_user(
            user_id=req["uid"],
            user_info=req["user_info"],
            uow=uow,
        )
        uow.commit_close_connection()
    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="User updated successfully",
        status_code=201,
    ).__dict__


@handyman.route("/get-user", methods=["GET"])
# @utils.authenticate_token
def get_user():
    """Get User"""
    uow = UnitOfWork()
    user_id = request.args.get('uid')
    try:
        user = uow.users.get(user_id=user_id)
        uow.close_connection()
    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="User returned successfully",
        status_code=201,
        data=user,
    ).__dict__

@handyman.route("/get-handyman", methods=["GET"])
# @utils.authenticate_token
def get_handyman():
    """Get Handyman"""
    uow = UnitOfWork()
    user_id = request.args.get('uid')
    print(user_id)
    try:
        handyman = handy_qry.get_handyman(user_id=user_id, uow=uow)
        uow.close_connection()
    except Exception as e:
        uow.close_connection()
        raise e
    
    return utils.Response(
        message="Handyman returned successfully",
        status_code=201,
        data=handyman,
    ).__dict__

@handyman.route("update-handyman", methods=["POST"])
# @utils.authenticate_token
def update_handyman():
    """Update Handyman"""
    req = request.get_json(force=True)
    uow = UnitOfWork()
    try:
        handy_cmd.update_handyman(
            user_id=req["uid"],
            handyman_info=req["handyman_info"],
            uow=uow,
        )
        uow.commit_close_connection()
    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="Handyman updated successfully",
        status_code=201,
    ).__dict__

@handyman.route("/get-task-categories", methods=["GET"])
# @utils.authenticate_token
def get_task_categories():
    """get all closed loops"""

    uow = UnitOfWork()
    categories = handy_qry.get_handyman_categories(uow=uow)
    uow.close_connection()

    return utils.Response(
        message="All categories returned successfully",
        status_code=201,
        data=categories,
    ).__dict__


@handyman.route("/create-task", methods=["POST"])
# @utils.authenticate_token
def create_task():
    """Create a new task"""
    req = request.get_json(force=True)
    uow = UnitOfWork()
    try:
        handy_cmd.create_task(
            id=str(uuid4()),
            user_id=req["uid"],
            category=req["category"],
            sub_categories=req["sub_categories"],
            description=req["description"],
            address=req["address"],
            budget=req["budget"],
            duration=req["duration"],
            date=datetime.now(),
            time=datetime.now(),
            status=handy_mdl.TaskStatus.PENDING,
            uow=uow,
        )
        uow.commit_close_connection()
    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="Task created successfully",
        status_code=201,
    ).__dict__

@handyman.route("/get-relevant-available-tasks", methods=["GET"])
# @utils.authenticate_token
def get_relevant_available_tasks():
    """get all closed loops"""

    uow = UnitOfWork()
    tasks = handy_qry.get_relevant_available_tasks(uow=uow)
    uow.close_connection()

    return utils.Response(
        message="All relevant available tasks returned successfully",
        status_code=201,
        data=tasks,
    ).__dict__

@handyman.route("/get-handyman-subcategories", methods=["GET"])
# @utils.authenticate_token
def get_handyman_subcategories():
    """get all closed loops"""

    uow = UnitOfWork()
    sub_cat = request.args.get('sub_cat')
    categories = handy_qry.get_handyman_subcategories(sub_cat, uow=uow)
    uow.close_connection()

    return utils.Response(
        message="All sub-categories returned successfully",
        status_code=201,
        data=categories,
    ).__dict__



"""Commands for the handypam entrypoint."""
from typing import Optional, Tuple
from typing import List, Set
from random import randint
from datetime import datetime
from core.entrypoint.uow import AbstractUnitOfWork
from core.handyman.domain import model as handy_mdl
from core.handyman.adapters.utils import map_subcategories_from_string

def create_handyman(
        id: str,
        user_id: str,
        category: handy_mdl.HandymanCategory,
        sub_categories: List[str],
        about: str,
        address: str,
        status: bool,
        uow: AbstractUnitOfWork,
) -> handy_mdl.Handyman:
    """create handyman command"""
    category = handy_mdl.HandymanCategory[category]
    subs = sub_categories.split(',')
    subs = map_subcategories_from_string(category, subs)

    handyman =  handy_mdl.Handyman(
        id=id,
        user_id=user_id,
        category=category,
        sub_categories=subs,
        about=about,
        address=address,
        status=status,
    )

    uow.handymen.add(handyman)

def update_handyman(
    user_id: str,
    handyman_info: dict,
    uow: AbstractUnitOfWork,
):
    handyman = uow.handymen.get(user_id=user_id)
    handyman.update_handyman(handyman_info=handyman_info)
    uow.handymen.save(handyman=handyman)
    return 200, handyman, True

def create_task(
        id: str,
        user_id: str,
        category: handy_mdl.HandymanCategory,
        sub_categories: List[str],
        description: str,
        address: str,
        budget: int,
        duration: int,
        date: datetime,
        time: datetime,
        status: handy_mdl.TaskStatus,
        uow: AbstractUnitOfWork,
):
    """create task command"""

    category = handy_mdl.HandymanCategory[category]
    subs = sub_categories.split(',')
    subs = map_subcategories_from_string(category, subs)

    task = handy_mdl.Task(
        id=id,
        user_id=user_id,
        handyman_id=None,
        category=category,
        sub_categories=subs,
        description=description,
        address=address,
        budget=budget,
        duration=duration,
        date=date,
        time=time,
        status=status,
    )

    uow.tasks.add(task)


#def create(
#    id: str,
#    status: mdl.EventStatus,
#    registrations: Dict[str, mdl.Registration],
#    cancellation_reason: str,
#    name: str,
#    organizer_id: str,
#    venue: str,
#    capacity: int,
#    description: str,
#    image_url: str,
#    closed_loop_id: str,
#    event_start_timestamp: datetime,
#    event_end_timestamp: datetime,
#    registration_start_timestamp: datetime,
#    registration_end_timestamp: datetime,
#    registration_fee: int,
#    uow: AbstractUnitOfWork,
#    auth_acl: acl.AbstractAuthenticationService,
#):
#    """Create event command"""
#    if not auth_acl.is_organizer(id=organizer_id, uow=uow):
#        raise exc.EventNotCreatedByOrganizer("Only organizers can create an event")

#    if not auth_acl.is_valid_closed_loop(id=closed_loop_id, uow=uow):
#        raise exc.ClosedLoopDoesNotExist("The closed loop doesn't exist")

#    event = mdl.Event(
#        id=id,
#        status=status,
#        registrations=registrations,
#        cancellation_reason=cancellation_reason,
#        name=name,
#        organizer_id=organizer_id,
#        venue=venue,
#        capacity=capacity,
#        description=description,
#        image_url=image_url,
#        closed_loop_id=closed_loop_id,
#        event_start_timestamp=event_start_timestamp,
#        event_end_timestamp=event_end_timestamp,
#        registration_start_timestamp=registration_start_timestamp,
#        registration_end_timestamp=registration_end_timestamp,
#        registration_fee=registration_fee,
#        event_form_schema={"fields":[]}
#    )
#    uow.events.add(event)
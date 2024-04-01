"""
Handyman Domain Model
- Define Handyman Categories
- Create Tasks
"""
from random import randint
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Tuple, Set, List
from uuid import uuid4


class HandymanCategory(str, Enum):
    """Handyman Category Enum"""
    PLUMBER = 1
    ELECTRICIAN = 2
    CARPENTER = 3
    PAINTER = 4
    TAILOR = 5
    SHIFTING = 6
    COOK = 7
    MASON = 8
    HVAC = 9
    VEHICLE_MECHANIC = 10
    VEHICLE_ELECTRICIAN = 11
    HOUSE_HELP = 12
    CAR_WASHER = 13
    DRIVERS = 14
    BABYSITTERS = 15
    DOCTORS = 16
    REAL_ESTATE_AGENTS = 17


class PlumberCategory(str, Enum):
    """Plumber Category Enum"""
    WATER_LINE_REPAIR = 1
    DRAIN_CLEANING = 2
    WATER_TANK_INSTALLATION = 3
    FAUCET_INSTALLATION = 4


class ElectricianCategory(str, Enum):
    """Electrician Category Enum"""
    WIRING = 1
    UPS_INSTALLATION = 2
    SOLAR_PANEL_INSTALLATION = 3
    BREAKER_BOX_INSTALLATION = 4


class CarpenterCategory(str, Enum):
    """Carpenter Category Enum"""
    FURNITURE_REPAIR = 1
    FURNITURE_INSTALLATION = 2
    DOOR_REPAIR = 3
    DOOR_INSTALLATION = 4


class PainterCategory(str, Enum):
    """Painter Category Enum"""
    WALL_PAINTING = 1
    FURNITURE_PAINTING = 2
    WALLPAPER_INSTALLATION = 3
    WALLPAPER_REMOVAL = 4

@dataclass
class Handyman():
    """Handyman can perform tasks"""
    id: str
    user_id: str
    category: HandymanCategory
    sub_categories: Set
    about: str
    address: str
    status: bool

    def update_handyman(self, handyman_info: Dict) -> None:
        """Update Handyman Attributes"""
        for key, value in handyman_info.items():
            if hasattr(self, key):
                setattr(self, key, value)

class TaskStatus(str, Enum):
    """Task Status Enum"""
    PENDING = 1
    ACCEPTED = 2
    COMPLETED = 3
    CANCELLED = 4


@dataclass
class Task():
    """Task Entity"""
    id: str
    user_id: str
    handyman_id: str
    category: HandymanCategory
    sub_categories: Set
    description: str
    address: str
    budget: int
    duration: int
    date: datetime
    time: datetime
    status: TaskStatus

    def create_task(self) -> None:
        """Create Task"""
        self.status = TaskStatus.PENDING

    def cancel_task(self) -> None:
        """Cancel Task"""
        pass

    def accept_task(self) -> None:
        """Accept Task"""
        pass

    def complete_task(self) -> None:
        """Complete Task"""
        pass


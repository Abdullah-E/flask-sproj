from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from psycopg2.extras import DictRow


@dataclass(frozen=True)
class HandymanCategoriesDTO:
    name: str

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "HandymanCategoriesDTO":
        print(row)
        return HandymanCategoriesDTO(
            name=row[0],
        )
    
@dataclass(frozen=True)
class TaskDTO:
    id: str
    user_id: str
    handyman_id: str
    category: str
    sub_categories: str
    description: str
    address: str
    budget: int
    duration: int
    date: datetime
    time: datetime
    status: str
    handyman_name: str

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "TaskDTO":
        return TaskDTO(
            id=row["id"],
            user_id=row["user_id"],
            handyman_id=row["handyman_id"],
            category=row["category"],
            sub_categories=row["sub_categories"],
            description=row["description"],
            address=row["address"],
            budget=row["budget"],
            duration=row["duration"],
            date=row["date"],
            time=row["time"],
            status=row["status"],
            handyman_name=row["handyman_name"],
        )

@dataclass(frozen=True)
class HandymanDTO:
    id: str
    user_id: str
    category: str
    sub_categories: str
    about: str
    address: str
    status: bool

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "HandymanDTO":
        return HandymanDTO(
            id=row["id"],
            user_id=row["user_id"],
            category=row["category"],
            sub_categories=row["sub_categories"],
            about=row["about"],
            address=row["address"],
            status=row["status"],
        )

    
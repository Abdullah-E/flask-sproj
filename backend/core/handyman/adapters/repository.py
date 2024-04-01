from abc import ABC, abstractmethod
from typing import Dict, List
from psycopg2.extensions import cursor, connection
from psycopg2.extras import DictCursor
from core.handyman.domain import model as mdl
from core.handyman.adapters.utils import map_subcategories

class HandymanAbstractRepository(ABC):
    """Task Abstract Repository"""

    @abstractmethod
    def add(self, handyman: mdl.Handyman) -> None:
        pass

    @abstractmethod
    def get(self, user_id: str) -> mdl.Handyman:
        pass

    @abstractmethod
    def save(self, handyman: mdl.Handyman) -> None:
        pass

class TaskAbstractRepository(ABC):
    """Task Abstract Repository"""

    @abstractmethod
    def add(self, task: mdl.Task) -> None:
        pass

    @abstractmethod
    def get(self, user_id: str) -> mdl.Task:
        pass

    @abstractmethod
    def save(self, task: mdl.Task) -> None:
        pass

class FakeHandymanRepository(HandymanAbstractRepository):
    """Handyman Fake Repository"""

    def __init__(self):
        self.handymen: Dict[str, mdl.Handyman] = {}

    def add(self, handyman: mdl.Handyman) -> None:
        self.handymen[handyman.user_id] = handyman

    def get(self, user_id: str) -> mdl.Handyman:
        if user_id not in self.handymen:
            raise Exception("Handyman not found.")
        return self.handymen[user_id]
    
    def save(self, handyman: mdl.Handyman) -> None:
        self.handymen[handyman.user_id] = handyman  

class FakeTaskRepository(TaskAbstractRepository):
    """Task Fake Repository"""

    def __init__(self):
        self.tasks: Dict[str, mdl.Task] = {}

    def add(self, task: mdl.Task) -> None:
        self.tasks[task.id] = task

    def get(self, task_id: str) -> mdl.Task:
        if task_id not in self.tasks:
            raise Exception("Task not found.")
        return self.tasks[task_id]
    
    def save(self, task: mdl.Task) -> None:
        self.tasks[task.id] = task  

class HandymanRepository(HandymanAbstractRepository):
    """Handyman Repository"""

    def __init__(self, connection: connection):
        self.connection = connection
        self.cursor: cursor = connection.cursor(cursor_factory=DictCursor)

    def add(self, handyman: mdl.Handyman) -> None:
        sql = """
            INSERT INTO handymen (id, user_id, category, sub_categories, about, address, status)
            VALUES (%(id)s, %(user_id)s, %(category)s, %(sub_categories)s, %(about)s, %(address)s, %(status)s)
        """ 
        
        sub_categories = sorted(handyman.sub_categories) # convert sub categories to list

        self.cursor.execute(
            sql,
            {
                "id": handyman.id,
                "user_id": handyman.user_id,
                "category": handyman.category.name,
                "sub_categories": sub_categories,
                "about": handyman.about,
                "address": handyman.address,
                "status": handyman.status
            },
        )

    def get(self, user_id: str) -> mdl.Handyman:
        sql = """
            SELECT id, user_id, category, sub_categories, about, address, status
            FROM handymen
            WHERE user_id = %(user_id)s
        """

        self.cursor.execute(sql, {"user_id": user_id})
        handyman_row = self.cursor.fetchone()

        if handyman_row is None:
            raise Exception("Handyman not found.")

        category = mdl.HandymanCategory[handyman_row["category"]]
        sub_categories = handyman_row["sub_categories"]

        sub_categories_from_model = map_subcategories(category, sub_categories)
    
        return mdl.Handyman(
            id=handyman_row["id"],
            user_id=handyman_row["user_id"],
            category=mdl.HandymanCategory[handyman_row["category"]],
            sub_categories=set(sub_categories_from_model),
            about=handyman_row["about"],
            address=handyman_row["address"],
            status=handyman_row["status"],
        )
    
    def save(self, handyman: mdl.Handyman) -> None:
        sql = """
            INSERT INTO handymen (id, user_id, category, sub_categories, about, address, status)
            VALUES (%(id)s, %(user_id)s, %(category)s, %(sub_categories)s, %(about)s, %(address)s, %(status)s)
            ON CONFLICT(id) DO UPDATE SET
                id = excluded.id,
                user_id = excluded.user_id,
                category = excluded.category,
                sub_categories = excluded.sub_categories,
                about = excluded.about,
                address = excluded.address,
                status = excluded.status
        """ 
        
        sub_categories = sorted(handyman.sub_categories)

        self.cursor.execute(
            sql,
            {
                "id": handyman.id,
                "user_id": handyman.user_id,
                "category": handyman.category.name,
                "sub_categories": sub_categories,
                "about": handyman.about,
                "address": handyman.address,
                "status": handyman.status
            },
        )

class TaskRepository(TaskAbstractRepository):
    """Task Repository"""

    def __init__(self, connection: connection):
        self.connection = connection
        self.cursor: cursor = connection.cursor(cursor_factory=DictCursor)

    def add(self, task: mdl.Task) -> None:
        sql = """
            INSERT INTO tasks (id, user_id, handyman_id, category, sub_categories, description, address, budget, duration, date, time, status)
            VALUES (%(id)s, %(user_id)s, %(handyman_id)s, %(category)s, %(sub_categories)s, %(description)s, %(address)s, %(budget)s, %(duration)s, %(date)s, %(time)s, %(status)s)
        """ 
        
        sub_categories = sorted(task.sub_categories) # convert sub categories to list

        self.cursor.execute(
            sql,
            {
                "id": task.id,
                "user_id": task.user_id,
                "handyman_id": task.handyman_id,
                "category": task.category.name,
                "sub_categories": sub_categories,
                "description": task.description,
                "address": task.address,
                "budget": task.budget,
                "duration": task.duration,
                "date": task.date,
                "time": task.time,
                "status": task.status.name
            },
        )

    def get(self, task_id: str) -> mdl.Task:
        sql = """
            SELECT id, user_id, handyman_id, category, sub_categories, description, address, budget, duration, date, time, status
            FROM TASKS
            WHERE id = %(id)s
        """

        self.cursor.execute(sql, {"id": task_id})
        task_row = self.cursor.fetchone()

        if task_row is None:
            raise Exception("Task not found.")
        
        category = mdl.HandymanCategory[task_row["category"]]
        sub_categories = task_row["sub_categories"]

        sub_categories_from_model = map_subcategories(category, sub_categories)

        return mdl.Task(
            id=task_row["id"],
            user_id=task_row["user_id"],
            handyman_id=task_row["handyman_id"],
            category=mdl.HandymanCategory[task_row["category"]],
            sub_categories=set(sub_categories_from_model),
            description=task_row["description"],
            address=task_row["address"],
            budget=task_row["budget"],
            duration=task_row["duration"],
            date=task_row["date"],
            time=task_row["time"],
            status=mdl.TaskStatus[task_row["status"]],
        )

    def save(self, task: mdl.Task) -> None:
        sql = """
            INSERT INTO tasks (id, user_id, handyman_id, category, sub_categories, description, address, budget, duration, date, time, status)
            VALUES (%(id)s, %(user_id)s, %(handyman_id)s, %(category)s, %(sub_categories)s, %(description)s, %(address)s, %(budget)s, %(duration)s, %(date)s, %(time)s, %(status)s)
            ON CONFLICT(id) DO UPDATE SET
                id = excluded.id,
                user_id = excluded.user_id,
                handyman_id = excluded.handyman_id,
                category = excluded.category,
                sub_categories = excluded.sub_categories,
                description = excluded.description,
                address = excluded.address,
                budget = excluded.budget,
                duration = excluded.duration,
                date = excluded.date,
                time = excluded.time,
                status = excluded.status
        """ 
        
        sub_categories = sorted(task.sub_categories) # convert sub categories to list

        self.cursor.execute(
            sql,
            {
                "id": task.id,
                "user_id": task.user_id,
                "handyman_id": task.handyman_id,
                "category": task.category.name,
                "sub_categories": sub_categories,
                "description": task.description,
                "address": task.address,
                "budget": task.budget,
                "duration": task.duration,
                "date": task.date,
                "time": task.time,
                "status": task.status.name
            },
        )

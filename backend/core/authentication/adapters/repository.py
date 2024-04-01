"""User Repository """
from abc import ABC, abstractmethod
from typing import Dict

from core.authentication.domain import model as mdl
from psycopg2.extensions import cursor, connection
from psycopg2.extras import DictCursor


class UserAbstractRepository(ABC):
    """User Abstract Repository"""

    @abstractmethod
    def add(self, user: mdl.User) -> None:
        pass

    @abstractmethod
    def get(self, user_id: str) -> mdl.User:
        pass

    @abstractmethod
    def save(self, user: mdl.User) -> None:
        pass


class FakeUserRepository(UserAbstractRepository):
    """User Fake Repository"""

    def __init__(self):
        self.users: Dict[str, mdl.User] = {}

    def add(self, user: mdl.User) -> None:
        self.users[user.id] = user

    def get(self, user_id: str) -> mdl.User:
        if user_id not in self.users:
            raise Exception("User not found.")
        return self.users[user_id]

    def save(self, user: mdl.User) -> None:
        self.users[user.id] = user


class UserRepository(UserAbstractRepository):
    def __init__(self, connection: connection):
        self.connection = connection
        self.cursor: cursor = connection.cursor(cursor_factory=DictCursor)

    def add(self, user: mdl.User):
        sql = """
            INSERT INTO users (id, first_name, last_name, cnic, gender, phone_number, email, services, otp, phone_number_verified)
            VALUES (%(id)s, %(first_name)s, %(last_name)s, %(cnic)s, %(gender)s, %(phone_number)s, %(email)s, %(services)s, %(otp)s, %(phone_number_verified)s)
        """

        self.cursor.execute(
            sql,
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "cnic": user.cnic,
                "gender": user.gender.name,
                "phone_number": user.phone_number,
                "email": user.email,
                "services": user.services,
                "otp": user.otp,
                "phone_number_verified": user.phone_number_verified,
            },
        )

    def get(self, user_id: str) -> mdl.User:
        sql = """
            SELECT id, first_name, last_name, cnic, gender, phone_number, email, services, otp, phone_number_verified, created_at
            FROM users
            WHERE id = %(id)s
        """

        self.cursor.execute(sql, {"id": user_id})
        row = self.cursor.fetchone()

        if row is None:
            raise Exception("User not found.")
        
        print(row["services"])

        return mdl.User(
            id=row["id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            cnic=row["cnic"],
            gender=mdl.Gender[row["gender"]],
            phone_number=row["phone_number"],
            email=row["email"],
            services=row["services"],
            otp=row["otp"],
            phone_number_verified=row["phone_number_verified"],
        )
    
    def save(self, user: mdl.User):
        sql = """
            INSERT INTO users (id, first_name, last_name, cnic, gender, phone_number, email, services, otp, phone_number_verified)
            VALUES (%(id)s, %(first_name)s, %(last_name)s, %(cnic)s, %(gender)s, %(phone_number)s, %(email)s, %(services)s, %(otp)s, %(phone_number_verified)s)
            ON CONFLICT(id) DO UPDATE SET
                ID = EXCLUDED.id,
                first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name,
                cnic = EXCLUDED.cnic,
                gender = EXCLUDED.gender,
                phone_number = EXCLUDED.phone_number,
                email = EXCLUDED.email,
                services = EXCLUDED.services,
                otp = EXCLUDED.otp,
                phone_number_verified = EXCLUDED.phone_number_verified
        """

        self.cursor.execute(
            sql,
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "cnic": user.cnic,
                "gender": user.gender.name,
                "phone_number": user.phone_number,
                "email": user.email,
                "services": user.services,
                "otp": user.otp,
                "phone_number_verified": user.phone_number_verified,
            },
        )

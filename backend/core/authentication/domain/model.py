"""
Authentication Domain Model
- Create Account*
- Verify OTP
- Profile Info
    - Member Varaibles
        - ID
        - First Name
        - Last Name
        - CNIC
        - Gender
        - Phone Number*
        - Email Address*
        - Password*
        - Confirm Password*
        - OTP*
        - Phone Number Verified
    - Methods
        - VerifyOTP()*
"""
from random import randint
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Tuple, Set, List
from uuid import uuid4
from core.handyman.domain import model as handyman_model

class Gender(str, Enum):
    """Gender Enum"""
    MALE = 1
    FEMALE = 2
    OTHER = 3

@dataclass
class User():
    """User Entity"""

    id: str
    first_name: str
    last_name: str
    cnic: str
    gender: Gender
    phone_number: str
    email: str
    otp: str

    services: List[handyman_model.HandymanCategory] = field(default_factory=list)
    phone_number_verified: bool = False

    def verify_otp(self, otp: str) -> bool:
        """Verify OTP"""
        if self.otp == otp:
            self._generate_new_otp()
            return True
        raise Exception("Invalid OTP")
    
    def verify_phone_number(self, otp: str) -> None:
        """Verify Phone Number"""
        if self.phone_number_verified:
            raise Exception("Phone Number Already Verified")

        if self.verify_otp(otp):
            self.phone_number_verified = True

    def update_user(self, user_info: Dict) -> None:
        """Update User Attributes"""
        for key, value in user_info.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def _generate_new_otp(self) -> None:
        self.otp = str(randint(1000, 9999))

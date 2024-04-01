import pytest
from core.authentication.domain import model as auth_mdl

def test_verify_otp(seed_user):
    user: auth_mdl.User = seed_user()

    assert user.phone_number_verified == False

    with pytest.raises(Exception, match="Invalid OTP"):
        user.verify_phone_number("1235")

    user.verify_phone_number(user.otp) 

    assert user.phone_number_verified == True

    with pytest.raises(Exception, match="Phone Number Already Verified"):
        user.verify_phone_number(user.otp)
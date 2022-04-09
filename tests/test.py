import pytest

from accounts import serializers


class TestUserRegistration:
    @pytest.mark.django_db
    def test_create(self):
        # baker.make(models.User)
        user_registration = serializers.UserSerializer()
        test_result = user_registration.create(
            {
                "firstname": "Tests",
                "lastname": "User",
                "phonenumber": "0712345678",
                "email": "testuser@gmail.com",
                "password": "Pass1234",
            }
        )

        assert test_result.firstname == "Tests"
        assert test_result.lastname == "User"

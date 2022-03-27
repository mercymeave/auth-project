from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating users"""

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Password"},
    )

    class Meta:
        model = User
        fields = ("firstname", "lastname", "phonenumber", "email", "password")

    def create(self, validated_data, **kwargs):
        """
        Overriding the default create method of the Model serializer.
        """
        print(validated_data)
        user = User(
            email=validated_data["email"],
            firstname=validated_data["firstname"],
            lastname=validated_data["lastname"],
            phonenumber=validated_data["phonenumber"],
        )
        password = validated_data["password"]
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(LoginSerializer, self).validate(attrs)
        # Custom data include in the response
        data.update({"id": self.user.id})
        data.update({"email": self.user.email})
        data.update({"firstname": self.user.firstname})
        data.update({"lastname": self.user.lastname})
        data.update({"phonenumber": self.user.phonenumber})
        return data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class UpdateUserSerializer(serializers.ModelSerializer):
    """
    Serializer to update the information of a logged-in user
    """

    class Meta:
        model = User
        fields = ("firstname", "lastname", "phonenumber")

    def update(self, instance, validated_data):
        user = self.context["request"].user
        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        instance.firstname = validated_data["firstname"]
        instance.lastname = validated_data["lastname"]
        instance.phonenumber = validated_data["phonenumber"]
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Change the password of the user.
    Note that the user sending the request must
    be the same user whose password is to be changed
    """

    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def update(self, instance, validated_data):
        user = self.context["request"].user
        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        instance.set_password(validated_data["password"])
        instance.save()
        return instance

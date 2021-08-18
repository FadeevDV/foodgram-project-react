from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  )


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже зарегистрирован в системе'
            )
        return data


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    secret = serializers.CharField(required=True)

    def validate(self, data):
        email = data['email']
        secret = data['secret']
        if not User.objects.filter(email=email,
                                   secret=secret).exists():
            raise serializers.ValidationError('Вы отправили неверный код')
        return data

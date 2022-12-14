from rest_framework import serializers
from allauth.account.adapter import get_adapter
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from rest_auth.registration.serializers import RegisterSerializer

from .models import Member, Subscribe

# JWT 사용을 위한 설정
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

# 기본 유저 모델 불러오기
Member = get_user_model()

#회원가입
class MemberRegisterSerializer(RegisterSerializer):
    nickname=serializers.CharField(required=True, max_length=50)
    profile = serializers.CharField(required=False, max_length=200)
    profile_image = serializers.ImageField(required=False)
    
    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data() # username, password, email이 디폴트
        data_dict['nickname'] = self.validated_data.get('nickname', '')
        data_dict['profile'] = self.validated_data.get('profile', '')
        data_dict['profile_image'] = self.validated_data.get('profile_image', '')

        return data_dict

# 로그인 
class MemberLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password", None)
        # 사용자 아이디와 비밀번호로 로그인 구현(<-> 사용자 아이디 대신 이메일로도 가능)
        member = authenticate(username=username, password=password)

        if member is None:
            return {'username': 'None'}
        try:
            payload = JWT_PAYLOAD_HANDLER(member)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, member)

        except Member.DoesNotExist:
            raise serializers.ValidationError(
                'Member with given username and password does not exist'
            )

        return {
            "username": member.username,
            "token": jwt_token
        }

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = "__all__"
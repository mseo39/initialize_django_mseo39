from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# TokenObtain는 Access Token이고 다음과 같이 PAYLOAD에 담을 정보를 추가할 수 있다
"""
TokenObtainPairSerializer 사용했을 때
{
  "token_type": "access",
  "exp": 1714067315,
  "iat": 1714067135,
  "jti": "c11d7d47b24a4c608a438d2c5907704f",
  "user_id": 1
}

커스텀한거 사용했을 때
{
  "token_type": "access",
  "exp": 1714067958,
  "iat": 1714067778,
  "jti": "b79a92031b454913a7c6bdd279cbc3c9",
  "user_id": 1,
  "username": "mseo",
  "email": "mseo@naver.com"
}
"""
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    # database에서 조회된 user의 정보가 user로 들어오게 된다. (요청한 user의 정보)
    def get_token(cls, user):
		# 가지고 온 user의 정보를 바탕으로 token을 생성한다.
        token = super().get_token(user)

        # 로그인한 사용자의 클레임 설정하기.
        token['username'] = user.username
        token['email'] = user.email

        return token
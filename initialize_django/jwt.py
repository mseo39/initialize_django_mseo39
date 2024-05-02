from datetime import timedelta

# 여기서 SIGNING_KEY는 기본으로 settings.SECRET_KEY를 사용한다
# 지금은 따로 관리 안해줬지만 SECRET_KEY가 털리면 큰일나므로 따로 관리해줘야 한다
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

# jwt 토큰을 담기 위함
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'BearerAuth': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': "JWT Token"
        }
    },
    'SECURITY_REQUIREMENTS': [{
        'BearerAuth': []
    }]
}
## 회원가입
http://127.0.0.1:8000/user/session_signup
```
{
    "username" : "mseo",
    "password": 1234,
    "email" : "mseo@naver.com",
    "age":24
}
```

### session
> django에서는 session이 기본으로 적용된다고 한다. 따라서 따로 기능을 만들어 주지 않아도 된다
 * 로그인 API user/session_signin
 * 회원가입 API user/session_signup


---

### jwt
 * 로그인 API user/jwt_signin
 * 회원가입 API user/jwt_signup

---

### 비밀번호 암호화
* make_password()
  * django에서 제공하는 함수
  * PBKDF2 알고리즘
    * salt
    * 키 스트레칭
* bcrypt
    * 따로 설치해야 함
    * salt
    * 키 스트레칭
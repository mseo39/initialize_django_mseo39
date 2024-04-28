## board CRUD



### category
```
board/categories

✅ post
: header에 jwt 토큰을 함께 보내야 함
: admin 계정만 접근 가능

요청
{
    "name":"수학"
}
결과
{
    "id": 2,
    "name": "수학"
}

✅ get
: 모두 접근 가능

결과
[
    {
        "id": 1,
        "name": "수학"
    },
    {
        "id": 2,
        "name": "영어"
    },
    {
        "id": 3,
        "name": "국어"
    }
]
```

### posts
```
posts/<int:category_id>

결과
[
    {
        "id": 20,
        "title": "수업",
        "created_date": "2024-04-28",
        "modified_date": "2024-04-28T13:05:29.117421Z"
    },
    {
        "id": 21,
        "title": "수업 째고 싶어용",
        "created_date": "2024-04-28",
        "modified_date": "2024-04-28T13:05:59.141494Z"
    }
]

```

### post
: 인증된 사용자는 읽기 쓰기 모두 허용, 인증되지 않은 사용자는 읽기만 가능

```
posts/<int:post_id>

✅ get

결과
{
    "id": 20,
    "category": 1,
    "comments": [
        {
            "id": 4,
            "content": "ㅋㅋㅋz",
            "post": 20,
            "author": 3
        }
    ],
    "title": "넘 어렵다",
    "content": "이번 시험 망한듯ㅋ",
    "created_date": "2024-04-29",
    "modified_date": "2024-04-28T16:20:43.165006Z",
    "author": {
        "username": "mseo"
    }
}

✅ post
: header에 jwt 토큰을 함께 보내야 함
: 인증된 사람만 가능
{
    "category": 2,
    "title": "수업 째고 싶어용",
    "content": "ㅈㄱㄴ"
}

✅ put
: header에 jwt 토큰을 함께 보내야 함
: 인증된 사람만 가능
: 글 등록한 사람과 일치
요청
{
    "category": 1,
    "title": "넘 어렵다",
    "content": "이번 시험 망한듯,,,ㅠ"
}

결과
{
    "id": 20,
    "category": 1,
    "comments": [
        {
            "id": 4,
            "content": "ㅋㅋㅋz",
            "post": 20,
            "author": 3
        }
    ],
    "title": "넘 어렵다",
    "content": "이번 시험 망한듯,,,ㅠ",
    "created_date": "2024-04-29",
    "modified_date": "2024-04-28T16:24:59.084761Z",
    "author": {
        "username": "mseo"
    }
}

✅ delete
: header에 jwt 토큰을 함께 보내야 함
: 인증된 사람만 가능
: 글 등록한 사람과 일치

```
### comment

```
comments/
✅ post
: header에 jwt 토큰을 함께 보내야 함
: 인증된 사람만 가능

요청
{
    "post":20,
    "content": "ㅋㅋㅋ"
}
결과
{
    "id": 5,
    "content": "ㅋㅋㅋ",
    "post": 20,
    "author": {
        "username": "mseo1"
    }
}

comments/<int:comment_id>
✅ delete
: header에 jwt 토큰을 함께 보내야 함
: 인증된 사람만 가능
: 댓글 등록한 사람과 일치
```

---

### 참고자료
* [블로그](https://blog.naver.com/funlucky1002/221484941608)
* [인증 인가](https://donis-note.medium.com/django-rest-framework-authentication-permission-%EC%9D%B8%EC%A6%9D%EA%B3%BC-%EA%B6%8C%ED%95%9C-cc9b183fd901)
* [to representation](https://velog.io/@arara90/django-torepresentation)
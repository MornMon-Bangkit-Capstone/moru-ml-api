# API

## Endpoint

`https://xxxx/api/v1/{prefix}/{param}`

## Books

### Recommendation Content Based

- URL
  - `/books/recommendation_content/{judul}/{jumlah}"`
- Method
  - `POST`
- Parameter:
  - `judul` as `string`, must be unique
  - `jumlah` as `int`
- Response

```
{
    "message": "Data Sucessfully Generated",
    "status": 200,
    "error": false,
    "data": [
        {
            "Judul": "Wild About Harry",
            "Penulis": "Linda Lael Miller"
        },
        {
            "Judul": "The Secrets of Harry Bright",
            "Penulis": "Joseph Wambaugh"
        },
        {
            "Judul": "Harry the Dirty Dog",
            "Penulis": "Gene Zion"
        },
        {
            "Judul": "Harry Potter and the Goblet of Fire",
            "Penulis": "J. K. Rowling"
        },
        {
            "Judul": "Harry Potter and the Chamber of Secrets",
            "Penulis": "J. K. Rowling"
        }
    ]
}
```

### Recommendation Collaborative Based

- URL
  - `/books/recommendation_collaborative/{user_id}"`
- Method
  - `POST`
- Parameter:
  - `user_id` as `int`, must be unique
- Response

```
{
    "message": "Data Sucessfully Generated",
    "status": 200,
    "error": false,
    "data": [
        [
            "Little Altars Everywhere",
            "Castle",
            "Potshot",
            "Whirlwind",
            "Legend",
            "Revelation Space",
            "A Cry in the Night",
            "Tunnel in the Sky",
            "Guess How Much I Love You",
            "Illusions"
        ]
    ]
}
```

## Sports

- URL
  - `/sports/recommendation_content/{judul}"`
- Method
  - `POST`
- Parameter:
  - `judul` as `string`, must be unique based on database and case sensitive
- Response

```
{
    "message": "Data Sucessfully Generated",
    "status": 200,
    "error": false,
    "data": [
        "Running",
        "Stair Climbing",
        "Scissor Kick",
        "Tucks Jump",
        "Bridge",
        "Badminton",
        "Elliptical Training",
        "Jumping Jack",
        "Horseback Riding",
        "Jumping Rope"
    ]
}
```

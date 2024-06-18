

## Operations (CRUD of HTTP Requests)

### One Person
- `PUT` Person (CREATE)
- `POST` Person (UPDATE or CREATE or UPSERT)
- `DELETE` Person (DELETE)
- `GET` Person (READ)

### Collection of Person
- `GET` Collection of Person


```
Person:
+ person_id: str
+ name: str
+ dob: str
+ occupation: str
+ height: float | int
```

Date of Birth `DOB` must be in `YYYY-MM-dd` format.

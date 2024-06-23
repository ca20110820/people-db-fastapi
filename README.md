# Person API - Sample Dockerized FastAPI

## Build and Run the Sample with Docker
- Build the image:
    ```bash
    docker build -t person-api .
    ```
- Run a container:
    ```bash
    $ docker run --rm -t --name person-api-container -p 127.0.0.1:8000:8000 person-api

    # Run with Volume Mount (on Windows Git Bash)
    # Make sure that you have "<project-root>/data/people.json"
    $ docker run --rm -t --name person-api-container -p 127.0.0.1:8000:8000 -v //$(pwd)/data/people.json:/app/data/people.json person-api
    ```

## Operations (CRUD of HTTP Requests)

### One Person
- `GET` Person (READ)
- `POST` Person (CREATE)
- `PUT` Person (UPDATE or CREATE or UPSERT)
- `DELETE` Person (DELETE)

### Collection of Person
- `GET` Collection of Person


```
Person:
+ person_id: str
+ name: str
+ dob: str
+ occupation: str = null
+ height: float | int = null
```

Date of Birth `DOB` must be in `YYYY-MM-dd` format.

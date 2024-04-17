# FastAPI Boilerplate

### Short Demo Video
https://drive.google.com/file/d/1uvKvt1xeCfH0qwD0Hlhc2yVVH-k_07PA/view?usp=sharing

# New Features
- Event Entity
- Modify User Entity to Support Event
- Event Routers and Services
- New User Routers and Services
- For Event Merge, merge attributes as follows
  - sort by startTime
  - merge "Title1", "Title2" -> "title: Title1; title: Title2"
  - merge "description1", "description2" -> "Title1: description1; Title2: description2"
  - merge "status1", "status2" -> 'TODO' if status1=='TODO'; 'COMPLETED' if status2=='COMPLETED'; 'IN_PROGRESS' otherwise
  - merge "startTime1", "startTime2" -> startTime1
  - merge "endTime1", "endTime2" -> endTime2
  - merge [invitees1], [invitees2] -> [invitees1, invitees2]

## Event Entity
app/event/domain/entity/event.py
- `id`: primary key, auto increment
- `title`: String, required
- `description`: String, optional
- `status`: Enum, required. 'TODO', 'IN_PROGRESS', 'COMPLETED'
- `createdAt`: DateTime, auto generated
- `updatedAt`: DateTime, auto generated
- `startTime`: DateTime, optional
- `endTime`: DateTime, optional
- `invitees`: sqlalchemy relationship with User Entity

## Event User Entity
app/event/domain/entity/event.py
- `event_id`: foreign key to Event Entity
- `user_id`: foreign key to User Entity

## New Field in User Entity
app/user/domain/entity/user.py
- `events`: sqlalchemy relationship with Event Entity

## APIs

### Event APIs
- Create Event
    - POST /api/v1/event
    - Request Body
    ```json
    {
        "title": "Event Title",
        "description": "Event Description",
        "status": "TODO",
        "startTime": "2022-01-01T00:00:00",
        "endTime": "2022-01-01T01:00:00"
    }
    ```
    - Response
    ```json
    {
        "id": 1,
        "title": "Event Title",
        "description": "Event Description",
        "status": "TODO",
        "startTime": "2022-01-01T00:00:00",
        "endTime": "2022-01-01T01:00:00"
    }
    ```
- Get Event
    - GET /api/v1/event/{event_id}
    - Response
    ```json
    {
        "id": 1,
        "title": "Event Title",
        "description": "Event Description",
        "status": "TODO",
        "startTime": "2022-01-01T00:00:00",
        "endTime": "2022-01-01T01:00:00",
        "createdAt": "2022-01-01T00:00:00",
        "updatedAt": "2022-01-01T00:00:00",
        "invitees": [1,2,3] // User IDs
    }
    ```
- Delete Event
    - DELETE /api/v1/event/{event_id}
    - Response
    ```json
    {
        "message": "success"
    }
    ```
- Add User to Event Invitees
  - PUT /api/v1/event/{event_id}/invitee
  - Request Body
    ```json
    {
        "user_id": 1
    }
    ```
  - Response
      ```json
      {
          "user_id": "{user_id}",
          "event_id": "{event_id}"
      }
      ```

### New User APIs
- Get User by ID
    - GET /api/v1/user/{user_id}
    - Response
    ```json
    {
        "id": 1,
        "email": "a@b.c",
        "nickname": "hide",
        "events": ["title: Event Title1", "title: Event Title2"] // Event Titles
    }
    ```
- Add Event to User Events
  - PUT /api/v1/user/{user_id}/event
  - Request Body
    ```json
    {
        "event_id": 1
    }
    ```
  - Response
      ```json
      {
          "user_id": "{user_id}",
          "event_id": "{event_id}"
      }
      ```
- Merge Events for a User
  - PUT /api/v1/user/{user_id}/events
  - Response
      ```json
      {
          "message": "success"
      }
      ```

## Code Structure

- `Routers`: app/event/adapter/input/api/v1/event.py; The top level router, defines urls 
- `Services`: app/event/application/service/event.py; Logic Layer include exception handling, business logics
- `DAO`: app/event/adapter/output/persistence/sqlalchemy/event.py; Data Access Layer, CRUD operations
- `Entities`: app/event/domain/entity/event.py; Data Model
- `Tests`: 
    - app/event/application/service/test_event.py; Service Layer Test
    - app/event/adapter/output/persistence/sqlalchemy/test_event.py; DAO Layer Test
    - app/event/adapter/input/api/v1/test_event.py; Router Layer Test for Event
    - app/user/adapter/input/api/v1/test_user.py; Router Layer Test for new User APIs
    


## Run

### Checkout eventAPIs branch
```shell
> git checkout eventAPIs
```

### Launch docker
```shell
> docker-compose -f docker/docker-compose.yml up
```

### Install dependency
```shell
> poetry shell
> poetry install
```

### Apply alembic revision
```shell
> alembic upgrade head
```

### Run server
```shell
> python3 main.py --env local|dev|prod --debug
```

### Run test codes
```shell
> make test
```

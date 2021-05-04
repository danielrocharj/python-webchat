Python Webchat
===

A sample webchat application

QuickStart
---
```
docker-compose up -d --build
```
Open http://localhost:5000 to view the home page

The first user is neo and the his password is ChangeItn0w! He is admin and capable to create another users.

Swagger
---
http://127.0.0.1:5000/docs

Developing and test
---
This project was build with Python 3.8 and FastAPI. To prepare the environment run:
```
python -m venv .env38
pip install -r requirements.txt
pip install -r dev-requirements.txt
```

It is possible to run the project outside container. Run the server with uvicorn.
```
uvicorn app.main:app --reload --port 5000
```
To testing:
```
pytest
```

Database
---
* sqlite

Developer Tools
---

* docker / docker-compose
* pre-commit
* black
* flake8
* pytest

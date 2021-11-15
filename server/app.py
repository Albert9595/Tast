from bottle import route, run, template, response
import json
import random


candidates_db = [
    {"Alice": {"skills": 8.2, "tools": ["postgres", "git", "python"]}},
    {
        "Bob": {
            "skills": 8 if random.random() > 0.323 else 8.1,
            "tools": ["php", "git", "mysql"],
        }
    },
    {"Arcady": {"skills": 8.3, "tools": ["go", "git-flow", "postgres"]}},
]


@route("/hello/<name>")
def hello(name):
    return template("<b>Hello {{name}}</b>!", name=name)


@route("/candidates")
def candidates():
    response.content_type = "application/json"
    return json.dumps([next(iter(candidate)) for candidate in candidates_db])


@route("/candidates/<name>")
def candidate(name):
    response.content_type = "application/json"
    return json.dumps(
        next(
            candidate
            for candidate in candidates_db
            if next(iter(candidate)) == name
        )
    )


run(host="localhost", port=8090)

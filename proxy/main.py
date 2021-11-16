from bottle import route, run, template, HTTPResponse
import json
import requests
import pydantic
from config import BASE_CANDIDATES_URL
from schemas import CandidateData


"""
Обратная связь по заданию.

Альберт, я здесь оставлю несколько замечаний и советов на будущее:

1. в языке пайтон есть определённый стиль именования объектов и переменных.
    есть такие документы, называются pep, Python Enhancement Proposals.
    я советую тебе, как разработчику на пайтон, опираться на то, что рекомендуют создатели языка.
    про нейминг здесь https://www.python.org/dev/peps/pep-0008/

2. валидация данных обычно включает себя не только проверку одного параметра, 
    но и всех входящих данных. реализуют это часто с помощью внешних библиотек,
    которые основную часть рутинного кода в себя включают. тебе остаётся только описать схему данных. пример приведу ниже.

3. то, что ты взял мою наработку за основу, в целом, неплохо.
    но лучше было взять django, чтобы показать на нём то, что ты умеешь с тем, с чем работал.

4. в твоем коде ты по два раза обращаешься к данным каждого кандидата
    127.0.0.1 - - [16/Nov/2021 09:07:46] "GET /candidates HTTP/1.1" 200 26
    127.0.0.1 - - [16/Nov/2021 09:07:46] "GET /candidates/Alice HTTP/1.1" 200 66
    127.0.0.1 - - [16/Nov/2021 09:07:46] "GET /candidates/Alice HTTP/1.1" 200 66
    127.0.0.1 - - [16/Nov/2021 09:07:46] "GET /candidates/Bob HTTP/1.1" 200 56
    127.0.0.1 - - [16/Nov/2021 09:07:46] "GET /candidates/Arcady HTTP/1.1" 200 68
    127.0.0.1 - - [16/Nov/2021 09:07:46] "GET /candidates/Arcady HTTP/1.1" 200 68

    обрати внимание где и почему. здесь можно и нужно обойтись одним запросом к каждому роуту.

5. в целом, код можно и нужно писать в более понятной манере.
    для этого минимум нужно не торопиться, откладывать, переделывать, давать время полежать, чтобы переписать.


p.s. обрати внимание на то, как ты используешь git. называешь коммиты, используешь ли pull requests.
    совет: читай больше чужого несложного pythonic кода. вот тот же фреймворк bottle, на котором этот тест построен попробуй изучить.
    как организован код, как называются файлы, переменные, процедуры, коммиты. какой смысл несут названия и так далее.
    когда пишешь на пайтон старайся придерживаться принятого сообществом кодового стиля.


в общем, вот пример, лишённый указанных недостатков.

"""

@route("/hello/<name>")
def hello(name):
    return template("<b>Hello {{name}}</b>!", name=name)


@route("/candidates")
def candidates():
    candidates_names = requests.get(BASE_CANDIDATES_URL).json()
    candidates = []
    status = 200
    for name in candidates_names:
        candidate_raw = requests.get(f"{BASE_CANDIDATES_URL}/{name}").json()
        try:
            candidate__data_validated = CandidateData(**candidate_raw[name]).dict()
            candidates.append({name: candidate__data_validated})
        except pydantic.ValidationError:
            status = 206
    return HTTPResponse(status=status, body=json.dumps(candidates)) 

run(host="localhost", port=9115)

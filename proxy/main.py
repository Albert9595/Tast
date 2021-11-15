from bottle import route, run, template, HTTPResponse
import json
import requests


@route("/hello/<name>")
def hello(name):
    return template("<b>Hello {{name}}</b>!", name=name)


@route("/candidates")
def candidates():
    status = 200
    ConcatinationCandidates = []
    UrlCandidateName  = "http://localhost:8090/candidates"
    for CandidateSkill in requests.get(UrlCandidateName).json():
        if type(requests.get(f"{UrlCandidateName}/{CandidateSkill}").json()[CandidateSkill]["skills"]) == float:
            ConcatinationCandidates.append(requests.get(f"{UrlCandidateName}/{CandidateSkill}").json())
        else:
            status = 206
    return HTTPResponse(status=status, body=json.dumps(ConcatinationCandidates)) 

run(host="localhost", port=9115)

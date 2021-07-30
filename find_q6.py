# Python script to send/retrieve HTTP data
# Exploiting a quiz by brute forcing potential answer values until grade of 100% is achieved
# GW

import base64
import requests
import beepy
import time, datetime
import json


def now_milliseconds():
    return int(time.time() * 1000)


def build_data_q6(q6_ans):
    data = '{"result":[{"question":"autogen-a4-287","format":"tf","answer":true},{"question":"autogen-a4-288",' \
                '"format":"mc","answer":1},{"question":"autogen-a4-289","format":"line","answer":"magenta"},' \
           '{"question":' \
           '"autogen-a4-290","format":"line","answer":"' + str(10) + '"},' \
                                                                              '{"question":"autogen-a4-291","format"'\
                                                                       ':"line","answer":'\
           '"'+str(12)+'"},{"question":"autogen-a4-292","format":"line","answer":"'+str(q6_ans)+'"},{"question":' \
                                                                                                '"autogen-a4-293",' \
                       '"format":"mc"' \
           ',"answer":-1}],"quiz":"task3","practice":false,"total_questions":7,"retry":true,"instant":false,"warnzero"'\
           ':true,"duebefore":"2021-04-11 16:00","idnum":"27285","code":"eb5a13a2a5f1c58f167e694b312fb59b","user":' \
           '"89465738","declare":"user name"}'

    return base64.b64encode(bytes(data, 'ascii'))


def submit_quiz_q6():
    for x in range(57, 1001):
        obj = {'data': build_data_q6(x)}

        obj['data'] = (build_data_q6(x).decode('ascii')).replace("=", "")
        # need to remove '=' since it won't be sent properly, it'll be converted to non-base64 encoded string

        # https://stackoverflow.com/questions/45442665/python-convert-json-object-to-dict
        headers = """[
			{
				"name": "Accept",
				"value": "*/*"
			},
			{
				"name": "Accept-Encoding",
				"value": "gzip, deflate, br, base64"
			},
			{
				"name": "Accept-Language",
				"value": "en-CA,en-US;q=0.7,en;q=0.3"
			},
			{
				"name": "Authorization",
				"value": "Basic Z2FicmllbGEud2Npc2xvOnd2dGx6bW0="
			},
			{
				"name": "Connection",
				"value": "keep-alive"
			},
			{
				"name": "Content-Length",
				"value": "864"
			},
			{
				"name": "Content-Type",
				"value": "application/x-www-form-urlencoded"
			},
			{
				"name": "Content-Encoding",
				"value": "base64"
			},
			{
				"name": "Cookie",
				"value": "<REMOVED FOR GIT>"
			},
			{
				"name": "Host",
				"value": "<REMOVED FOR GIT>"
			},
			{
				"name": "Origin",
				"value": "https://<REMOVED FOR GIT>"
			},
			{
				"name": "Referer",
				"value": "https://<REMOVED FOR GIT>/27285/task3.html"
			},
			{
				"name": "Sec-GPC",
				"value": "1"
			}
		]"""

        headers_dict = {}
        for d in json.loads(headers):
            d['name']: d['value']
            headers_dict[d['name']] = d['value']

        print("Submitting quiz...\n")
        r = requests.post("https://<REMOVED FOR GIT>/submit.pl",
                          data=obj, headers=headers_dict)
        print("Submitted to url = ", r.url)
        print("Status returned = ", r.status_code)
        print("request headers:\n", r.request.headers)
        print("request body:\n", r.request.body)

        r2 = ses.get("https://<REMOVED FOR GIT>/27285/task3.submitted?=" + str(now_milliseconds()))
        print(r2.text)
        print("was returned from ", r2.url)
        grade = get_grade()
        if str(60) == grade:
            # https://pypi.org/project/beepy/
            beepy.beep(6)
            print("x = ", x, "\tgrade = ", grade)
            break

def get_grade():
    print("Getting grade.\n")
    r = ses.get('https://<REMOVED FOR GIT>/27285/task3.feedback')
    print(r.status_code)
    print(r.text)
    return r.text[0:2]


if __name__ == '__main__':
    global ses
    ses = requests.Session()
    ses.auth = ('89465738', 'wvtlzmm')
    submit_quiz_q6()
    get_grade()



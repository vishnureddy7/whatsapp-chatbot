from flask import Flask
from flask import request
from twilio.twiml.messaging_response import MessagingResponse
import requests


app = Flask(__name__)


@app.route("/bot", methods=["POST"])
def bot():
    print(request.values);
    for i in request.values:
        print(i)
    print(request.values.get('Body',''));
    incoming_msg = request.values.get("Body", '');
    resp = MessagingResponse();
    msg = resp.message();
    if 'corona' in incoming_msg:
        cor_resp = requests.get("https://coronavirus-19-api.herokuapp.com/all")
        if cor_resp.status_code == 200:
            data = cor_resp.json();
            msg.body("cases:{cases}\ndeaths:{deaths}\nrecovered:{recovered}".\
                     format(cases=data['cases'], deaths=data['deaths'],\
                            recovered=data['recovered']));
        else:
            msg.body('unable to get corona stats now');
    else:
        msg.body('you have reached us.')
        #msg.media(); if you want to send any image or video put link
    return str(resp);


@app.route("/", methods="GET")
def home():
    return "Working Fine";


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True);

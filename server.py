import os
from flask import Flask, Response , request
from twilio.jwt.access_token import AccessToken, VoiceGrant
from twilio.rest import Client
import twilio.twiml
import json
from json import JSONEncoder

ACCOUNT_SID = 'AC***'
API_KEY = 'SK***'
API_KEY_SECRET = '***'
PUSH_CREDENTIAL_SID = 'CR***'
APP_SID = 'AP***'


app = Flask(__name__)

@app.route('/accessToken',methods=['GET', 'POST'])
def token():
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  api_key = os.environ.get("API_KEY", API_KEY)
  api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)
  push_credential_sid = os.environ.get("PUSH_CREDENTIAL_SID", PUSH_CREDENTIAL_SID)
  app_sid = os.environ.get("APP_SID", APP_SID)
  

  grant = VoiceGrant(
    push_credential_sid=push_credential_sid,
    outgoing_application_sid=app_sid
  )
  
  identity = request.form['socialId']
  
  token = AccessToken(account_sid, api_key, api_key_secret, identity)
  token.add_grant(grant)

  response={'identity':identity,'token':str(token)}
  return Response(json.dumps(response),  mimetype='application/json')

@app.route("/voice",methods=['GET', 'POST'])
def voice():
      
    
    
    resp = twilio.twiml.Response()
    dial = resp.dial(callerId="587327ac4d35ecdb1114f87b")
    dial.client("58736d239e9507d0070c5d16")   
    return Response(str(resp), mimetype='text/xml')

@app.route('/outgoing', methods=['GET', 'POST'])
def outgoing():
  resp = twilio.twiml.Response()
  resp.say("Congratulations! You have made your first oubound call! Good bye.")
  return str(resp)

@app.route('/incoming', methods=['GET', 'POST'])
def incoming():
  resp = twilio.twiml.Response()
  resp.say("Congratulations! You have received your first inbound call! Good bye.")
  return str(resp)

@app.route('/placeCall', methods=['GET', 'POST'])
def placeCall():
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  api_key = os.environ.get("API_KEY", API_KEY)
  api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)

  client = Client(api_key, api_key_secret, account_sid)
  call = client.calls.create(url=request.url_root + 'incoming',to='client:' + 'receiver', from_='client:' + 'sender')
  return str(call.sid)

@app.route('/', methods=['GET', 'POST'])
def welcome():
  resp = twilio.twiml.Response()
  resp.say("Welcome to Twilio")
  return str(resp)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port, debug=True)

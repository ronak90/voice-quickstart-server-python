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

IDENTITY = 'voice_test'
CALLER_ID = 'quick_start'

app = Flask(__name__)

@app.route('/accessToken',methods=['GET', 'POST'])
def token():
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  api_key = os.environ.get("API_KEY", API_KEY)
  api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)
  push_credential_sid = request.form['push_credential_sid']
  app_sid = os.environ.get("APP_SID", APP_SID)
  
  
  identity = request.form['socialId']

  grant = VoiceGrant(
    push_credential_sid=push_credential_sid,
    outgoing_application_sid=app_sid
  )

  token = AccessToken(account_sid, api_key, api_key_secret, identity)
  token.add_grant(grant)

  response={'identity':identity,'token':str(token)}
  return Response(json.dumps(response),  mimetype='application/json')

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
  
  IDENTITY = request.form['To']
  CALLER_ID = request.form['From']
  
  client = Client(api_key, api_key_secret, account_sid)
  call = client.calls.create(url=request.url_root + 'incoming', to='client:' + IDENTITY, from_='client:' + CALLER_ID)
  return str(call.sid)

@app.route('/', methods=['GET', 'POST'])
def welcome():
  resp = twilio.twiml.Response()
  resp.say("Welcome to Twilio")
  return str(resp)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=True)

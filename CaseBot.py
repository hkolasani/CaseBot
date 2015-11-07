from flask import Flask,request
import httplib,sys

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():

    channel = "dfdf"
    try:
      channel = request.values['channel_name']
    except:
      print "Unexpected error:", sys.exc_info()[0]
      e = sys.exc_info()[0]
      raise
    else:
        postToSlack(channel)
    finally:
        return '{"text":"Hello from pyCharm to "' + channel + '"}!'

def postToSlack(chnl):

    body = '{"text":"Posting from pyCharm' + chnl + '"}'
    conn = httplib.HTTPSConnection("hooks.slack.com")
    conn.request("POST", "/services/T0DMM2G9H/B0DQK99SM/5NWo2oxIn3l4SXoD2seyDBqu",body)
    response = conn.getresponse()
    conn.close()
    print response.status, response.reason

    return

if __name__ == '__main__':
    app.run()



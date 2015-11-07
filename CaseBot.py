from flask import Flask,request
from cmislib import CmisClient, Repository, Folder
import httplib,sys

app = Flask(__name__)

theToken = 'sII3Kx1Kml2sJWgbcFyNCRlh'
theChannel = ''

@app.route('/CaseBot', methods=['GET', 'POST'])
def hello_world():

    try:
      client = CmisClient('http://cmis.alfresco.com/cmisatom', 'admin', 'admin')
      repo = client.defaultRepository
      print repo.id

      channelName = request.values['channel_name']
      channelId = request.values['channel_id']
      token = request.values['token']
      userId = request.values['user_id']
    except:
      print "Unexpected error:", sys.exc_info()[0]
      e = sys.exc_info()[0]
      raise
    else:
        if token != theToken:
            return '{"text":"Invalid Token in the Request"}'
        else :
            postToSlack(channelName)
    finally:
        return '{"text":"RepoId from pyCharm to "' + repo.id + channelName + '"}!'

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



from flask import Flask,request,jsonify,Response
from cmislib import CmisClient, Repository, Folder
import httplib,sys,json

app = Flask(__name__)

theToken = 'sII3Kx1Kml2sJWgbcFyNCRlh'
theChannel = ''

@app.route('/CaseBot', methods=['GET', 'POST'])
def hello_world():

    docs = []
    postText = ""
    responseURL = ""

    try:
      client = CmisClient('http://cmis.alfresco.com/cmisatom', 'admin', 'admin')
      repo = client.defaultRepository
      print repo.id

      cmisdocs = repo.query("select * from cmis:document where cmis:name LIKE '%Hari%'")
      for cmisdoc in cmisdocs:
            print cmisdoc.name
            doc = {}
            doc['title'] = cmisdoc.name
            docs.append(doc)
            postText = postText + cmisdoc.name + '\n'

      print jsonify(results=docs)
      responseURL = request.values['response_url']
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
            postToSlack(postText,responseURL)
    finally:
        #return '{"text":"RepoId from pyCharm to "' + repo.id + channelName + '"}!'
        #print json.dumps(docs)
        #return jsonify(results=docs)
        return Response(status=200)

def postToSlack(bodyText,postURL):

    body = '{"text":"' + bodyText + '"}'
    #body = '{"text":"<http://www.google.com>"}'
    #conn = httplib.HTTPSConnection("hooks.slack.com")
    conn = httplib.HTTPSConnection(postURL)
    #conn.request("POST", "/services/T0DMM2G9H/B0DQK99SM/5NWo2oxIn3l4SXoD2seyDBqu",body)
    conn.request("POST",body)
    response = conn.getresponse()
    conn.close()
    print response.status, response.reason

    return

if __name__ == '__main__':
    app.run()



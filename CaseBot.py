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
      return Response(status=500)
    else:
        if token != theToken:
            return '{"text":"Invalid Token in the Request"}'
        else :
            postToSlack(postText,responseURL)
            return Response(status=200)

def postToSlack(bodyText,postURL):

    salckcommandURL = 'https://hooks.slack.com/commands'

    if postURL.index(salckcommandURL) < 0:
        return

    salckcommandURI = postURL[salckcommandURL.length:]

    body = '{"response_type": "in_channel","text":"' + bodyText + postURL +  '"}'
    #body = '{"text":"<http://www.google.com>"}'
    conn = httplib.HTTPSConnection("hooks.slack.com")
    #conn.request("POST", "/services/T0DMM2G9H/B0DQK99SM/5NWo2oxIn3l4SXoD2seyDBqu",body)  //to an incming web hook
    #conn.request("POST",postURL,body)
    fullURL = salckcommandURL + '/' + salckcommandURI
    conn.request("POST",fullURL,body)
    response = conn.getresponse()
    conn.close()
    print response.status, response.reason

    return

if __name__ == '__main__':
    app.run()



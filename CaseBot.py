from flask import Flask,request,jsonify,Response
from cmislib import CmisClient, Repository, Folder
import httplib,sys,json
import random

app = Flask(__name__)

slackToken = 'sII3Kx1Kml2sJWgbcFyNCRlh'
theChannel = ''

@app.route('/CaseBot', methods=['POST'])
def doPost():

    try:
        token = request.values['token']
        if token != slackToken:
            return '{"text":"Error: Invalid Token!"}'

        cmdArg = request.values['text']
        if cmdArg == None:
            createNewCase(request)
        else:
            args = cmdArg.split(" ")
            caseNumber = args[0]
            action = args[1]

            if caseNumber == None or action == None:
                return '{"text":"Error: Invalid Command!"}'

            if action == "docs":
                getDocs(caseNumber)
            elif action == "info":
                getInfo(caseNumber)
            else:
                moveToChannel(caseNumber)
    except:
      print "Unexpected error:", sys.exc_info()[0]
      e = sys.exc_info()[0]
      return Response(status=500)

def getDocs(caseNumber):

    attachmentsDict = {}
    attachments = []

    client = CmisClient('http://cmis.alfresco.com/cmisatom', 'admin', 'admin')
    repo = client.defaultRepository

    cmisdocs = repo.query("select * from cmis:document where cmis:name LIKE '%Hari%'")

    for cmisdoc in cmisdocs:
        props = [{"title":"Author","value":"jhgjgj","short":True},{"title":"Date Created","value":"3 Days Ago","short":True}]
        #attachment = {"title":cmisdoc.name,"text":cmisdoc.id,"title_link":cmisdoc.id,"color":generateColor(),"fields":props}
        attachment = {"title":cmisdoc.name,"text":cmisdoc.id,"title_link":cmisdoc.id,"color":generateColor()}
        attachments.append(attachment)

    attachmentsDict['attachments'] = attachments
    postText = json.dumps(attachments)

    body = '{"response_type": "in_channel","attachments":' + postText  + '}'

    responseURL = request.values['response_url']

    postToSlack(body,responseURL)

    return Response(status=200)

def getInfo(caseNumber):
    return

def getInfo(caseNumber):
    return

def moveToChannel(caseNumber,channelName):
    return

def postToSlack(body,postURL):

    salckcommandURL = 'https://hooks.slack.com/commands'

    if postURL.index(salckcommandURL) < 0:
        return

    salckcommandURI = postURL[len(salckcommandURL) +  1:len(postURL) - 1]

    conn = httplib.HTTPSConnection("hooks.slack.com")

    fullURL = salckcommandURL + '/' + salckcommandURI

    conn.request("POST",fullURL,body)
    response = conn.getresponse()
    conn.close()
    print response.status, response.reason

    return

def createNewCase(reqeust):
    return

def generateColor():
    color = '#{:02x}{:02x}{:02x}'.format(*map(lambda x: random.randint(0, 255), range(3)))
    return color

if __name__ == '__main__':
    app.run()



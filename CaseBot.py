from flask import Flask,request,jsonify,Response
from cmislib import CmisClient, Repository, Folder
import httplib,sys,json
import random

app = Flask(__name__)

incomingHooks = {"hold":"https://hooks.slack.com/services/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"}
slackToken = 'sII3Kx1Kml2sJWgbcFyNCRlh'
theChannel = ''

@app.route('/CaseBot', methods=['POST'])
def doPost():

    try:
        token = request.values['token']
        if token != slackToken:
            return '{"text":"Error: Invalid Token!"}'

        fromChannel = request.values['channel_name']

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
                toChannel = action
                move(caseNumber,fromChannel,toChannel)
    except:
      print "Unexpected error:", sys.exc_info()[0]
      e = sys.exc_info()[0]
      return Response(status=500)
    else:
      return Response(status=200)


def getDocs(caseNumber):

    attachmentsDict = {}
    attachments = []

    #query CMS
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
    postURL = getCommandURL(responseURL)

    postToSlack(body,postURL)

def move(caseNumber,fromChannel,toChannel):

    #post to toChannel
    hooks = incomingHooks
    toChannelURL = hooks[toChannel]
    body = '{"text:":"Moved from #'  + fromChannel + '"}'
    postToSlack(body,toChannelURL)

    #now post the response back to the fromChannel
    body = '{"response_type": "in_channel","text":"Case ' + caseNumber + ' Posted to #' + toChannel  + '"}'
    responseURL = request.values['response_url']
    postURL = getCommandURL(responseURL)
    postToSlack(body,postURL)

    return

def getInfo(caseNumber):
    return

def getCommandURL(responseURL):
    salckcommandURL = 'https://hooks.slack.com/commands'

    if responseURL.index(salckcommandURL) < 0:
        return

    salckcommandURI = responseURL[len(salckcommandURL) +  1:len(responseURL) - 1]
    fullURL = salckcommandURL + '/' + salckcommandURI

    return fullURL

def postToSlack(body,postURL):
    conn = httplib.HTTPSConnection("hooks.slack.com")
    conn.request("POST",postURL,body)
    response = conn.getresponse()
    conn.close()

    return

def createNewCase(reqeust):
    return

def generateColor():
    color = '#{:02x}{:02x}{:02x}'.format(*map(lambda x: random.randint(0, 255), range(3)))
    return color

if __name__ == '__main__':
    app.run()



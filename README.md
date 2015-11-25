# CaseBot is Slackbot for CMIS Repos.

Case Management is typically about bundling data/documents and routing it thru a business process (workflows/queues). Some of the big players in that space are IBM, Pega and Alfresco. These tools are backed by a content repository, workflow engine and a web based UI that will enable the users to work on a "Case" (a claim or Loan application). Case Management users typically work on activities using workflow queues and move data,content from one queue to the other. 

So, how can we use Slack for Case Management:

1. Define Slack Channels that correspond to the Case Management Activities/Queues.

2. Integrate Slack with the Content Management system using:

Slash command that talks to the Slack bot for the CMS repository
Incoming Web hooks for each of the Slack Channels, so the the Slack Bot can respond with data and content.
Below are a few examples of the Slack's Slash commands that integrate with external Content Management Systems.

A. Getting the documents for a specific case:

B. Getting the Case Details:

C. Moving the Case from One Channel (queue) to another:

D. Trigger on a New Case Event in CMS to post message to the 'Intake' channel on Slack.

Prototype

I built a quick prototype that demonstrate the above functionality with these components:

1. Alfresco Content Management System where the Case documents are stored. This repository is accessed from the CaseBot using CMIS API. 
2. Slack Incoming Web Hooks for Intake  Channel: The new case event from Alfresco will post a message using this incoming hook.

3. Slash commands that Slack users can type in the message box:

        "/case [casenumber] docs"  -    gets the Case Documents

        "/case [caseNumber] info"  - gets the Case details

        "/case [caseNumber] [channelName]"  - posts a message to channel

4. CaseBot: A Python-Flask based HTTP Service that can receive the requests   from Slack commands and post the response back to the Slack channels. The CaseBot accesses Alfresco CMS using CMIS API with Apache Chemistry's  python cmslib This CaseBot can be configured to connect to any CMIS (Content Management Interoperability service) supported repositories like Alfresco or IBM FileNet.

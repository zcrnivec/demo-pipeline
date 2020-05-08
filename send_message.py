#
#	Copyright (c) 2020 Cisco and/or its affiliates.
#
#	This software is licensed to you under the terms of the Cisco Sample
#	Code License, Version 1.1 (the "License"). You may obtain a copy of the
#	License at
#
#		       https://developer.cisco.com/docs/licenses
#
#	All use of the material herein must be in accordance with the terms of
#	the License. All rights not expressly granted by the License are
#	reserved. Unless required by applicable law or agreed to separately in
#	writing, software distributed under the License is distributed on an "AS
#	IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#	or implied.
#

import json
import os
import sys
from fpdf import FPDF
import urllib3

import requests
from requests.auth import HTTPBasicAuth
from requests_toolbelt.multipart.encoder import MultipartEncoder

WEBEX_TEAMS_ACCESS_TOKEN = os.environ['WEBEX_TEAMS_ACCESS_TOKEN']
WEBEX_TEAMS_ROOM_ID = os.environ['WEBEX_TEAMS_ROOM_ID']
JENKINS_TOKEN = os.environ['JENKINS_TOKEN']

#Disable Certificate warning
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size = 10)
data = requests.get(sys.argv[3], auth=('admin', JENKINS_TOKEN))
for x in data.text.split('\n'):
    pdf.cell(200, 10, txt = x, ln = 1, align = 'L')
pdf.output("buildresults_" + sys.argv[5] + ".pdf")

m = MultipartEncoder(
    {
      'roomId': WEBEX_TEAMS_ROOM_ID,
      'markdown': f'## A new CI/CD build in {sys.argv[1]} branch has just finished!\n' + \
                  f' --- \n' + \
                  f'* **BUILD:** {sys.argv[2]}\n' + \
                  f'* **LOGS:** Click [HERE]({sys.argv[3]}) or review the attached PDF.\n' + \
                  f'* **STATUS:** {sys.argv[4]}.',
      'files': ("buildresults_" + sys.argv[5] + ".pdf", open("buildresults_" + sys.argv[5] + ".pdf", 'rb'), 'application/pdf')
    }
)
message = requests.post(
    'https://api.ciscospark.com/v1/messages',
    data=m,
    headers={
              'Authorization': f'Bearer {WEBEX_TEAMS_ACCESS_TOKEN}',
              'Content-Type': m.content_type
            }
)

#Send final result code as message for Jenkins to catch in the build logs
print(message)


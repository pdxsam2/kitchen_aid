from __future__ import print_function
import pdb
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

### GLOBALS ###
index_file= open("/home/pi/gitHUB/kitch_aid/msg_bird-master/grocery_index.txt", "r")
grocery_index= index_file.readlines()
MAX= len(grocery_index)

### CREDENTIALS ###
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents']

# The ID of a sample document.
DOCUMENT_ID = '1FtdntyPniMYuV64z_8YSCmcK5zAzdk7FtxsiYr1eLSg'

### FUNCTIONS ###
#sends integers to a list of grocery items which returns the indicated grocery item
def listen():

	###this line was temporary, used for testing
	###print("Enter the number for the food you need:\n")

	i= int(input())

	if i < 0 or i > MAX:
		return "Error: Invalid Input"
	else: 
		return grocery_index[i] 

##connects to the file and then writes out the new item
def	export(new_item):
	creds = None
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'/home/pi/gitHUB/kitch_aid/msg_bird-master/credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('docs', 'v1', credentials=creds)

	#fill requests with new input 
	requests = [
         {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': new_item
            }
        }
		]
	#export to file
	result = service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()


### EXECUTE ###
if __name__ == '__main__':	##this is to gaurantee that you are in the right file
	new_item= listen()
	while(True):
		export(new_item)
		new_item= listen()



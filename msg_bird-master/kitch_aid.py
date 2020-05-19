from __future__ import print_function
import pdb
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

### GLOBALS ###
index_file= open("./grocery_index.txt", "r")
grocery_index= index_file.readlines()
MAX= len(grocery_index)

### CREDENTIALS ###
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents']

# The ID of a sample document.
id_creds = open("./credentials.txt", "r") 
DOCUMENT_ID= id_creds.readline()
DOCUMENT_ID= DOCUMENT_ID[:-1]

### FUNCTIONS ###
#sends integers to a list of grocery items which returns the indicated grocery item
def listen():

	i= raw_input()

	if i == 'q':
		return i;
	elif not i.isdigit():
		return "Error: Incorrect input type\n"
	else :
		j= int(i)

	if j < 0 or j > MAX:
		return "Error: Input out of range\n"
	else: 
		return grocery_index[j] 

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
				'./credentials.json', SCOPES)
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
if __name__ == '__main__':	
	new_item= listen()
	while(True):
		if new_item == 'q':
			exit()
		export(new_item)
		new_item= listen()



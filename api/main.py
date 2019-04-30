import requests
import json
import data as dt
from transcluster import *
import psql as sql
from login import *
import os


def checkResponseCode(code):
	print(code)
	if code == 200:
		return True;
	if code == 403:
		print('Bearer key issue')
	else:
	 	print('somethings wrong dude')
	 	return False;

def getBearerToken(credls):

	headers = {
	    'content-type': 'application/x-www-form-urlencoded',
	    'user-key': credls['user_key'],
	    'Authorization':'Basic '+credls['client_id']
	}
	#search=[sdfsdf,sdfsdf]

	data = {
	  'grant_type': 'client_credentials',
	  'scope': 'search'

	}

	response  = requests.post('https://api.meltwater.com/oauth2/access_token', headers=headers, data=data)
	response=response.json()

	print(response)
	

	if 'access_token' in response:
		dic={'bearer_key':response['access_token']}
	
		with open('bfile.txt','w') as file:
			file.write(json.dumps(dic))
			status='good'
			return({'status':status,'access_token':response['access_token']})
	else:
		return ({'statusCode':401})





	

def getSearches(credls):
	headers ={
    'Accept': 'application/json',
    'user-key':credls['user_key'] ,
    'Authorization': 'Bearer '+ credls['bearer_key'],
	}

	response = requests.get('https://api.meltwater.com/export/v1/searches', headers=headers)
	#print(str(response.content))
	if(checkResponseCode(int(response.status_code))):
		print('Search list response is good to go, code is {}'.format(response.status_code))
	return response;

def login(email,pswd,user_key):
	
	res=sql.if_exist('user_mail',email,'login_table')
	if(res['status']==True):
		print('Email id and client key exist in database.')
		temp=res['row']
		client_key=temp[0][1]; 
		credls={'user_key':user_key,'client_id':client_key}
		res=getBearerToken(credls)
		#print(res)
		if 'access_token' in res:

			#Which means credentaisl were right ? what to do with that ?
			#also now i have acces token which can be used for getting search ids. userkey will also be needed.
			print('acces key is in response acces key is : {}'.format(res['access_token']))
			access_token=res['access_token']
			return {'client_key':client_key,'message':'good'}
			#return client_key;


		else:
			status=False
			if 'statusCode' in res:
				if res['statusCode']==401:		

					print('Client or user creds are wrong, Client credentails were re generated and table entries shlud be updated with new ones.')
					#DELETE client credentails here and generate new one
					#DeleteCredls(client_id,email,password):
					res=createCreds(email,pswd)
					if(res['message']=='Unauthorized'):
						print('Here')
						return {'message':'Unauthorized'}


					client_id=res['client_id']
					print(client_id)
					DeleteCredls(client_id,email,pswd)
					res=createCreds(email,pswd)
					#print('printing from main page clien and secret  {} {}'.format(res['client_id'],res['client_secret']))
					string=res['client_id']+':'+res['client_secret']
					encoded_key=base64.b64encode(string.encode())
					encoded_key=encoded_key.decode('utf-8')

				#Update it to database..............................
					sql.addUser(email,encoded_key)
					status=True

				#Which means credentials could be wrong.
					credls={'user_key':user_key,'client_id':encoded_key}
					res=getBearerToken(credls)
					if 'access_token' in res:
						print('After updating on table, acces token generated')
						print('acces key is in response acces key is : {}'.format(res['access_token']))
						access_token=res['access_token']

						return {'client_key':encoded_key,'message':'good'}
					else :
						print('after updating entries on table someting happaned, probably because of internal server error')

				

			
					
	else:
		print('Entry is not there in Table')
		res=createCreds(email,pswd)
		if(res['message']=='Unauthorized'):
			return {'message':'Unauthorized'}
		client_id=res['client_id']
		if 'client_secret' in res:
			print('Accound does not have credls.. creating one.')
			string=res['client_id']+':'+res['client_secret']
			encoded_key=base64.b64encode(string.encode())
			encoded_key=encoded_key.decode('utf-8')
			sql.addUser(email,encoded_key)
			return {'client_key':encoded_key,'message':'good'}



		else:
			print('Accound does have credls, so regenerating it after deleting ....... ')
			DeleteCredls(client_id,email,pswd)
			res=ClasTrans(email,pswd)
			#print('printing from main page clien and secret  {} {}'.format(res['client_id'],res['client_secret']))
			string=res['client_id']+':'+res['client_secret']
			encoded_key=base64.b64encode(string.encode())
			encoded_key=encoded_key.decode('utf-8')
			sql.addUser(email,encoded_key)
			return {'client_key':encoded_key,'message':'good'}







		#Entry in database does not exist.
		#Generate Credls here.
		#if

			
			 



		#Client id assosiated with that account exists in my database:
		#getBearerToken(user_key,res[''])

	#print(cur)
	
	

	#if res['message'] == 'Exists':
		#print('Cliend id already exists')
		# Regenerate again here.
		#DeleteCredls(res['client_id'],email,password)


	#print(res['message'])




	#id=getBearerToken()
	#print(getBearerToken())
	#getSearches()
	#with open('file.txt','w') as file:
		#file.write(json.dumps(mydicct))


	

if __name__ == '__main__':

	os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/Bibin/OneDrive/Documents/key.json"


	email=input("Enter you email :")
	pswd =getpass.getpass('Password:') 
	#res=createCreds(email,pswd)
	user_key='<Your Key Here>'

	key=login(email,pswd,user_key)
	if(key['message']!='good'):
		print(key['message'])
		sys.exit()
	key=key['client_key']
	print('Got clientkey from login page {}'.format(key))

	#========================#
	# Do some checking above #
	#========================#
	
	credls={'user_key':user_key,'client_id':key}

	#with open('file.txt','r') as file:
		#credls=json.loads(file.read())

		
	with open('bfile.txt','r') as file:
		t_credls=json.loads(file.read())
		credls['bearer_key']=t_credls['bearer_key']

	response=getSearches(credls)
	#print("reponse code is {}".format(response.status_code))
	if (int(response.status_code)==403):
		credls['bearer_key']=getBearerToken(credls)
		print("Updated Bearer key")
		response=getSearches(credls)
	response=json.loads(response.content)
	i=0
	search_list=[]
	for search in response['searches']:
		i=i+1
		print ("{}. Search id : {}  Seach name : {}".format(i,search['search_id'],search['name']))
		search_list.append(search['search_id'])
	choice=int(input("Pick one search : "))
	data=dt.getLink(credls,search_list[choice-1],"2018-12-01T01:00:00","2019-01-15T01:00:00")
	res=data['response']
	document_count=data['document_count']
	res=json.loads(res)
	data_link=res['onetime_export']['data_url']
	print(data_link)
	export_id=res['onetime_export']['id']
	export_company=res['onetime_export']['company_name']

	# Getting company name here.
	


	company_name='samsung';
	export_name=input('Type a name for export :')
	status=dt.checkStatus(credls,export_id,document_count)
	if status:
		print("Data link is generated at {} \n with id {}".format(data_link,export_id))
		urls=clasTranslate(data_link,company_name)

		# =============================== DATABASE PART ======================================
		exist=sql.check_exist(company_name)
		# Checking weather company exists or not.
		if not exist: 
			sql.CreateCompanyTable(company_name)

		sql.addLog(company_name,export_id,export_name,data_link,urls['translated_url'],urls['clustered_url'],int(document_count))

		

		#print(urls)
	else :
		print('Request Timed out! Export Api is taking too long to respond.')


	
















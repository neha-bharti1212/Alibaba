import requests
import base64
import getpass
import json
import psql as sql


def DeleteCredls(client_id,email,password):
	string=email+':'+password
	encoded_key=base64.b64encode(string.encode())
	encoded_key=encoded_key.decode('utf-8')
	print(encoded_key)

	#print("Credls are {} and {} and {} \n".format(email_id,pswd,encoded_key))


	headers = {
    'Accept': 'application/json',
    'user-key': '0dbc77732948761d0dc2a4bbcabf2f0a',
    'Authorization': 'Basic '+encoded_key,
	}

	response = requests.delete('https://api.meltwater.com/oauth2/clients/'+client_id, headers=headers)
	print('from delete reqest {}'.format(response.status_code))

	#res=json.loads(response.content)
	#print('printing error from delete credentials \n{}'.format(res))
	#status_code=res['errors'][0]['title']
	#client_id=res['errors'][0]['meta']['client_id']
	
	

	


	

	
def checkStatus(status):
	if status == 'Client already exists.':
		return ('Exists')
		#Deleting existing credetinals and generating again.
	if status == 'Unauthorized.':
		return ('The credentials you are using are invalid.')
	if status == 'Entitlement missing.':
		return ('You are missing a required entitlement. Please, contact your sales representative to add the necessary entitlement to your Meltwater account.')
	if status=='Failed to handle request.':
		return ('Failed to handle client credentials request, unsupported.')


def createCreds(email_id,pswd):

	string=email_id+':'+pswd
	encoded_key=base64.b64encode(string.encode())
	encoded_key=encoded_key.decode('utf-8')

	#print("Credls are {} and {} and {} \n".format(email_id,pswd,encoded_key))


	headers = {
	    'Content-Type': 'application/json',
	    'Accept': 'application/json',
	    'user-key': '0dbc77732948761d0dc2a4bbcabf2f0a',
	    'Authorization': 'Basic '+encoded_key,
	}

	response = requests.post('https://api.meltwater.com/oauth2/clients', headers=headers)
	res=json.loads(response.content)
	print(res)
	#status_code=res['errors'][0]['title']
	

	if response.status_code==201:
		print("Client ID and Client Secret ID succefulyl generated.\n Client ID : {} 	Client Secret ID : {}".format(res['client_id'],res['client_secret']))
		return {'message':'Succesfully recieved credentials','client_id':res['client_id'],'client_secret':res['client_secret']}

	if 'errors' in res:
		message=res['errors'][0]['title']
		if message =='Unauthorized.':
			return {'message':'Unauthorized'}
		elif message=='Entitlement missing.':
			return {'message':'Entitlement missing.'}
		elif message=='Failed to handle request.':
			return {'message':'Failed to handle request.'}
		

		status_message=checkStatus(message)


		if status_message == 'Exists':
			client_id=res['errors'][0]['meta']['client_id']
			print(client_id)




	

	return {'message':status_message,'client_id':client_id}







if __name__ == '__main__':
	email='bibin.benny@meltwater.com'#input("Enter you email :")
	pswd ='antonyvarghesebibin@5' #getpass.getpass('Password:')
	#res=createCreds(email,pswd)
	res=sql.if_exist('user_mail',email,'login_table')
	if(res['status']==True):
		res=credentials(email,)
		#Client id assosiated with that account exists in my database:

	#print(cur)
	
	

	if res['message'] == 'Exists':
		print('Cliend id already exists')
		# Regenerate again here.
		#DeleteCredls(res['client_id'],email,password)


	print(res['message'])
	









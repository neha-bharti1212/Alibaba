import requests
import json
import time






def getLink(credls,search_id,start_date,end_date):

	start_date=str(start_date)
	end_date=str(end_date)

	headers = {
	    'Content-Type': 'application/json',
	    'Accept': 'application/json',
	    'user-key': credls['user_key'],
	    'Authorization': 'Bearer '+credls['bearer_key'],
	}




	params = (
    ('start_date', start_date),
    ('end_date', end_date),
		)


	countRes=requests.get('https://api.meltwater.com/export/v1/searches/'+str(search_id)+'/count',headers=headers,params=params)
	countRes=json.loads(countRes.content)
	#print(countRes)
	if 'count' in countRes:
		document_count=countRes['count']['total']
	else :
		print('Error: Could not get count. ( Data.py)')


	print('Total number of documents is {}'.format(document_count))

	data ={
	  "onetime_export":
	   {
	  "search_ids": [search_id],
	  "start_date": str(start_date),
	  "end_date": str(end_date)
		}}


	
	response = requests.post('https://api.meltwater.com/export/v1/exports/one-time', headers=headers,data=json.dumps(data))
	#print("Respose code is {} and Responce message is: \n {}".format(response.status_code, str(response.content)))
	res=json.loads(response.content)
	link=res['onetime_export']['data_url']
	data={'response':response.content,'document_count':document_count}
	#print("The data Link is : {}".format(link))
	return data


def checkStatus(credls,export_id,document_count):

	condition=True
	temp_var=0
	counter=0;
	if document_count<10000:
		sleep_duration=5;
	else:
		sleep_duration=10;
	while (condition):
		counter=counter+1;
		if counter>50:
			break;
	

		headers = {
		    'Accept': 'application/json',
		    'user-key': credls['user_key'],
		    'Authorization': 'Bearer '+ credls['bearer_key'],
				}

		response = requests.get('https://api.meltwater.com/export/v1/exports/one-time/'+str(export_id), headers=headers)
		res=json.loads(response.content)
		status_message=res['onetime_export']['status']
		if status_message == "PENDING":
			temp_str='.'*temp_var
			temp_var=temp_var+1
			print("Status {} {}".format(status_message,temp_str),end="\r")
			condition=True
		elif status_message =="FINISHED":
			condition=False
			print("Status {}".format(status_message))
		time.sleep(sleep_duration)
	if status_message=="FINISHED":
		return True
	elif status_message=="PENDING":
		return False

		




if __name__ == '__main__':

	credls=[]
	with open('bfile.txt','r') as file:
		credls=json.loads(file.read())

	res=getLink(credls,5481861)
	res=json.loads(res)
	link=res['onetime_export']['data_url']
	export_Id=res['onetime_export']['id']
	
	status=checkStatus(credls,export_Id)
	if status:
		print("Data Link is {} and id is {}".format(link,export_Id))
	










import pandas as pd 
from threading import Thread
import six
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os

from queue import Queue

from google.cloud import translate
import datetime

from reports import *





def save_data(local_name,company_name,folder,filename):
	print('\nSaving data . . . ')
	s3 = boto3.client('s3')
	bucket = 'bibinimagebuckets'
	file_name =local_name
	key_name ='Data/'+company_name+'/'+folder+'/'+filename
	s3.upload_file(file_name, bucket, key_name)
	url = '{}/{}/{}'.format(s3.meta.endpoint_url, bucket, key_name)
	return url

def clasTranslate(csv_url,company_name):
	
	df=translates(csv_url)
	df=classify(df)
	#df.to_csv('final.csv',sep='\t')

	html_string=createReport(df)
	try:
		f =open('report.html','w', encoding="utf-8")
		f.write(html_string)
		f.close()
	except:
		print('Could not open file to save html data')

    #final_df=kmean(df_copy)
	print(df[['Translated Hit Sentence','Translated Headline']])
	time=str(datetime.datetime.now())

	# Saving data Locally (Output csv file) 
	df.to_csv('temp_data.csv',sep='\t')


	#clustered_url=save_data(final_df,company_name,time,'report.html')
	translated_url=save_data('temp_data.csv',company_name,time,'translated_data.csv')

	clustered_url=save_data('report.html',company_name,time,'Report.html')

	print(clustered_url)


	return {'clustered_url':clustered_url,'translated_url':translated_url}






def classify(df):

	print('Classifyin Text')

	texts=list([ str(row['Translated Headline'] + ' ' + row['Translated Hit Sentence']) for index,row in df.iterrows() ])
	q= Queue(maxsize=0)
	num_threads=min(100,len(texts))



	results=[{} for x in texts]


	threads=[]

	for i in range(len(texts)):

		q.put((i,texts[i]))

	for i in range(num_threads):

		worker=Thread(target=classify_text,args=(q,results))
		worker.setDaemon(True)
		worker.start()
	q.join()


	#print(*results,sep='\t')
	print('Classification is Done')

	translted=pd.Series(results)

	df['Category']=translted.values
	return df


def classify_text(q,results):

    # [START language_classify_text]
    while not q.empty():
    	work=q.get()

    	text=work[1]
    	index=work[0]

    	while len(text.split()) < 20:
    		text=text+' '+text

    	client = language.LanguageServiceClient()

    	if isinstance(text, six.binary_type):
    		text = text.decode('utf-8')

    	document = types.Document(
			content=text.encode('utf-8'),
			type=enums.Document.Type.PLAIN_TEXT)
    	try:
    		data= client.classify_text(document)
    		categories=data.categories

    		if not categories:
    			results[index]='unknown'   

    		else:
    			results[index]=categories[0].name
    		
    	except:
    		results[index]='unknown'  
    	q.task_done()
    	
    return True




def translates(csv_url):

	print('Translates Text')


	csv_url=csv_url+'&format=csv'

	ls_headline=[]
	ls_hitSentence=[]
	ls_categories=[]
	#s=requests.get('https://exports.meltwater.com/v1/one-time/138348?data_key=20258c12-e4bd-495e-8d30-1d4f47b48785&format=csv').content
	try:
		df=pd.read_csv(csv_url,sep='\t',encoding='utf-16')
	except:
		print('Could not oprn Link')
	print('Downloaded File')
	texts=list ([ list( [row['Headline'], row['Hit Sentence']]) for index,row in df.iterrows() ]) 

	'''
	for inner in texts:
		for items in inner:
			print('{} \t'.format(items))
		print('\n')
	'''
	q= Queue(maxsize=0)
	num_threads=min(100,len(texts))



	results=[{} for x in texts]


	threads=[]

	for i in range(len(texts)):

		q.put((i,texts[i]))

	for i in range(num_threads):

		worker=Thread(target=translate_text,args=(q,results))
		worker.setDaemon(True)
		worker.start()
	q.join()
	print('Tranlsation is Done')

	#print(*results,sep='\t')

	translted_headline=pd.Series([x[0] for x in results])
	translted_hitSentence=pd.Series([x[1] for x in results])


	df['Translated Headline']=translted_headline.values
	df['Translated Hit Sentence']=translted_hitSentence.values

	return df
	#Testing Purpose Code
	'''
	check=list(True if (row['Translated Headline'] == row['Translated Headline1']) else False for index,row in df.iterrows() )
	check2=list(True if (row['Translated Hit Sentence'] == row['Translated Hit Sentence1']) else False for index,row in df.iterrows() )
	print(*check,sep='\t')
	print('\n\n\n\n\n')
	print(*check2,sep='\t')
	'''



def translate_text(q,results):


    # [START language_classify_text]
    while not q.empty():
    	work=q.get()

    	text=work[1]
    	#print(text[1])
    	index=work[0]
    	translate_client = translate.Client()
    	target='en'
    	
    	try:
    		translation = translate_client.translate(
					    [text[0],text[1]],
					    target_language=target)
    		results[index][0]=translation[0]['translatedText']
    		results[index][1]=translation[1]['translatedText']
   
    		
    	except:
    		results[index][0]='unknown'
    		results[index][1]='unknown'  
    	q.task_done()
    return True





if __name__ == '__main__':
	
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/Neha/Downloads/key.json"
	clasTranslate('https://exports.meltwater.com/v1/one-time/163457?data_key=e34809eb-a355-46de-ac36-6fe69cc0b4fe','lolCompany')

	
	


	







	


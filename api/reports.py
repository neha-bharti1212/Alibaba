import pandas as pd 
from tabulate import tabulate
import collections
import matplotlib
import matplotlib.pyplot as plt
import datetime
import boto3






def save_data(local_name,filename):
	print('\nSaving data . . . ')
	s3 = boto3.client('s3')
	bucket = 'bibinimagebuckets'
	file_name =local_name
	key_name ='Images/'+filename
	s3.upload_file(file_name, bucket, key_name)
	temp='https://s3.amazonaws.com'
	url = '{}/{}/{}'.format(temp, bucket, key_name)
	return url



def pprint(df):
	print(tabulate(df, headers='keys', tablefmt='psql'))

def createReport(data):
	plt.rcParams.update({'font.size': 6})
	plt.rcParams.update({'figure.autolayout': True})

	#data=pd.read_csv('data.csv',sep='\t')

	data_temp=data

	print(list(data))

	data.drop_duplicates(subset ="Translated Hit Sentence",  keep = False, inplace = True)
	data=data.reset_index(drop=True)

	print('Printing data \n {}'.format(data))



	categories=data['Category']

	






	categories=categories.tolist()

	count=collections.Counter(categories)
	count=dict(count)
	df=pd.DataFrame.from_dict(count,orient='index',columns=['Count'])

	df=df.sort_values(by=['Count'],ascending=False)
	uni_categoris=df.index.unique()
	uni_categoris=uni_categoris.tolist()



	try:

		while 'unknown' in categories:
			categories.remove('unknown')
	except:
		print('Array not found')

	print('Before Removing {} \n After \n'.format(uni_categoris))

	try:
		uni_categoris.remove('unknown')
		#print(uni_categoris)
	except:
		print('no on known')


	categories_temp=categories
	print('categories \n{}\n'.format(uni_categoris))
	html= ''' '''





	#Limiting the number of top categories here. 
	categories_limit=3

	for category in uni_categoris[:categories_limit]:
		#print('===================\n')
		#print(category)
		#print(data[data['Category'] == category])

		category_df=data[data['Category'] == category]
		category_df=category_df.sort_values(by=['Reach'],ascending=False)
		num_articles=category_df.shape[0]
		category_df=category_df.head()



		
		#print(category_df.head()[['Translated Hit Sentence','Category','Reach']])

		html= html + '''
		<br>
		<h4  >
		'''+ category[1:] +''' <span class="badge badge-secondary">'''+ str(num_articles) +''' Articles</span>
		</h4>
		<br>
		'''
		for index, row in category_df.iterrows():
			html=html +'''
			

			<p  >
			'''+ str(row['Translated Headline']) +'''
			</p>
			<a href="#" class="badge badge-success">Reach :''' +str(row['Reach'])  +'''</a> 
			<a href="#" class="badge badge-success">Source : ''' +str(row['Source'])  +'''e </a> 
			<hr/>

			'''


		'''
		</p>
		<a href="#" class="badge badge-success">Reach : 50000</a> 
		<a href="#" class="badge badge-success">Source : WeChat</a>
		'''
		#print(html)


		#print('===================\n')


	categories[:]=[category.split('/')[-1] for category in categories]



	count=collections.Counter(categories)
	count=dict(count)




	'''
	for key, value in count.items():
		count[key]=[value]


	print(count)


	#print(count)

	'''
	df=pd.DataFrame.from_dict(count,orient='index',columns=['Count'])

	#print(df)



	ax = df.plot.bar( y='Count', rot=90,color='#00cb9a')
	#plt.show()
	try:
		plt.savefig('barchart.png')
	except:
		print('Cpi;d mpt save data chart image locally.')

	filename=str(datetime.datetime.now())
	filename=filename.replace(" ","")
	image_url=save_data('barchart.png',filename+'bar'+'.png')
	print(image_url)
	#PieChart

	shape=df.shape

	if shape[0]> 5:

		df=df.sort_values(by=['Count'],ascending=False)
		temp_df=df # With all values
		others = df['Count'].tolist()
		print(others)
		print(others[6:])
		sum_items=sum(others[6:])

		pie_df=df.head()
		pie_df.loc['Others']=sum_items


		labels=pie_df.index.values.tolist()
		sizes=pie_df['Count'].tolist()
		colors = ['#ef5350','#ab47bc','#ec407a','#66bb6a','#29b6f6','#bdbdbd']
		fig1, ax1 = plt.subplots()

		ax1.pie(sizes, colors = colors, labels=labels, autopct='%1.1f%%', startangle=90)

		#draw circle
		centre_circle = plt.Circle((0,0),0.70,fc='white')
		fig = plt.gcf()
		fig.gca().add_artist(centre_circle)
		# Equal aspect ratio ensures that pie is drawn as a circle
		ax1.axis('equal')  
		plt.tight_layout()
	
		try:
			plt.savefig('piechart.png')
		except:
			print('Cpi;d mpt save data chart image locally.')

		filename=str(datetime.datetime.now())
		filename=filename.replace(" ","")
		image_url=save_data('piechart.png',filename+'pie'+'.png')
		print(image_url)








	#image_url=save_data('barchart.png',filename+'.png')
	#print(image_url)
	





	############################################################################################################################
	html_string = '''

	<html>
	    <head>
	    	<link href="https://fonts.googleapis.com/css?family=Open+Sans|Oswald" rel="stylesheet">
	        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
	        <style>body{ margin:0 100; font-family: 'Open Sans', sans-serif;  }</style>
	        <style>
	        *{
  			 font-family: 'Roboto', sans-serif;;
				}
			H3{
				font-family: 'Roboto', sans-serif;;
				font-weight:600;
				color: #424242;
				
			}

			H1{
				font-weight:900;
				color: #424242;

			}
			.badge-secondary {
			  background-color: #f44336;
			}
			H4{
			color:#616161;
			font-weight:700;

			}
			.badge-success {
			  background-color: #607d8b;
			}

			p{
				color:#616161;
				font-weight:500;
				font-family: 'Roboto', sans-serif;;
			}
			</style>

	    </head>

	<body font-family: 'Open Sans', sans-serif;>
		
	<H1>
	Alibaba Reports
	</H1>
	<H5>
	Report generated on ''' +str(datetime.datetime.now())  + ''' 
	</H5>
	<br>
	<br>


	<H3>
	Categorical Data
	</H3>
	<img src=''' + image_url + ''' />


	<h3 >
	Top Categories
	</h3>
	''' + html + '''

	<br>
	<br>
	<br>

	</body>


	</html>

	'''



	#print(html_string)

	############################################################################################################################

	return html_string

	






	#plt.show()



	#print(categories)
	#print(categories.count())










#print(data)





#print(data[['Translated Hit Sentence','Category']])
if __name__ == '__main__':
	data=pd.read_csv('modi_data.csv',sep='\t')
	html_string=createReport(data)
try:
	f =open('report.html','w', encoding="utf-8")
	f.write(html_string)
	f.close()
except:
	print('Could not open file to save html data')
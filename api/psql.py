import psycopg2
from datetime import datetime as dt
import sys


def addCompany(companyid,companyname):

	try:
		conn = psycopg2.connect(database="testdb", user = "postgres", password = "12345", host = "localhost", port = "5432")
		#print ("Opened database successfully")
	except:
		print('Unable to connect to database')

	cur=conn.cursor()
	try:
		cur.execute("INSERT INTO companies (company_id,company_name) VALUES ('{}','{}')".format(companyid,companyname))
	except psycopg2.OperationalError as e:
		print('Unable to connect : {}'.format(e))

	conn.commit()
	conn.close()


def CreateCompanyTable(company_id):

	table_name=company_id+'_table'

	try:
		conn = psycopg2.connect(database="testdb", user = "postgres", password = "12345", host = "localhost", port = "5432")
		#print ("Opened database successfully")
	except:
		print('Unable to connect to database')

	cur=conn.cursor()
	try:
		addCompany(company_id,company_id)
	except:
		print('Error!')
		sys.exit()
	try:
		cur.execute('''CREATE TABLE {} (export_id varchar PRIMARY KEY,export_name varchar UNIQUE NOT NULL, created_on TIMESTAMP DEFAULT NOW(),exported_csv varchar NOT NULL,\
		 translated_csv varchar, clustered_data varchar, comments varchar DEFAULT NULL,document_count BIGINT NOT NULL)'''.format(table_name))
	except psycopg2.OperationalError as e:
		print('Unable to connect : {}'.format(e))
	


	conn.commit()
	conn.close()

def if_exist(coloumn_name,coloumn_value,table_name):

	try:
		conn = psycopg2.connect(database="testdb", user = "postgres", password = "12345", host = "localhost", port = "5432")
		#print("Opened database successfully")
	except:
		print('Unable to connect to database')

	cur=conn.cursor()

	try:
		cur.execute('''SELECT * FROM {} WHERE {}='{}' '''.format(table_name,coloumn_name,coloumn_value))
		row=cur.fetchall();
		if len(row)>0:
			return({'status':True,'row':row})
			
		else:
			return({'status':False,'row':None})
			#print(str(cur.fetchall()))
			#for row in cur.fetchall():
				#print(row)
			#return row
	except psycopg2.OperationalError as e:
		print('Error Finding existence {}'.format(e))

	finally:
		if(conn):
			conn.close()
	


def check_exist(company_id):
	try:
		conn = psycopg2.connect(database="testdb", user = "postgres", password = "12345", host = "localhost", port = "5432")
		#print("Opened database successfully")
	except:
		print('Unable to connect to database')

	cur=conn.cursor()

	try:
		cur.execute('''SELECT 1 FROM company WHERE company_id='{}' '''.format(company_id))
		if len((cur.fetchall())) >0:
			return True
		else:
			return False

	except psycopg2.OperationalError as e:
		print('Error Finding existence {}'.format(e))
	conn.close()
	


def addLog(company_name,export_id,export_name,exported_csv,translated_csv,clustered_data,document_count):
	try:
		conn = psycopg2.connect(database="testdb", user = "postgres", password = "12345", host = "localhost", port = "5432")
		#print ("Opened database successfully")
	except:
		print('Unable to connect to database')

	cur=conn.cursor()
	try:
		cur.execute('''INSERT INTO {} (export_id,export_name,exported_csv,translated_csv,clustered_data,document_count)\
		VALUES ('{}','{}','{}','{}','{}','{}')'''.format(company_name+'_table',export_id,export_name,exported_csv,translated_csv,clustered_data,document_count))
		print('Log created successfully')
	except psycopg2.OperationalError as e:
		print('Unable to connect : {}'.format(e))

	conn.commit()
	conn.close()
	
	
def addUser(email,client_key):
	try:
		conn = psycopg2.connect(database="testdb", user = "postgres", password = "12345", host = "localhost", port = "5432")
		#print ("Opened database successfully")
	except:
		print('Unable to connect to database')

	cur=conn.cursor()
	try:
		cur.execute('''INSERT INTO {} (user_mail,client_key)\
		VALUES ('{}','{}') ON CONFLICT (user_mail) DO UPDATE \
		SET client_key = '{}' '''.format('login_table',email,client_key,client_key))
		print('User Log created successfully')
	except psycopg2.OperationalError as e:
		print('Unable to connect : {}'.format(e))

	conn.commit()
	conn.close()




if __name__ == '__main__':
	print('hi')


	
	#addCompany('alibaba','fsdf2323')
	
		#Do FOO here.
	#CreateCompanyTable('sonny','sdfsaflk')


	




	













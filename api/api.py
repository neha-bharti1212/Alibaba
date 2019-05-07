from flask import Flask
from flask import request
from flask import make_response
from flask import Response,jsonify
from flask import Flask, render_template
import json
import os

from main import *
import data as dt








app = Flask(__name__)

user_key='<user key>'


@app.route('/login',methods=['GET','POST'])
def myclustering():
    print('here')
    
    data=request.form.to_dict(flat=False)
    print(data)
    str_data=str(data).split("'")
    data=str_data[1];
    data=json.loads(data)
    email=data['username']
    password=data['password']
    key=login(email,password,user_key)
    if(key['message']!='good'):
        print(key['message'])
        res={'message':key['message']}
        return jsonify(res)
        sys.exit()
    key=key['client_key']
    res={'message':'good','client_key': key}
    return jsonify(res)

@app.route('/clustering',methods=['GET','POST'])
def createReport():
    
    data=request.form.to_dict(flat=False) 
    data=str(data).split("'")
    data=data[1]
    data=data[1:-1]
    data=data.split('[')
    data=data[1].split(']')
    bearer_key=data[-1]+'}'
    bearer_key=json.loads(bearer_key)
    bearer_key=bearer_key['bearer_key']
    bearer_key= bearer_key.replace('Bearer ','')

    tdata=data;
    data=json.loads(data[0])
    print(data)
    print('\n\n\n')
    search_id=data['search_id']
    print('\n\n\n')
    print('Printinf search ids = {}'.format(search_id))
    print('\n\n\n')
    tdata=tdata[1]
    tdata=tdata[2:]
    tdata=tdata.replace('{','').replace('}','')
    tdata='{ '+tdata + '}'
    tdata=json.loads(tdata)
    start_date= tdata['secondCtrl']
    print(start_date)
    end_date=tdata['thirdCtrl']
    print(end_date)
    export_name=tdata['forthCtrl']
    print(export_name)
    


    credls={}
    credls['user_key']=user_key
    credls['bearer_key']=bearer_key
    print(credls['bearer_key'])
    data=dt.getLink(credls,data['search_id'],start_date,end_date)
    res=data['response']
    document_count=data['document_count']
    temp_count = document_count
    res=json.loads(res)
    data_link=res['onetime_export']['data_url']
    print(data_link)
    export_id=res['onetime_export']['id']
    export_company=res['onetime_export']['company_name']
    company_name='fitbit'
    export_name=export_name
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="<Google credential>"
    status=dt.checkStatus(credls,export_id,document_count)
    if status:
        print("Data link is generated at {} \n with id {}".format(data_link,export_id))
        urls=clasTranslate(data_link,company_name)
        # =============================== DATABASE PART ======================================
        exist=sql.check_exist(company_name)
        # Checking weather company exists or not.
        if not exist: 
            sql.CreateCompanyTable(company_name)
            
        sql.addLog(company_name,export_id,export_name,data_link,urls['translated_url'],urls['clustered_url'],int(temp_count))
        return urls['clustered_url']

    else :
        print('Request Timed out! Export Api is taking too long to respond.')
        return jsonify({'url':'badurl'})




    



if __name__ == '__main__':
    port=int(os.getenv('PORT',5000))
    app.run(debug=True,port=port,host='0.0.0.0')

import urllib3, json, array, csv, os
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd

http = urllib3.PoolManager()

project_key = input("enter the project key :")

with open('repository.csv','rt') as f:
    data = csv.reader(f)
    for row in data:
        url = "https://gitlab.com/api/v4/projects/"+str(row[1])+"/repository/branches"
        response = http.request('GET', url , headers={"PRIVATE-TOKEN" : project_key})
        print("==============")
        print(str(row[0]))
        if response.status == 200:
            print("status: success")
        else:
            print("  status: Failure")
        print("==============")
        #========data===========
        soup = BeautifulSoup(response.data, "html.parser")
        #========json_data===========
        json_data = json.loads(soup.text)
        #========indi_json_data===========
        for i in json_data:
            print("->"+str(i['name']))
            if response.status == 200:
                print("  status: success")
            else:
                print("  status: Failure")
            url = "https://gitlab.com/api/v4/projects/"+str(row[1])+"/repository/commits?ref_name="+str(i['name'])+"&per_page=5"
            response = http.request('GET', url , headers={"PRIVATE-TOKEN" : project_key})
            soup = BeautifulSoup(response.data, "html.parser")
            json_data = json.loads(soup.text)
            #
            #specify the path here
            #
            path = os.getcwd()+'\\result\\'
            pd.read_json(json.dumps(json_data)).to_csv(path+str(row[0])+'_'+str(i['name'])+'.csv', columns=['id',  'title',  'committer_name', 'committer_email', 'committed_date']) 




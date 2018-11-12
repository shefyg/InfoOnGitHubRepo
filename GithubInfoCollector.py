import requests
import json
import datetime
from time import gmtime, strftime
import os.path
from shutil import copyfile

class GithubInfoCollector:

    githubProjUrl=''
    jsonDataFilePath=''

    def __init__(self, url, jsonFilePath):

        self.githubProjUrl = url
        self.jsonDataFilePath = jsonFilePath



    def collectCurrentData(self):

        '''
            Getting data from GitHub as text
        '''

        response = requests.get(self.githubProjUrl)
        txt = response.content.decode("utf-8")

        '''
            Preparing old data, so new data can be added
        '''

        allData = []
        if (os.path.isfile(self.jsonDataFilePath)):
            with open(self.jsonDataFilePath) as json_file:
                allData = json.load(json_file)

        '''
             Getting current Data
        '''

        data = {}
        data['repoUrl'] = self.githubProjUrl
        data['dateAndTime'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())


        '''
            Number of users Watching the GitHub project
        '''

        tmpInd = txt.find("users are watching this repository")
        firstInd, lastInd = self.getFirstAndLastIndsOfStringInText(tmpInd, txt)
        watchersMsg = txt[firstInd + 1:lastInd]
        data['watchersNum'] = watchersMsg.split(' ')[0]


        '''
            Number of users that have stared this GitHub project
        '''

        tmpInd = txt.find("users starred this repository")
        firstInd, lastInd = self.getFirstAndLastIndsOfStringInText(tmpInd, txt)
        staredMsg = txt[firstInd + 1:lastInd]
        data['staredNum'] = staredMsg.split(' ')[0]


        '''
            Number of users that have Forked this GitHub project
        '''

        tmpInd = txt.find("users forked this repository")
        firstInd, lastInd = self.getFirstAndLastIndsOfStringInText(tmpInd, txt)
        forkedMsg = txt[firstInd + 1:lastInd]
        data['forkedNum'] = forkedMsg.split(' ')[0]

        '''
            Adding current data to all data and saving          
        '''
        allData.append(data)
        with open(self.jsonDataFilePath, 'w') as outfile:
            json.dump(allData, outfile, indent=4)


    def getFirstAndLastIndsOfStringInText(self, midInd, txtStr):
        firstInd = midInd
        lastInd = midInd
        while (txtStr[firstInd] != '"'):
            firstInd -= 1
        while (txtStr[lastInd] != '"'):
            lastInd += 1

        return firstInd,lastInd

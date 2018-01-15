import requests
import logging
import datetime, time, random
from stocklist import Roster
from model import updateTable
payload = ""
queryIndex = []

jsonData = {}
jsonAggregateData = []

now = datetime.datetime.now().strftime("%m-%d-%Y %H:%M")

APIToken = '' # *****Hide in production*****
from TestjsonData import batch1, batch2 # debug only


# Initiate Logging
logging.basicConfig(filename='APILog.log', level=logging.CRITICAL) # Use to filter logging events


def queryConstructor():
    iterativeCycles = 0
    indexIncrement = 0
    # Roster = ["MSFT", "GOOG", "YAHOO"] # Debugging Use Only
    while iterativeCycles <= 13:
        targetBatch = Roster[0+indexIncrement: 100+indexIncrement]
        targetBatch = ','.join(map(str, targetBatch))
        payload = 'https://www.alphavantage.co/query?function=BATCH_STOCK_QUOTES&symbols=%s&apikey=%s' % (targetBatch, APIToken,)
        #print payload # debug use only
        queryIndex.append(payload)
        iterativeCycles += 1
        indexIncrement += 100


def grabData():
    now = datetime.datetime.now().strftime("%m-%d-%Y %H:%M")
    for query in queryIndex:
        r = requests.get(query)
        if r.status_code == 200:
            jsonData = r.json()
            loopVariant = 0
            for item in range(len(jsonData["Stock Quotes"])):
                jsonAggregateData.append(jsonData["Stock Quotes"][loopVariant])
                loopVariant += 1
        else:
            logging.debug(now + "Data API call unsucessful--status code error")
        time.sleep(15+random.randint(1,10))


def refreshData():
    updateTable(jsonAggregateData)


def jsonParser(): # debug use only
    stockIndex = 0
    for item in range(len(batch1["Stock Quotes"])):
        jsonAggregateData.append(batch1["Stock Quotes"][stockIndex])
        stockIndex += 1
    print jsonAggregateData
    updateTable(jsonAggregateData)



if __name__ == '__main__':
    logging.info(now + "New Data Pull Job Started")
    queryConstructor()
    grabData()
    # jsonParser()
    refreshData()
import sqlite3
from stocklist import Roster

targetTable = 'equityData.db'
createTable = """CREATE TABLE TargetStocks(
                                            ticker text,
                                            price1 real,
                                            price2 real,
                                            price3 real,
                                            price4 real,
                                            price5 real,
                                            price6 real,
                                            price7 real,
                                            volume1 integer,
                                            volume2 integer,
                                            volume3 integer,
                                            volume4 integer,
                                            volume5 integer,
                                            volume6 integer,
                                            volume7 integer
                                            );"""

def buildSQLtable():
    try:
        conn = sqlite3.connect(targetTable)
        c = conn.cursor()
        c.execute(createTable)
        tickerList = []
        for ticker in Roster:
            tickerList.append([ticker, None, None, None, None, None, None, None, None, None, None, None, None, None, None])
        for tickerdata in tickerList:
            c.execute("INSERT INTO TargetStocks VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", tickerdata)
        conn.commit()
        conn.close()
    except Exception as e:
        print "table creation/connection unsuccessful"
        print str(e)




def updateTable(payload):
    try:
        conn = sqlite3.connect(targetTable)
        c = conn.cursor()
        # offset prior indices
        c.execute("UPDATE TargetStocks SET price1 = price2, volume1 = volume2;")
        c.execute("UPDATE TargetStocks SET price2 = price3, volume2 = volume3;")
        c.execute("UPDATE TargetStocks SET price3 = price4, volume3 = volume4;")
        c.execute("UPDATE TargetStocks SET price4 = price5, volume4 = volume5;")
        c.execute("UPDATE TargetStocks SET price5 = price6, volume5 = volume6;")
        c.execute("UPDATE TargetStocks SET price6 = price7, volume6 = volume7;")
        #load in fresh data
        for stock in payload:
            key = stock["1. symbol"]
            price = stock["2. price"]
            if stock["3. volume"] == '--':
                volume = 0
            else:
                volume = stock["3. volume"]
            parameters = [price, volume, key]
            c.execute("UPDATE TargetStocks SET price7 = ?, volume7 = ? WHERE ticker = ?;", parameters)
        conn.commit()
        conn.close()
    except Exception as e:
        print "table update failed"
        print str(e)


if __name__ == '__main__':
    buildSQLtable()

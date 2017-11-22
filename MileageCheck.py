import pymysql
import util
import ssl
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
def dbinit(databaseinfo=util.DEFAULT_REMOTE_DATABASE):
    db = pymysql.connect(databaseinfo.host,
                         databaseinfo.user_name,
                         databaseinfo.authentication_string,
                         databaseinfo.database_name)
    return db

def getAllIllegalData(db):
    cursor = db.cursor()
    sqlCommand = """SELECT * FROM airline
                    WHERE kilos = 0"""
    cursor.execute(sqlCommand)
    return cursor.fetchall()

def getAllFlightData(db):
    cursor = db.cursor()
    sqlCommand = """SELECT * FROM airline"""
    cursor.execute(sqlCommand)
    return cursor.fetchall()

def getMatchedCity(db,IATA):
    cursor = db.cursor()
    sqlCommand = """SELECT * FROM airport
                    WHERE IATA = \'%s\'"""%IATA
    cursor.execute(sqlCommand)
    a = cursor.fetchall()
    if a == 0:
        raise util.NullResultException("MileageCheck.getMatchedCity: no matched city for airport: "+IATA)
    return a

def getOnlineMileage(IATA1,IATA2):
    url = """http://www.webflyer.com/travel/mileage_calculator/getmileage.php?city=%s&city=%s&city = & city = & city = & city = & bonus = 0 & bonus_use_min = 0 & class_bonus = 0 & class_bonus_use_min = 0 & promo_bonus = 0 & promo_bonus_use_min = 0 & min = 0 & min_type = m & ticket_price = """%(IATA1,IATA2)
    gcontext = ssl._SSLContext(ssl.PROTOCOL_SSLv23)
    html = urlopen(url,context=gcontext)
    bs = BeautifulSoup(html,'lxml')

    warning = bs.find_all('td',{'align':"CENTER",'valign':"TOP"})
    for suggestion in warning:
        temp = suggestion.find('b')
        if temp:
            raise util.QueryException(temp.text+" not recorded in the online mileage calculator")
    rows = bs.find_all("tr",{'class':'row_odd_bg'})
    result = []
    for row in rows:
        datas = row.find_all('td')
        texts = []
        for data in datas:
            texts.append(data.text)
        if 'Distance' in texts:
            print(texts)
            for text in texts:
                if re.match('[0-9\.]+ miles',text):
                    numric = re.sub('miles','',text)
                    result.append(float(numric))
    mileage = 'NULL'
    try:
        mileage = min(result)
    except ValueError:
        print(IATA1+' '+IATA2)
    return mileage

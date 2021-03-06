"""
This modula provides generals utilities to the project
"""

import random
import datetime
import pymysql

def select_on_prob(item_list, prob_list):
    """
    select an item form item_list based on the probability provided in prob_list.
    note that the element of item_list and prob_list should be one to one match
    :param item_list: a list of items
    :param prob_list: a list of numeric values, each one element represents the probability of choosing the corresponding
            item
    :return: the item selected
    """
    if not len(item_list) == len(prob_list):
        raise Exception('util: selct_on_prob func: invalid input')
    total = 0
    for num in prob_list:
        total += num
    flag = random.uniform(0,total)
    cumulative_probability = 0.0
    for i in range(0,len(item_list)):
        cumulative_probability += prob_list[i]
        if flag < cumulative_probability:
            return item_list[i]

def getTomorrowDatetime(current):
    """
    returns the datetime object of the next day 0hrs,0min,0sec of the current datetime instance
    :param current: a current datetime
    :return: datetime object
    """
    year = current.year
    month = current.month
    day = current.day
    dateStr = "%d:%d:%d %d-%d-%d"%(year,month,day,0,0,0)
    return datetime.datetime.strptime(dateStr,"%Y:%m:%d %H-%M-%S") + datetime.timedelta(days=1)


import unicodedata
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

class databaseinfo:
    def __init__(self, host, user_name, authentication_string, database_name):
        self.host = host
        self.user_name = user_name
        self.authentication_string = authentication_string
        self.database_name = database_name

DEFAULT_REMOTE_DATABASE = databaseinfo(host='124.218.32.37',user_name='admin4',authentication_string='admin4',database_name='test')

class logutil:
    def __init__(self, logfileName):
        self.logfileName = logfileName
    def log(self,str,header = 'RoloSong'):
        header = '['+header+']'
        with open(self.logfileName,'a') as file:
            file.write(header+str)

class ANAFlightException(Exception):
    logfile = 'ANAFlightExceptionLog.txt'
    logAgent = logutil(logfile)
    def log(self):
        self.logAgent.log(self(self.args),self.__class__)
    pass
class NullResultException(ANAFlightException):
    pass
class QueryException(ANAFlightException):
    pass
class JumpingException(ANAFlightException):
    pass

def dbinit(databaseinfo=DEFAULT_REMOTE_DATABASE):
    db = pymysql.connect(databaseinfo.host,
                         databaseinfo.user_name,
                         databaseinfo.authentication_string,
                         databaseinfo.database_name)
    return db
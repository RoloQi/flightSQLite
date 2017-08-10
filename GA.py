import BFS
import sql
from random import randint
import datetime

TIME_CONFLICT_WEIGHT = 1000
DESTINATION_CONFLICT_WEIGHT = 1000
DEPARTURE_CITY = None
ARRIVAL_CITY = None

class Node:
    """
    Node class for Genetic Algorithm,
    generate a table for each day
    Each table contains an entity for each flight and a bool value representing wether to take it
    """
    def __init__(self, startDate, endDate):
        self.startDate = startDate
        self.endDate = endDate
        self.tables = []
        for i in range(0,(self.endDate-self.startDate).days+1):
            self.tables.append(self.table(self.startDate+datetime.timedelta(days = i)))

    def __lt__(self, other):
        if self.eval() < other.eval():
            return True
        return False
    def __eq__(self, other):
        if self.eval() == other.eval()\
           and self.startDate == other.startDate\
           and self.endDate == other.endDate:
            return True
        return False


    def printInfo(self):
        for a in self.tables:
            print(a.getTableDate())

    def eval(self):
        result = 0
        for ele in self.tables:
            result += ele.eval()
        for i in range(0, self.tables.__len__()):

            if i+1 < self.tables.__len__():
                if not BFS.earlyTo(self.tables[i].getFinalFlight().arrivalTime,
                                   self.tables[i+1].getFirstFlight().departureTime):
                    result -= TIME_CONFLICT_WEIGHT
                if not self.tables[i].getFinalFlight().destination == self.tables[i+1].getFirstFlight().departureCity:
                    result -= DESTINATION_CONFLICT_WEIGHT
        if not self.tables[0].getFirstFlight().departureCity == DEPARTURE_CITY:
            result -= DESTINATION_CONFLICT_WEIGHT
        if not self.tables[-1].getFinalFlight().destination == ARRIVAL_CITY:
            result -= DESTINATION_CONFLICT_WEIGHT
        if not BFS.earlyTo(self.startDate,self.tables[0].getFirstFlight().departureTime):
            result -= TIME_CONFLICT_WEIGHT
        if not BFS.earlyTo(self.tables[-1].getFinalFlight().arrivalTime,self.endDate):
            result -= TIME_CONFLICT_WEIGHT
        return result

    class table:

        def __init__(self,currentDate):
            self.currentDate = currentDate
            flights = sql.FlightDBManager().getEntireFlightList()
            self.flightTable = []
            for f in flights:
                flight = BFS.flight(f[2],f[3],f[5],f[4],f[1],f[0],currentDate)
                self.flightTable.append(self.tableElement(flight,randint(0,1)))
            self.earliestFlight = None
            self.latestFlight = None
        def eval(self):
            result = 0
            self.earliestDate = datetime.datetime(year=self.currentDate.year, month= self.currentDate.month, day=self.currentDate.day,
                                                  hour=0, minute=0, second=0)
            self.earliestDate = self.earliestDate + datetime.timedelta(days = 1)
            self.latestDate = datetime.datetime(year=self.currentDate.year,month= self.currentDate.month,day=self.currentDate.day,
                                            hour=0,minute=0,second=0)

            for i in range(0,self.flightTable.__len__()):
                if self.flightTable[i].taken:
                    result += self.flightTable[i].flight.Mileage
                    if BFS.earlyTo(self.flightTable[i].flight.departureTime, self.earliestDate):
                        self.earliestDate = self.flightTable[i].flight.departureTime
                        self.earliestFlight = self.flightTable[i].flight
                    if BFS.earlyTo(self.latestDate,self.flightTable[i].flight.arrivalTime):
                        self.latestDate = self.flightTable[i].flight.arrivalTime
                        self.latestFlight = self.flightTable[i].flight

                    for ii in range(i,self.flightTable.__len__()):
                        if self.flightTable[ii].taken:
                            if BFS.earlyTo(self.flightTable[i].flight.arrivalTime,
                                           self.flightTable[ii].flight.departureTime):
                                result -= TIME_CONFLICT_WEIGHT
                            if not self.flightTable[i].flight.destination == self.flightTable[ii].flight.departureCity:
                                result -= DESTINATION_CONFLICT_WEIGHT
            return result

        def getTableDate(self):
            return self.currentDate
        def getFirstFlight(self):
            return self.earliestFlight
        def getFinalFlight(self):
            return self.latestFlight
        def test(self):
            for f in self.flightTable:
                print(f.flight.flightNO)
                print(f.taken)
        def compareTableElements(self,other):
            for a in range(0, self.flightTable.__len__()):
                print(self.flightTable[a].flight.flightNO)
                print(other.flightTable[a].flight.flightNO)

        class tableElement:
            flight = None
            taken = False
            def __init__(self, flight, taken):
                self.flight = flight
                self.taken = taken

a = Node.table(datetime.datetime.now())
print(a.eval())

b = Node(datetime.datetime.now(),datetime.datetime.now()+datetime.timedelta(days = 5))
print(b.eval())

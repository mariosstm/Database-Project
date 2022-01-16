import tkinter
from tkinter import ttk
import tkcalendar
import datetime
import sqlite3
import geopy.distance
import random
import usefulFunctions as myFuncs
#import handleDataBase as hdb


#Δημιουργία Time picker, κληρονομει Frame
class myTimePicker(tkinter.Frame):
    def __init__(self,root,*args,**kwrds):
        tkinter.Frame.__init__(self,root,*args,**kwrds)
        myfont = "helvetica 12"
        thours = [str(i//10) + str(i%10) for i in range(24)]
        tmins = ['00','15','30','45']
        textvar = tkinter.StringVar()
        w = 2
        self.hours = tkinter.Spinbox(self,values = thours, font = myfont,textvariable = textvar, width = w, state = "readonly")
        self.mins = tkinter.Spinbox(self, values = tmins, increment = 15, font = myfont, width = w, state = "readonly")
        textvar.set('12')

        self.hours.grid(row = 0, column = 0)
        tkinter.Label(self,text = ":", font = "helvetica 15").grid(row = 0, column = 1)
        self.mins.grid(row = 0, column = 2)



#Option Menu για πολεις, κληρονομει OptionMenu
class myCityOptionMenu(tkinter.OptionMenu):
    def __init__(self,root,startingVal,**kwargs):
        self.airports = {"Αθήνα":'ATH', "Λονδίνο":'LHR', "Μάντσεστερ":'MAN', "Παρίσι":'CDG', "Άμστερνταμ":'AMS', "Κωνσταντινούπολη":'IST', "Φρανκφούρτη":'FRA', "Μόναχο":'MUC', "Μαδρίτη":'MAD', "Βαρκελώνη":'BCN', "Ρώμη":'FCO', "Ζυρίχη":'ZRH', "Βρυξέλλες":'BRU', "Δουβλίνο":'DUB', "Μόσχα":'DME', "Όσλο":'OSL', "Βιέννη":'VIE', "Νέα Υόρκη":'JFK', "Λος Άντζελες":'LAX', "Σικάγο":'ORD'}
        self.cities = [i for i in self.airports.keys()]
        self.cityChoice = tkinter.StringVar()
        self.cityChoice.set(startingVal)
        tkinter.OptionMenu.__init__(self,root,self.cityChoice,*(self.cities),**kwargs)
        self.configure(width = 16)



#SpinBox για πυλες 
class myGateSpinbox(tkinter.Spinbox):
    def __init__(self,root, **kw):
        tkinter.Spinbox.__init__(self,root,from_ = 1, to_ = 100, font = 'helvetica 11', width = 3,**kw)
        


#Frame για αρχικο και τελικο προορισμο
class myFrame(tkinter.Frame):
    def __init__(self,root,isStartingPoint,*args,**kwrds):
        tkinter.Frame.__init__(self,root,*args,**kwrds)
        self.isStartingPoint = isStartingPoint
        if self.isStartingPoint:
            text1 = "Από: "
            text2 = "Ώρα αναχώρησης: "
            startVal = 'Αθήνα'
        else :
            text1 = "Προς: "
            text2 = "Ώρα Άφιξης: "
            startVal = 'Μαδρίτη'
            
        myfont = 'helvetica 12'
        
        tkinter.Label(self, text = text1,width = 7, font = myfont).grid(row = 0, column = 0)
        
        self.cityMenu = myCityOptionMenu(self,startVal)
        self.cityMenu.grid(row = 0, column = 1)

        tkinter.Label(self, text =  text2,width = 20, font = myfont).grid(row = 0, column = 2)

        self.timePicker = myTimePicker(self)
        self.timePicker.grid(row = 0, column = 3)

        if isStartingPoint:
            tkinter.Label(self, text = 'Πύλη: ', font = myfont).grid(row = 0, column = 4)

            self.gate = myGateSpinbox(self)
            self.gate.grid(row = 0, column = 5)

    def getValues(self):
        values = {}
        if self.isStartingPoint:
            timeText = "departure time"
            values["gate"] = str(int(self.gate.get())%100)
        else:
            timeText = "arrival time"
        
        values["city"] = self.cityMenu.cityChoice.get()
        values[timeText] = self.timePicker.hours.get() + ':' + self.timePicker.mins.get()
        

        return values



#Frame για ενδιαμεσες στασεις
#Χωρίζεται σε 2 υποFrame
class myStationFrame(tkinter.Frame):
    def __init__(self,root,oneOrTwo,*args,**kwrds):
        tkinter.Frame.__init__(self,root,*args,**kwrds)
        myfont = 'helvetica 12'
        
        
        self.leftFrame = tkinter.Frame(self)
        self.midFrame = tkinter.Frame(self)
        self.rightFrame = tkinter.Frame(self)
        self.leftFrame.pack(expand = 1, fill = 'x',side = 'left')
        self.midFrame.pack(expand = 1,fill = 'both', side = 'left')
        self.rightFrame.pack(expand = 1, fill = 'x',side = 'right')

        #Αριστερο Frame
        tkinter.Label(self.leftFrame, text = "Στάση "+str(oneOrTwo)+":",width = 7, font = myfont).grid(row = 0, column = 0)

        if oneOrTwo == 1:
            city = "Ρώμη"
        else:
            city = "Ζυρίχη"
        self.cityMenu = myCityOptionMenu(self.leftFrame,city)
        self.cityMenu.grid(row = 0, column = 1)

        #Μεσαίο Frame
        tkinter.Label(self.midFrame,width = 20, text =  "Ώρα Άφιξης: ", font = myfont).grid(row = 0, column = 0)
        self.timePickerArrive = myTimePicker(self.midFrame)
        self.timePickerArrive.grid(row = 0, column = 1)
        tkinter.Label(self.midFrame,width = 20, text =  "Ώρα Αναχώρησης: ", font = myfont).grid(row = 1, column = 0)
        self.timePickerLeave = myTimePicker(self.midFrame)
        self.timePickerLeave.grid(row = 1, column = 1)


        #Δεξί Frame
        tkinter.Label(self.rightFrame, text = 'Πύλη: ', font = myfont).grid(row = 0, column = 0)
        self.gate = myGateSpinbox(self.rightFrame)
        self.gate.grid(row = 0, column = 1)

        
    def getValues(self):
        values = {}
        values["city"] = self.cityMenu.cityChoice.get()
        values["arrival time"] = self.timePickerArrive.hours.get() + ':' + self.timePickerArrive.mins.get()
        values["departure time"] = self.timePickerLeave.hours.get() + ':' + self.timePickerLeave.mins.get()
        values["gate"] = str(int(self.gate.get())%100)
        
        return values

#Εδω φτιάχνεται η φόρμα εισαγωγής
class FlightForm:
    def __init__(self, root,dbHandler):
        self.root = root
        self.dbHandler = dbHandler
        self.airports = {"Αθήνα":{"IATA":'ATH', "coordinates":(37.9356509,23.9462269)}, "Λονδίνο":{"IATA":'LHR' ,"coordinates":(51.4954157,-0.4524431)},
                         "Μάντσεστερ":{"IATA":'MAN' ,"coordinates":(53.3557446,-2.2786987)}, "Παρίσι" :{"IATA":'CDG', "coordinates":(49.0096739,2.545777)},
                         "Άμστερνταμ":{"IATA":'AMS', "coordinates":(52.3105419,4.7660857)}, "Κωνσταντινούπολη":{"IATA":'IST', "coordinates":(41.2598532,28.7404678)},
                         "Φρανκφούρτη":{"IATA":'FRA', "coordinates":(50.037936,8.5599631)}, "Μόναχο":{"IATA":'MUC', "coordinates":(48.3509719,11.774246)},
                         "Μαδρίτη":{"IATA":'MAD', "coordinates":(40.4983322,-3.5675982)}, "Βαρκελώνη":{"IATA":'BCN', "coordinates":(41.297449,2.0811054)},
                         "Ρώμη":{"IATA":'FCO', "coordinates":(41.8034314,12.2497041)}, "Ζυρίχη":{"IATA":'ZRH', "coordinates":(47.4612388,8.5513089)},
                         "Βρυξέλλες":{"IATA":'BRU', "coordinates":(50.9010024,4.4833857)}, "Δουβλίνο":{"IATA":'DUB', "coordinates":(53.4264513,-6.2520985)},
                         "Μόσχα":{"IATA":'DME', "coordinates":(55.4103099,37.9002626)}, "Όσλο":{"IATA":'OSL', "coordinates":(60.1975527,11.0982265)},
                         "Βιέννη":{"IATA":'VIE', "coordinates":(48.1126161,16.5733252)}, "Νέα Υόρκη":{"IATA":'JFK', "coordinates":(40.6413153,-73.780327)},
                         "Λος Άντζελες":{"IATA":'LAX', "coordinates":(33.9415933,-118.4107187)}, "Σικάγο":{"IATA":'ORD', "coordinates":(41.980284,-87.9111866)}}
        self.cities = [i for i in self.airports.keys()]
        
        self.numberOfLegs = tkinter.IntVar()
        self.numberOfLegs.set(3)
        self.rButtonFrame = tkinter.Frame(self.root)
        tkinter.Radiobutton(self.rButtonFrame, text = "1 Σκέλος", variable = self.numberOfLegs, value = 1, command = lambda : self.numberOfLegsChanged(self.numberOfLegs.get())).pack()
        tkinter.Radiobutton(self.rButtonFrame, text = "2 Σκέλη", variable = self.numberOfLegs, value = 2, command = lambda : self.numberOfLegsChanged(self.numberOfLegs.get())).pack()
        tkinter.Radiobutton(self.rButtonFrame, text = "3 Σκέλη", variable = self.numberOfLegs, value = 3, command = lambda : self.numberOfLegsChanged(self.numberOfLegs.get())).pack()

        self.rButtonFrame.grid(row = 0, column = 0)

        t = datetime.date.today()
        self.cal = tkcalendar.Calendar(self.rButtonFrame, selectmode = "day", year = t.year, month = t.month,day = t.day)
        self.cal.pack(side = 'right')

        r = 1
        self.fStart = myFrame(self.root,isStartingPoint = True)
        self.fStart.grid(row = r,column = 0)

        self.fStation1 = myStationFrame(self.root,1)
        self.fStation1.grid(row = r+1,column = 0)

        self.fStation2 = myStationFrame(self.root,2)
        self.fStation2.grid(row = r+2,column = 0)

        self.fFinish = myFrame(self.root,isStartingPoint = False)
        self.fFinish.grid(row = r+3,column = 0)

        tkinter.Button(self.root, text = 'SUBMIT FLIGHT', command = lambda :self.submit(self.numberOfLegs.get())).grid(row = r+4, column = 0)

    def numberOfLegsChanged(self,legs):
        if legs == 1:
            self.fStation1.grid_remove()
            self.fStation2.grid_remove()
        elif legs == 2:
            self.fStation1.grid()
            self.fStation2.grid_remove()
        elif legs == 3:
            self.fStation1.grid()
            self.fStation2.grid()

    #Ελέγχει εαν μία πόλη έχει επιλεχθει σε παραπάνω απο 1 σταθμους
    def isThereADouble(self,cityList):
        for city in cityList:
            if cityList.count(city) > 1 :
                print("Η πόλη",city,"εχει επιλεχθεί παραπάνω από 1 φορές")
                return True
        return False


    #H submit συνδεει όλα τα δεδομένα που έχουν δωθει στα widgets ωστε να σχηματίσει σε μορφη λεξικων όλα τα σκελη και τα ταξιδια
    #Εδω το legs ειναι το πληθος των σκελων
    def submit(self,legs):
        values = ([self.fStart.getValues(),self.fStation1.getValues(),self.fStation2.getValues()][0:legs]) + [self.fFinish.getValues()]
        self.date = myFuncs.format_date(self.cal.get_date())


        if self.isThereADouble([i["city"] for i in values]):
            print("Αδυναμία εισαγωγής πτήσης")
            return

        print(" -> ".join([self.airports[i["city"]]["IATA"] for i in values]))
        print()

        self.flightLegs = []
        
        date1 = self.date
        date2 = self.date
        for i in range(legs):
            #Υπολογισμος απόστασης σε χιλιόμετρα
            c1 = self.airports[values[i]['city']]["coordinates"]
            c2 = self.airports[values[i+1]['city']]["coordinates"]
            d = geopy.distance.distance(c1,c2).km
            d = round(d,2)
            
            """Ελεγχος εαν αλλάζει η ημερολογιακή ημέρα κατα τη διαρκεια του ταξιδιου"""
            #Περίπτωση 1: Η ημέρα αλλάζει όση ωρα ο επιβάτης περίμενει στο αεροδρόμιο κατα μία ενδιάμεση στάση
            if(len(values[i]) == 4): #Μόνο εαν το values[i] εχει 4 στοιχεία η στάση i είναι ενδιάμεση στάση
                if myFuncs.dayHasChanged(values[i]['arrival time'],values[i]['departure time']):
                    date2 = myFuncs.setNDaysLater(date2,1)
                    date1 = date2
            #Περίπτωση 2: Η ημέρα αλλάζει όσο το αεοπλάνο βρίσκεται στον αέρα
            if myFuncs.dayHasChanged(values[i]['departure time'],values[i+1]['arrival time']):
                date2 = myFuncs.setNDaysLater(date2,1)
            
            self.flightLegs.append({"legID":None, "travelDistance":d, "departTime" : values[i]['departure time'],"arrivalTime": values[i+1]['arrival time'],"departDate":date1, "arrivalDate":date2, "departGate" : values[i]['gate'], "departureAirportID" : self.airports[values[i]['city']]["IATA"] , "arrivalAirportID" : self.airports[values[i+1]['city']]["IATA"]})
            date1= date2

            
        self.journeys = []
        
        for i in range(legs):
            for j in range(legs - i):
                self.journeys.append({"journeyID" : None,"departureAirportID" : self.flightLegs[i]["departureAirportID"] , "arrivalAirportID" : self.flightLegs[i+j]["arrivalAirportID"], "journeyDate": self.flightLegs[i]["departDate"]})

        self.createDicts()
        
        return

    #Καθορίζει ολα τα λεξικα με τις τιμες  που θα εισαχθούν στη βάση και αριθμεί τα ταξίδια και τα σκέλη, έπειτα καλεί την insert οσες φορές χρειάζεται
    #Για καθε Table της sql θα δημιουργηθεί μία λίστα με ένα λεξικο για καθε γραμμη που εισάγουμε, με κλειδια τα ονοματα των γνωρισμάτων του πίνακα και τιμες τις τιμές αυτων για κάθε εισαχθεισα σειρά 
    def createDicts(self):
        legs = self.numberOfLegs.get()
        
        #Αρίθμηση Legs,Journeys
        query = """
                select max(legID),max(journeyID)
                from journeysLegs
                """
        [l,j]=list(self.dbHandler.executeSQL(query)[0].values())
        
    
        for i in self.flightLegs:
            l+=1
            i["legID"] = str(l)
            
        for i in self.journeys:
            j+=1
            i["journeyID"] = str(j)

        #Ζευγαρια για τον πίνακα journeysLegs
        journeysAndLegs = []
        if(len(self.flightLegs) == 1):
            journeysAndLegs.append({"journeyID":self.journeys[0]["journeyID"], "legID":self.flightLegs[0]["legID"]})
        elif(len(self.flightLegs) == 2):
            journeysAndLegs.append({"journeyID":self.journeys[0]["journeyID"], "legID":self.flightLegs[0]["legID"]})
            journeysAndLegs.append({"journeyID":self.journeys[1]["journeyID"], "legID":self.flightLegs[0]["legID"]})
            journeysAndLegs.append({"journeyID":self.journeys[1]["journeyID"], "legID":self.flightLegs[1]["legID"]})
            journeysAndLegs.append({"journeyID":self.journeys[2]["journeyID"], "legID":self.flightLegs[1]["legID"]})

        elif(len(self.flightLegs) == 3):
            for i in range(len(self.journeys)):
                if i in [0,1,2]:
                    journeysAndLegs.append({"journeyID":self.journeys[i]["journeyID"], "legID":self.flightLegs[0]["legID"]})
                if i in [1,2,3,4]:
                    journeysAndLegs.append({"journeyID":self.journeys[i]["journeyID"], "legID":self.flightLegs[1]["legID"]})
                if i in [2,4,5]:
                    journeysAndLegs.append({"journeyID":self.journeys[i]["journeyID"], "legID":self.flightLegs[2]["legID"]})

        #Επιλογη Random πιλοτου, αεροσκάφους για καθε σκελ0ς
        pilotsAircrafts = []
        for i in range(legs):
            self.dbHandler.executeSQL("""CREATE INDEX dateIndex on FlightLegs(departDate)""")
            query = """SELECT pilotID, aircraftID
                        from Pilot, Aircraft
                        WHERE pilot.pilotID not in (SELECT pilotID
                        from (Controls NATURAL join FlightLegs)
                        where departDate = '{self.flightLegs[i]["departDate"]}'
                        )
                        AND aircraftID not in (SELECT airplaneID
                        from (Controls NATURAL join FlightLegs)
                        where departDate = '{self.flightLegs[i]["departDate"]}'
                        )
                        ORDER by random()
                        limit(1)
                    """
            randPilAirc = self.dbHandler.executeSQL(query)[0]
            self.dbHandler.executeSQL("""DROP INDEX dateIndex""")
            
            if i == 0:
                pilotsAircrafts.append(randPilAirc)
            elif i == 1:
                pilot = [randPilAirc['pilotID'],pilotsAircrafts[0]['pilotID']][random.randint(0,1)]
                aircraft = [randPilAirc['aircraftID'],pilotsAircrafts[0]['aircraftID']][random.randint(0,1)]
                pilotsAircrafts.append({'pilotID':pilot,'aircraftID':aircraft})
            elif i == 2:
                pa = {}
                for j in randPilAirc:
                    if randPilAirc[j] == pilotsAircrafts[0][j] and randPilAirc[j] != pilotsAircrafts[1][j]:
                        pa.update({j:pilotsAircrafts[1][j]})
                    else:
                        pa.update({j:[randPilAirc[j],pilotsAircrafts[1][j]][random.randint(0,1)]})
                
                pilotsAircrafts.append(pa)


        controls = []
        for i in range(legs):
            controls.append({"pilotID":pilotsAircrafts[i]["pilotID"], "airplaneID":pilotsAircrafts[i]['aircraftID'],"legID":self.flightLegs[i]["legID"]})

        """ΕΙΣΑΓΩΓΗ ΔΕΔΟΜΕΝΩΝ"""
        #Flight Legs
        print("~~~~~~Εισαγωγη στο flightLegs~~~~~~")
        for i in range(len(self.flightLegs)):
            print(self.flightLegs[i])
            self.dbHandler._insertToDB("FlightLegs",self.flightLegs[i])
        print("\n\n")

        #Journeys
        print("~~~~~~Εισαγωγη στο Journey~~~~~~")
        for i in range(len(self.journeys)):
            print(self.journeys[i])
            self.dbHandler._insertToDB("Journey",self.journeys[i])
        print("\n\n")
        
        #journeysLegs
        print("~~~~~~Εισαγωγη στο journeysLegs~~~~~~")
        for i in range(len(journeysAndLegs)):
            print(journeysAndLegs[i])
            self.dbHandler._insertToDB("journeysLegs",journeysAndLegs[i])
        print("\n\n")
        
        #controls
        print("~~~~~~Εισαγωγη στο Controls~~~~~~")
        for i in range(len(controls)):
            print(controls[i])
            self.dbHandler._insertToDB("Controls",controls[i])
        print("\n\n")

        return




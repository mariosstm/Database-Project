import tkinter as tk
from functools import partial
from tkinter.constants import CENTER, RIGHT, VERTICAL
from PIL import Image, ImageTk
from tkinter.messagebox import showinfo
import handleDataBase as hdb
from datetime import date,datetime
import usefulFunctions as F
import tkcalendar as tkc
import journeyFinder as jF
import showJourneyDetails as s

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Statistics():
    def __init__(self,root,main,db,info):
        self.root=root
        self.main=main
        self.customerInfo=info
        
        self.db=db
        self.topFrame=tk.Frame(main,background='gray80',relief='groove', highlightthickness=2)
        self.topFrame.grid(row=0, sticky='nsew')
    
        self.botFrame=tk.Frame(main,background='gray90', highlightthickness=2)
        self.botFrame.grid(row=1,sticky="nswe")
        
        #LEFTSIDE
        self.leftFrame=tk.Frame(self.botFrame,bg='gray90', highlightthickness=2)
        self.leftFrame.grid(row=0,column=0, sticky='nsew')
        
        class myCityOptionMenu(tk.OptionMenu):
            def __init__(self,root,startingVal,**kwargs):
                self.root=root
                self.startingVal=startingVal
                self.airports = {"Athens":'ATH', "London":'LHR', "Manchester":'MAN', "Paris":'CDG', "Amsterdam":'AMS', "Istanbul":'IST', "Frankfurt":'FRA', "Monacho":'MUC', "Madrid":'MAD', "Barcelona":'BCN', "Rome":'FCO', "Zurich":'ZRH', "Brussels":'BRU', "Dublin":'DUB', "Moscow":'DME', "Oslo":'OSL', "Vienna":'VIE', "New York":'JFK', "Los Angeles":'LAX', "Chicago":'ORD'}
                self.cities = [i for i in self.airports.keys()]
                self.cityChoice = tk.StringVar()
                self.cityChoice.set(self.startingVal)
                tk.OptionMenu.__init__(self,root,self.cityChoice,*(self.cities),**kwargs)
                self.configure(width = 16)
        #RIGHTSIDE   
        
        self.rightFrame=tk.Frame(self.botFrame,background='gray90', highlightthickness=2)
        self.rightFrame.grid(row=0,column=1, sticky='nsew')

        main.grid_rowconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=8)
        main.grid_columnconfigure(0, weight=1)
        
        
        self.botFrame.grid_rowconfigure(0,weight=1)
        self.botFrame.grid_columnconfigure(0,weight=1)
        
        
        self.Title=tk.Label(self.topFrame,borderwidth='218',text="Your Personalised Data",bd=5,bg='grey80',font=('Adobe Arabic',16,''))
        self.Title.place(x=500,y=30,anchor=CENTER)
        self.exitButton=tk.Button(self.topFrame,text='Quit',command=lambda : self.back(main)).place(relx=0.98, rely=0.5, anchor=CENTER )
        
        destinationsSQL = f"""SELECT departureAirportID, arrivalAirportID, min(departDate) as d,journeyID
                from (( journeysLegs NATURAL join (select * from Journey where journeyID in
                (select journeyID
                from Ticket
                where customerID = '{self.customerInfo['ID']}')))NATURAL join (SELECT legID, FlightLegs.departDate from FlightLegs))
                group by journeyID 
                order by d """
        
        destinations=self.db.executeSQL(destinationsSQL,show=False)
        i=0
        dest=dict()
        base=0
        for de in destinations:
            
            airID=de["arrivalAirportID"]
            if  airID in dest:
                dest[airID]+=1
            else:
                dest[airID]=1
            base+=1
            
            
        fig = Figure(figsize=(10, 5), dpi=100)
        fig.patch.set_facecolor('white')# create a figure object
        ax = fig.add_subplot(111) # add an Axes to the figure
        val=[(i/base)*100 for i in dest.values()]
        keys=[j for j in dest.keys() ]
        ax.pie(val, radius=1, labels=keys,autopct='%0.2f%%', shadow=True,)
                
        chart1 = FigureCanvasTkAgg(fig,self.botFrame)
        ax.patch.set_facecolor('red')
        chart1.get_tk_widget().place(relx=0,rely=0)
        
            
        
        
        
    def back(self,main):
        for widget in self.main.winfo_children():
            widget.destroy()
    
    def mainf(self):
        #dbfile='database.db'
        #db=hdb.DataModel(dbfile)
        #root=tk.Tk()        
        Statistics(self.main,self.db)
        self.main.mainloop()
#from signal import signal
import tkinter as tk
from functools import partial
from tkinter.constants import CENTER, RIGHT, VERTICAL
from PIL import Image, ImageTk
from itertools import count, cycle
import handleDataBase as hdb
from datetime import date,datetime
import tkinter.ttk as ttk
import tkinter.messagebox as tkmb
import ticket_insertion as TI
import tkcalendar as tkc
import usefulFunctions as F
import journeyFinder as jF
import Overview as o


####   MAIN CLASS / MAIN PANEL
####   CONSISTS OF 2 FRAMES --> TOP , BOT 
#### BOT FRAME CONSISTS OF LEFT AND RIGHT FRAME

class customerApplication():
    def __init__(self,main,db,i):
        
        self.info=i
        self.db=db
        main.geometry('1200x600-50-100')  
        main.title('Welcome to Terminal-A')
        self.topFrame=tk.Frame(main,background='cyan3')
        self.topFrame.grid(row=0, sticky='nsew')
        
        self.Logo=tk.Label(self.topFrame,text="Terminal-A",bd=5,bg='cyan3',font=('Brush Script MT',14,'')).place(relx=0.075,rely=0.5,anchor=CENTER)


        self.botFrame=tk.Frame(main,background='gray90')
        self.botFrame.grid(row=1,sticky="nswe")

     #LEFTSIDE
        self.leftFrame=tk.Frame(self.botFrame,bg='gray20')
        self.leftFrame.grid(row=0,column=0, sticky='nsew')
     #RIGHTSIDE   
        self.rightFrame=tk.Frame(self.botFrame,background='gray80')
        self.rightFrame.grid(row=0,column=1, sticky='nsew')
        
    
        main.grid_rowconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=10)
        main.grid_columnconfigure(0, weight=1)
        
        
        self.botFrame.grid_rowconfigure(0,weight=1)
        self.botFrame.grid_columnconfigure(0,weight=2)
        self.botFrame.grid_columnconfigure(1,weight=11)
        
        
        ##### MAIN PRESSABLE LABELS THAT RETURN A CLASS #####
        
        self.Profile=tk.Label(self.leftFrame,borderwidth='218',text="Profile",bd=5,bg='grey20',font=('Adobe Arabic',14,''))
        self.Profile.place(relx=0.5,rely=0.07,anchor=CENTER)
        self.Profile.bind("<Button-1>",lambda x:Profile(main,self.rightFrame,self.db,self.info,show=False))

        self.Journeys=tk.Label(self.leftFrame,borderwidth='218',text="My Journeys",bd=5,bg='grey20',font=('Adobe Arabic',14,''))
        self.Journeys.place(relx=0.5,rely=0.18,anchor=CENTER)
        self.Journeys.bind("<Button-1>",lambda z:Journeys(main,self.rightFrame,self.db,self.info))
        
        self.buyTicket=tk.Label(self.leftFrame,borderwidth='218',text="Buy a Ticket",bd=5,bg='grey20',font=('Adobe Arabic',14,''))
        self.buyTicket.place(relx=0.5,rely=0.29,anchor=CENTER)
        self.buyTicket.bind("<Button-1>",lambda ti:buyTicket(main,self.rightFrame,self.db,self.info))
        
        self.Cancel=tk.Label(self.leftFrame,borderwidth='218',text="Cancel Ticket",bd=5,bg='grey20',font=('Adobe Arabic',14,''))
        self.Cancel.place(relx=0.5,rely=0.40,anchor=CENTER)
        self.Cancel.bind("<Button-1>",lambda pi:Cancel(main,self.rightFrame,self.db,self.info))
        
        self.Overview=tk.Label(self.leftFrame,borderwidth='218',text="Overview",bd=5,bg='grey20',font=('Adobe Arabic',14,''))
        self.Overview.place(relx=0.5,rely=0.51,anchor=CENTER)
        self.Overview.bind("<Button-1>",lambda over:o.Statistics(main,self.rightFrame,self.db,self.info))

    
    def mainf(self,main):
        
        customerApplication(main,self.db,self.info)
        main.mainloop()


##### BUY TICKET TAKES roor=main ( main frame of customer ) and main=rightframe( of customer)
class buyTicket():
    def __init__(self,root,main,db,info):
        self.signal=0
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
        
        #WE CREATE AN OPTION MENU FOR THE CUSTOMER TO CHOOSE HIS DESTINATIONS
        
        class myCityOptionMenu(ttk.OptionMenu):
            def __init__(self,root,startingVal,**kwargs):
                self.root=root
                self.startingVal=startingVal
                self.airports = {"Athens":'ATH', "London":'LHR', "Manchester":'MAN', "Paris":'CDG', "Amsterdam":'AMS', "Istanbul":'IST', "Frankfurt":'FRA', "Monacho":'MUC', "Madrid":'MAD', "Barcelona":'BCN', "Rome":'FCO', "Zurich":'ZRH', "Brussels":'BRU', "Dublin":'DUB', "Moscow":'DME', "Oslo":'OSL', "Vienna":'VIE', "New York":'JFK', "Los Angeles":'LAX', "Chicago":'ORD'}
                self.cities = [i for i in self.airports.keys()]
                self.cityChoice = tk.StringVar()
                self.cityChoice.set(self.startingVal)
                tk.OptionMenu.__init__(self,self.root,self.cityChoice,*(self.cities),**kwargs)
                self.configure(width = 16)
        
        #RIGHTSIDE   
        
        self.rightFrame=tk.Frame(self.botFrame,background='gray90', highlightthickness=2)
        self.rightFrame.grid(row=0,column=1, sticky='nsew')

        main.grid_rowconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=8)
        main.grid_columnconfigure(0, weight=1)
        
        
        self.botFrame.grid_rowconfigure(0,weight=1)
        self.botFrame.grid_columnconfigure(0,weight=1)
        self.botFrame.grid_columnconfigure(1,weight=1)
        
        
        ######CREATE ALL THE CHOICES FOR THE CUSTOMER (TICKET TYPE , DESTINATION ...)
        
        self.Title=tk.Label(self.topFrame,borderwidth='218',text="Travel The World",bd=5,bg='grey80',font=('Adobe Arabic',16,''))
        self.Title.place(x=500,y=30,anchor=CENTER)
        self.exitButton=tk.Button(self.topFrame,text='Quit',command=lambda : self.back)
        self.exitButton.place(relx=0.98, rely=0.5, anchor=CENTER )
        self.travelLabel=tk.Label(self.leftFrame,text='Select Travel Date',background="grey90",font=('Adobe Arabic',13,''))
        self.Cal=tkc.Calendar(self.leftFrame,year=2022,month=1,day=18)
        submit=tk.Button(self.leftFrame,text='Find Ticket',width=20,bg="black",fg='white',command=self.findTicket)
        self.labelFrom=tk.Label(self.leftFrame,text="Select point of Departure:",bd=5,bg='grey90',font=('Adobe Arabic',14,'underline'))
        self.menuFrom=myCityOptionMenu(self.leftFrame,'Athens')
        self.labelTo=tk.Label(self.leftFrame,text="Select Destination :",bd=5,bg='grey90',font=('Adobe Arabic',14,'underline'))
        self.menuTo=myCityOptionMenu(self.leftFrame,'Amsterdam')
        self.ticketTypeLabel=tk.Label(self.leftFrame,text="Ticket Type:",bd=5,bg='grey90',font=('Adobe Arabic',14,'underline'))
        self.ticketType = tk.StringVar(self.leftFrame, "regular")
        flex=tk.Radiobutton(self.leftFrame, text = "Regular Class", bg='grey90',variable = self.ticketType, value = 'regular', command = lambda : self.ticketType.get())
        business=tk.Radiobutton(self.leftFrame, text = "Business Class", bg='grey90',variable = self.ticketType, value = 'business class', command = lambda : self.ticketType.get())
        
        
        self.LegsLabel=tk.Label(self.leftFrame,text="Ticket Type:",bd=5,bg='grey90',font=('Adobe Arabic',14,'underline'))
        self.legType = tk.IntVar(self.leftFrame, 1)
        
        leg1=tk.Radiobutton(self.leftFrame, text = "ΑΠΕΥΘΕΙΑΣ", bg='grey90',variable = self.legType, value = 1)
        leg2=tk.Radiobutton(self.leftFrame, text = "ΜΕΧΡΙ ΜΙΑ ΣΤΑΣΗ", bg='grey90',variable = self.legType, value = 2)
        leg3=tk.Radiobutton(self.leftFrame, text = "ΜΕΧΡΙ ΚΑΙ 2 ΣΤΑΣΕΙΣ", bg='grey90',variable = self.legType, value = 3)
        
        self.labelFrom.place(relx=0.01,rely=0.0)
        self.menuFrom.place(relx=0.05,rely=0.07)
        self.labelTo.place(relx=0.01,rely=0.2)
        self.menuTo.place(relx=0.05,rely=0.26)
        self.ticketTypeLabel.place(relx=0.01,rely=0.35)
        flex.place(relx=0.05,rely=0.42)
        business.place(relx=0.05,rely=0.48)
        self.LegsLabel.place(relx=0.01,rely=0.53)
        leg1.place(relx=0.05,rely=0.6)
        leg2.place(relx=0.05,rely=0.64)
        leg3.place(relx=0.05,rely=0.68)
        self.travelLabel.place(relx=0.575,rely=0.0)
        self.Cal.place(relx=0.5,rely=0.05)
        submit.place(relx=0.6,rely=0.455)

        self.canvasL=tk.Canvas(self.rightFrame,width=8, height=50,background="grey90", scrollregion=(0,0,4000,4000))
        self.scr_v1L = tk.Scrollbar(self.rightFrame,orient=VERTICAL)
        self.scr_v1L.pack(side=RIGHT,fill='y')
        self.scr_v1L.config(command=self.canvasL.yview)

        self.canvasL.config(yscrollcommand=self.scr_v1L.set)
        self.canvasL.pack(fill='both',expand=True)
    
    
    #FUNCTION TO FIND A SPECIFIC TICKET ON A SPECIFIC DATE
    #IF JOURNEY DOES NOT EXIST THE FIND TICKET ON A SPECTRUM OF DATES
    def findTicket(self,r=False):
        
        self.canvasL.delete('all')
        
        title=tk.Label(self.canvasL,text='Available Tickets',background="grey90",font=('Adobe Arabic',20,'underline'))
        self.canvasL.create_window( 250,+65, window=title)
        todaysDate=tk.Label(self.canvasL,text=f'Todays date:{date.today()}',background="grey90",font=('Adobe Arabic',12,'underline'))
        self.canvasL.create_window( 410,+15, window=todaysDate)
        
        wfrom=self.menuFrom.airports[self.menuFrom.cityChoice.get()]
        wto=self.menuFrom.airports[self.menuTo.cityChoice.get()]
        Nlegs=self.legType.get()
        pixelDIF=220
        
        ## SAVE INFORMATION FOR RETURN TICKET IF CUSTOMER WANTS ONE
        if not r:
            self.jfrom=wfrom
            self.jto=wto
            self.jdate=F.format_date(self.Cal.get_date())
            self.Journeys=jF.getJourneys(self.db,3,wfrom,wto,Nlegs,date1=F.format_date(self.Cal.get_date()),date2='')
        else:
            self.Journeys=jF.getJourneys(self.db,3,self.jto,self.jfrom,3,self.jdate)
        self.ticketList=[]
        i=0
        if  self.Journeys:
            for self.journey in self.Journeys:
                #WE CHECK FOR STOPS IN FLIGHTS
                # IF STASH 1 AND 2 DO NOT EXIST THEN PRINT CERTAIN FORMAT OF TICKEET
                # SAME FOR THE OTHER TWO 
                if ( (self.journey['Στάση 2']!='--') and self.journey['Στάση 1']!='--'):
                    pixelDIF+=50
                    self.labelframe=tk.LabelFrame(self.rightFrame,height=490,width=350,background="grey90",text=f'Date: {F.sqliteBetterDateFormat(self.journey["journeyDate"])}',bd=2,font=('Adobe Arabic',13,''))

                    LabelDeparture0=tk.Label(self.labelframe,text=f'Departure  from  {self.journey["From"]} :',bg='grey90',font=('Adobe Arabic ',10,'underline','bold'))
                    LabelTime0=tk.Label(self.labelframe,text=f'Departure Time: {self.journey["departTime"]}  ,',bg='grey90',font=('Adobe Arabic ',10,''))
                    LabelArrival0=tk.Label(self.labelframe,text=f'Arrival  at  {self.journey["Στάση 1"]} :',bg='grey90',font=('Adobe Arabic bold ',10,'underline','bold'))
                    LabelArrivalTime0=tk.Label(self.labelframe,text=f'Estimated Time of Arrival: {self.journey["s1ArrTime"]}',bg='grey90',font=('Adobe Arabic ',10,''))
                    dur=F.timeInterval(self.journey["departTime"],self.journey["s1ArrTime"])
                    LabelDuration0=tk.Label(self.labelframe,text=f'Estimated Duration: {dur} hours',bg='grey90',font=('Adobe Arabic bold',10,'bold'))
                    
                    LabelDeparture1=tk.Label(self.labelframe,text=f'Departure  from  {self.journey["Στάση 1"]} :',bg='grey90',font=('Adobe Arabic ',10,'underline','bold'))
                    LabelTime1=tk.Label(self.labelframe,text=f'Departure Time: {self.journey["s1DepTime"]}  ,',bg='grey90',font=('Adobe Arabic ',10,''))
                    LabelArrival1=tk.Label(self.labelframe,text=f'Arrival  at  {self.journey["Στάση 2"]} :',bg='grey90',font=('Adobe Arabic bold ',10,'underline','bold'))
                    LabelArrivalTime1=tk.Label(self.labelframe,text=f'Estimated Time of Arrival: {self.journey["s2ArrTime"]}',bg='grey90',font=('Adobe Arabic ',10,''))
                    dur1=F.timeInterval(self.journey["s1DepTime"],self.journey["s2ArrTime"])
                    LabelDuration1=tk.Label(self.labelframe,text=f'Estimated Duration: {dur1} hours',bg='grey90',font=('Adobe Arabic bold',10,'bold'))
                    
                    LabelDeparture2=tk.Label(self.labelframe,text=f'Departure  from  {self.journey["Στάση 2"]} :',bg='grey90',font=('Adobe Arabic ',10,'underline','bold'))
                    LabelTime2=tk.Label(self.labelframe,text=f'Departure Time: {self.journey["s2DepTime"]}  ,',bg='grey90',font=('Adobe Arabic ',10,''))
                    LabelArrival2=tk.Label(self.labelframe,text=f'Arrival  at  {self.journey["To"]} :',bg='grey90',font=('Adobe Arabic bold ',10,'underline','bold'))
                    LabelArrivalTime2=tk.Label(self.labelframe,text=f'Estimated Time of Arrival: {self.journey["arrivalTime"]}',bg='grey90',font=('Adobe Arabic ',10,''))
                    dur2=F.timeInterval(self.journey["s2DepTime"],self.journey["arrivalTime"])
                    LabelDuration2=tk.Label(self.labelframe,text=f'Estimated Duration: {dur2} hours',bg='grey90',font=('Adobe Arabic bold',10,'bold'))
                    
                    
                    
                    costLabel=tk.Label(self.labelframe,fg='blue',text=f'Average Cost: {self.journey["cost"]}(Regular)\n{2*self.journey["cost"]}(Business class)',bg='grey90',font=('Adobe Arabic bold',10,''))
                    buyButton=tk.Button(self.labelframe,fg='blue',text='Buy ',bg='grey90',font=('Adobe Arabic bold',10,''),command=self.buy_lambda(self.customerInfo['customerID']))
                    
                    
                    repeat=0.0
                    LabelDeparture0.place(relx=0.01,rely=0.005+repeat)
                    LabelTime0.place(relx=0.03,rely=0.05+repeat)
                    LabelArrival0.place(relx=0.01,rely=0.17+repeat)
                    LabelArrivalTime0.place(relx=0.03,rely=0.23+repeat)
                    LabelDuration0.place(relx=0.4,rely=0.275+repeat)
                    
                    repeat+=0.27
                    LabelDeparture1.place(relx=0.01,rely=0.05+repeat)
                    LabelTime1.place(relx=0.03,rely=0.11+repeat)
                    LabelArrival1.place(relx=0.01,rely=0.17+repeat)
                    LabelArrivalTime1.place(relx=0.03,rely=0.23+repeat)
                    LabelDuration1.place(relx=0.4,rely=0.28+repeat)
                    
                    repeat+=0.33
                    LabelDeparture2.place(relx=0.01,rely=0.005+repeat)
                    LabelTime2.place(relx=0.03,rely=0.05+repeat)
                    LabelArrival2.place(relx=0.01,rely=0.17+repeat)
                    LabelArrivalTime2.place(relx=0.03,rely=0.23+repeat)
                    LabelDuration2.place(relx=0.4,rely=0.28+repeat)
                    
                    
                    costLabel.place(relx=0.5,rely=0.005)
                    buyButton.place(relx=0.85,rely=0.95)
                    
                    self.canvasL.create_window( 230,pixelDIF+110, window=self.labelframe)
                    pixelDIF+=500
                    i+=1
                    
                if (self.journey['Στάση 1']=='--' ) :
                    pixelDIF+=50
                
                    
                    self.labelframe=tk.LabelFrame(self.rightFrame,height=490,width=350,background="grey90",text=f'Date: {F.sqliteBetterDateFormat(self.journey["journeyDate"])}',bd=2,font=('Adobe Arabic',13,''))
        
        
        
                    LabelDeparture=tk.Label(self.labelframe,text=f'Departure  from  {self.journey["From"]} :',bg='grey90',font=('Adobe Arabic ',12,'underline','bold'))

                    LabelTime=tk.Label(self.labelframe,text=f'Departure Time: {self.journey["departTime"]}  ,',bg='grey90',font=('Adobe Arabic ',12,''))
                    
                    LabelArrival=tk.Label(self.labelframe,text=f'Arrival  at  {self.journey["To"]} :',bg='grey90',font=('Adobe Arabic bold ',12,'underline','bold'))
                    
                    LabelArrivalTime=tk.Label(self.labelframe,text=f'Estimated Time of Arrival: {self.journey["arrivalTime"]}',bg='grey90',font=('Adobe Arabic ',12,''))
                    
                    dur=self.duration(self.journey["departTime"],self.journey["arrivalTime"])
                    LabelDuration=tk.Label(self.labelframe,text=f'Estimated Duration: {dur} hours',bg='grey90',font=('Adobe Arabic bold',12,'bold'))
                    
                    
                    costLabel=tk.Label(self.labelframe,fg='blue',text=f'Average Cost: {self.journey["cost"]}(Regular)\n{2*self.journey["cost"]}(Business class)',bg='grey90',font=('Adobe Arabic bold',10,''))
                    
                    buyButton=tk.Button(self.labelframe,fg='blue',text='Buy ',bg='grey90',font=('Adobe Arabic bold',10,''),command=self.buy_lambda)
                    
                    
                    
                    LabelDeparture.place(relx=0.01,rely=0.05)
                    LabelTime.place(relx=0.01,rely=0.13)
                    LabelArrival.place(relx=0.01,rely=0.3)
                    LabelArrivalTime.place(relx=0.01,rely=0.385)
                    LabelDuration.place(relx=0.1,rely=0.6)
                    costLabel.place(relx=0.5,rely=0.005)
                    buyButton.place(relx=0.85,rely=0.95)
                    self.canvasL.create_window( 230,pixelDIF+110, window=self.labelframe)
                    pixelDIF+=500
                    i+=1
                    
                if( (self.journey['Στάση 2']=='--') and self.journey['Στάση 1']!='--'):
                    pixelDIF+=50
                    self.labelframe=tk.LabelFrame(self.rightFrame,height=490,width=350,background="grey90",text=f'Date: {F.sqliteBetterDateFormat(self.journey["journeyDate"])}',bd=2,font=('Adobe Arabic',13,''))
        
                    
                    LabelDeparturex=tk.Label(self.labelframe,text=f'Departure  from  {self.journey["From"]} :',bg='grey90',font=('Adobe Arabic ',10,'underline','bold'))
                    LabelTimex=tk.Label(self.labelframe,text=f'Departure Time: {self.journey["departTime"]}  ,',bg='grey90',font=('Adobe Arabic ',10,''))
                    LabelArrivalx=tk.Label(self.labelframe,text=f'Arrival  at  {self.journey["Στάση 1"]} :',bg='grey90',font=('Adobe Arabic bold ',10,'underline','bold'))
                    LabelArrivalTimex=tk.Label(self.labelframe,text=f'Estimated Time of Arrival: {self.journey["s1ArrTime"]}',bg='grey90',font=('Adobe Arabic ',10,''))
                    dur=F.timeInterval(self.journey["departTime"],self.journey["s1ArrTime"])
                    LabelDurationx=tk.Label(self.labelframe,text=f'Estimated Duration: {dur} hours',bg='grey90',font=('Adobe Arabic bold',10,'bold'))
                    
                    LabelDeparturey=tk.Label(self.labelframe,text=f'Departure  from  {self.journey["Στάση 1"]} :',bg='grey90',font=('Adobe Arabic ',10,'underline','bold'))
                    LabelTimey=tk.Label(self.labelframe,text=f'Departure Time: {self.journey["s1DepTime"]}  ,',bg='grey90',font=('Adobe Arabic ',10,''))
                    LabelArrivaly=tk.Label(self.labelframe,text=f'Arrival  at  {self.journey["To"]} :',bg='grey90',font=('Adobe Arabic bold ',10,'underline','bold'))
                    LabelArrivalTimey=tk.Label(self.labelframe,text=f'Estimated Time of Arrival: {self.journey["arrivalTime"]}',bg='grey90',font=('Adobe Arabic ',10,''))
                    dur1=F.timeInterval(self.journey["arrivalTime"],self.journey["s1ArrTime"])
                    LabelDurationy=tk.Label(self.labelframe,text=f'Estimated Duration: {dur1} hours',bg='grey90',font=('Adobe Arabic bold',10,'bold'))
                    
                    costLabel=tk.Label(self.labelframe,fg='blue',text=f'Average Cost: {self.journey["cost"]}(Regular)\n{2*self.journey["cost"]}(Business class)',bg='grey90',font=('Adobe Arabic bold',10,''))
                    buyButton=tk.Button(self.labelframe,fg='blue',text='Buy ',bg='grey90',font=('Adobe Arabic bold',10,''),command=self.buy_lambda)
                    
                    
                    
                    repeat=0.0
                    LabelDeparturex.place(relx=0.01,rely=0.005+repeat)
                    LabelTimex.place(relx=0.03,rely=0.05+repeat)
                    LabelArrivalx.place(relx=0.01,rely=0.17+repeat)
                    LabelArrivalTimex.place(relx=0.03,rely=0.23+repeat)
                    LabelDurationx.place(relx=0.4,rely=0.275+repeat)
                    
                    repeat+=0.5
                    LabelDeparturey.place(relx=0.01,rely=0.05+repeat)
                    LabelTimey.place(relx=0.03,rely=0.11+repeat)
                    LabelArrivaly.place(relx=0.01,rely=0.17+repeat)
                    LabelArrivalTimey.place(relx=0.03,rely=0.23+repeat)
                    LabelDurationy.place(relx=0.4,rely=0.28+repeat)

                    costLabel.place(relx=0.5,rely=0.005)
                    buyButton.place(relx=0.85,rely=0.95)
                    
                    self.canvasL.create_window( 230,pixelDIF+110, window=self.labelframe)

                    
                    pixelDIF+=500
                    i+=1
        else:
            pass
        
    ##  BUY TICKET FOR CERTAIN DESTINATION
    def buy_lambda(self):
        if  self.signal==0:
            TI.makeTicket(self.db,self.customerInfo['ID'],self.journey["journeyID"],self.ticketType.get(),0.0)
            response=tkmb.askokcancel("Return?","Buy Return Ticket ?")
            if response:
    #   IF  HE WANTS TO BUY A RETURN TICKET WE TURN SIGNAL TO 1
                self.signal=1
                self.findTicket(True)  
            else:
                for widget in self.main.winfo_children():
                    widget.destroy()
        else:
            for widget in self.main.winfo_children():
                    widget.destroy()
            

        
    def duration(self,s1,s2):
        s1 = f'{s1}'+':00'
        s2 = f'{s2}'+':00'
        
        format = '%H:%M:%S'
        dur = str(datetime.strptime(s2, format) - datetime.strptime(s1, format))
        length=len(dur)
        return dur[0:length-3]
    
    def back(self):
        for widget in self.main.winfo_children():
            widget.destroy()
    def mainf(self):     
        buyTicket(self.main,self.db)
        self.main.mainloop()

class Profile():
    # PERSONAL INFORMATION FOR CUSTOMER
    def __init__(self,root,main,db,i,show=False):
        for widget in main.winfo_children():
            widget.destroy()
        self.root=root
        self.info=i
        self.db=db
        self.topFrame=tk.Frame(main,background='gray80',relief='groove')
        self.topFrame.grid(row=0, sticky='nsew')
    
        self.botFrame=tk.Frame(main,background='gray80')
        self.botFrame.grid(row=1,sticky="nswe")
        
    #LEFTSIDE
        self.leftFrame=tk.Frame(self.botFrame,bg='gray90', highlightthickness=1)
        self.leftFrame.grid(row=0,column=0, sticky='nsew')
    #### SHOW = FALSE HIDE VALUABLE INFORMATION
        if not show:
            xc=90
            yc=70
            entryx=xc+100
            entryy=yc+43
            titleLabel=tk.Label(self.leftFrame,text='Your Profile Information', width=20,font=("bold",20) ).place(x=xc-45,y=yc-60)
            FnameL=tk.Label(self.leftFrame,text='First Name').place(x=xc,y=yc)
            MnameL=tk.Label(self.leftFrame,text='Middle Name').place(x=xc,y=yc+40)
            yc+=40
            LnameL=tk.Label(self.leftFrame,text='Last Name').place(x=xc,y=yc+40)
            usernameL=tk.Label(self.leftFrame,text='Username').place(x=xc,y=yc+40*2)
            passwordL=tk.Label(self.leftFrame,text='Password').place(x=xc,y=yc+40*3)
            PostalCodeL=tk.Label(self.leftFrame,text='Posta-Code').place(x=xc,y=yc+40*4)
            CountryL=tk.Label(self.leftFrame,text='Country').place(x=xc,y=yc+40*5)
            CityL =tk.Label(self.leftFrame,text='City').place(x=xc,y=yc+40*6)
            streetAddressL=tk.Label(self.leftFrame,text='Street Address').place(x=xc,y=yc+40*7)
            emailL =tk.Label(self.leftFrame,text='E-mail').place(x=xc,y=yc+40*8)
            CellphoneNumbL=tk.Label(self.leftFrame,text='Cellphone').place(x=xc,y=yc+40*9)
            
            FnameE= tk.Label(main, bd=2,text=f"{self.info['Fname']}") 
            MnameE=tk.Label(main, bd=2,text=f"{self.info['Mname']}")
            LnameE=tk.Label(main,  bd=2,text=f"{self.info['Lname']}")
        
            usernameE=tk.Label(main,  bd=2,text=f"{'*'*len(list(self.info['USERNAME']))}")
            passwordE=tk.Label(main,  bd=2,text=f"{'*'*len(list(self.info['PASSWORD']))}") 
            PostalCodeE=tk.Label(main,  bd=2,text=f"{'*'*len(list(self.info['PostalCode']))}")
            
            CountryE=tk.Label(main,  bd=2,text=f"{'*'*len(list(self.info['Country']))}") 
            CityE=tk.Label(main,  bd=2,text=f"{'*'*len(list(self.info['City']))}") 
            streetAddressE=tk.Label(main,  bd=2,text=f"{'*'*len(list(self.info['streetAddress']))}")
            emailE=tk.Label(main,  bd=2,text=f"{'*'*len(list(self.info['EMAIL']))}")
            CellphoneNumbE=tk.Label(main,  bd=2,text=f"{'*'*len(list(self.info['CellphoneNumber']))}")
            
            FnameE.place(x=entryx,y=entryy)
            MnameE.place(x=entryx,y=entryy+40)
            entryy+=40
            LnameE.place(x=entryx,y=entryy+40)
            usernameE.place(x=entryx,y=entryy+80)
            passwordE.place(x=entryx,y=entryy+118)
            PostalCodeE.place(x=entryx,y=entryy+118+40)
            CountryE.place(x=entryx,y=entryy+118+80)
            CityE.place(x=entryx,y=entryy+2*118)
            streetAddressE.place(x=entryx,y=entryy+2*118+40)
            emailE.place(x=entryx,y=entryy+2*118+80)
            CellphoneNumbE.place(x=entryx,y=entryy+3*118)
            
        #RIGHTSIDE   
            self.rightFrame=tk.Frame(self.botFrame,background='gray80', highlightthickness=1)
            self.rightFrame.grid(row=0,column=1, sticky='nsew')
            
            main.grid_rowconfigure(0, weight=1)
            main.grid_rowconfigure(1, weight=12)
            main.grid_columnconfigure(0, weight=1)
            
            self.botFrame.grid_rowconfigure(0,weight=1)
            self.botFrame.grid_columnconfigure(0,weight=9)
            self.botFrame.grid_columnconfigure(1,weight=11)
            
            
            self.exitButton=tk.Button(self.topFrame,text='Quit',command=lambda : self.back(main)).place(relx=0.98, rely=0.5, anchor=CENTER )
            
            self.changeDataB=tk.Button(self.topFrame,text='Change Info',command=lambda : validationForm(self.root,main,self.rightFrame,self.leftFrame,self.db,self.info,'Change Info')).place(relx=0.915, rely=0.5, anchor=CENTER )
            
            self.seeDataB=tk.Button(self.topFrame,text='Reveal Your Info',command=lambda : validationForm(self.root,main,self.rightFrame,self.leftFrame,self.db,self.info,'Reveal Info')).place(relx=0.825, rely=0.5, anchor=CENTER )
        #### IF SHOW == TRUE SHOW INFORMATION
        else:
            xc=90
            yc=70
            entryx=xc+100
            entryy=yc+43
            
            titleLabel=tk.Label(self.leftFrame,text='Your Profile Information', width=20,font=("bold",20) ).place(x=xc-45,y=yc-60)
            FnameL=tk.Label(self.leftFrame,text='First Name').place(x=xc,y=yc)
            MnameL=tk.Label(self.leftFrame,text='Middle Name').place(x=xc,y=yc+40)
            yc+=40
            LnameL=tk.Label(self.leftFrame,text='Last Name').place(x=xc,y=yc+40)
            usernameL=tk.Label(self.leftFrame,text='Username').place(x=xc,y=yc+40*2)
            passwordL=tk.Label(self.leftFrame,text='Password').place(x=xc,y=yc+40*3)
            PostalCodeL=tk.Label(self.leftFrame,text='Posta-Code').place(x=xc,y=yc+40*4)
            CountryL=tk.Label(self.leftFrame,text='Country').place(x=xc,y=yc+40*5)
            CityL =tk.Label(self.leftFrame,text='City').place(x=xc,y=yc+40*6)
            streetAddressL=tk.Label(self.leftFrame,text='Street Address').place(x=xc,y=yc+40*7)
            emailL =tk.Label(self.leftFrame,text='E-mail').place(x=xc,y=yc+40*8)
            CellphoneNumbL=tk.Label(self.leftFrame,text='Cellphone').place(x=xc,y=yc+40*9)
            entryy=70
            FnameE= tk.Label(main, bd=2,text=f"{self.info['Fname']}") 
            MnameE=tk.Label(main, bd=2,text=f"{self.info['Mname']}")
            
            entryy+=40
            LnameE=tk.Label(main,  bd=2,text=f"{self.info['Lname']}")
            
            usernameE=tk.Label(main,  bd=2,text=f"{self.info['USERNAME']}")
            passwordE=tk.Label(main,  bd=2,text=f"{self.info['PASSWORD']}") 
            PostalCodeE=tk.Label(main,  bd=2,text=f"{self.info['PostalCode']}") 
            CountryE=tk.Label(main,  bd=2,text=f"{self.info['Country']}") 
            CityE=tk.Label(main,  bd=2,text=f"{self.info['City']}") 
            streetAddressE=tk.Label(main,  bd=2,text=f"{self.info['streetAddress']}")
            emailE=tk.Label(main,  bd=2,text=f"{self.info['EMAIL']}")
            CellphoneNumbE=tk.Label(main,  bd=2,text=f"{self.info['CellphoneNumber']}")
            
            FnameE.place(x=entryx,y=entryy)
            MnameE.place(x=entryx,y=entryy+40)
            entryy+=40
            LnameE.place(x=entryx,y=entryy+40)
            usernameE.place(x=entryx,y=entryy+80)
            passwordE.place(x=entryx,y=entryy+118)
            PostalCodeE.place(x=entryx,y=entryy+118+40)
            entryy+=5
            CountryE.place(x=entryx,y=entryy+118+80)
            CityE.place(x=entryx,y=entryy+2*118)
            streetAddressE.place(x=entryx,y=entryy+2*118+40)
            emailE.place(x=entryx,y=entryy+2*118+80)
            CellphoneNumbE.place(x=entryx,y=entryy+3*118)
            
        #RIGHTSIDE   
            self.rightFrame=tk.Frame(self.botFrame,background='gray80', highlightthickness=1)
            self.rightFrame.grid(row=0,column=1, sticky='nsew')
            
            main.grid_rowconfigure(0, weight=1)
            main.grid_rowconfigure(1, weight=12)
            main.grid_columnconfigure(0, weight=1)
            
            self.botFrame.grid_rowconfigure(0,weight=1)
            self.botFrame.grid_columnconfigure(0,weight=9)
            self.botFrame.grid_columnconfigure(1,weight=11)
            
            
            self.exitButton=tk.Button(self.topFrame,text='Quit',command=lambda : self.back(main)).place(relx=0.98, rely=0.5, anchor=CENTER )
            
            self.changeDataB=tk.Button(self.topFrame,text='Change Info',command=lambda : validationForm(self.root,main,self.rightFrame,self.leftFrame,self.db,self.info,'Change Info')).place(relx=0.915, rely=0.5, anchor=CENTER )
            
            self.seeDataB=tk.Button(self.topFrame,text='Reveal Your Info',command=lambda : validationForm(self.root,main,self.rightFrame,self.leftFrame,self.db,self.info,'Reveal Info')).place(relx=0.825, rely=0.5, anchor=CENTER )
        

    def back(self,main):
        for widget in main.winfo_children():
            widget.destroy()

    def mainf(main,self):     
        Profile(self.root,main,self.db,self.info)
        
        main.mainloop()    


#### SHOW JOURNEY HISTORY -> PAST AND UPCOMING 
class Journeys():
    def __init__(self,root,main,db,info):
        self.root=root
        self.main=main
        self.customerInfo=info
        self.db=db
        #main.geometry('1015x545-50-100')  
        #main.title('Administration Panel')
        
        self.topFrame=tk.Frame(self.main,background='gray80',relief='groove', highlightthickness=2)
        self.topFrame.grid(row=0, sticky='nsew')
    
        self.botFrame=tk.Frame(self.main,background='gray90', highlightthickness=2)
        self.botFrame.grid(row=1,sticky="nswe")
        
        #LEFTSIDE
        self.leftFrame=tk.Frame(self.botFrame,bg='gray90', highlightthickness=2)
        self.leftFrame.grid(row=0,column=0, sticky='nsew')
        #RIGHTSIDE   
        self.rightFrame=tk.Frame(self.botFrame,background='gray90', highlightthickness=2)
        self.rightFrame.grid(row=0,column=1, sticky='nsew')

        main.grid_rowconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=8)
        main.grid_columnconfigure(0, weight=1)
 
        self.botFrame.grid_rowconfigure(0,weight=1)
        self.botFrame.grid_columnconfigure(0,weight=1)
        self.botFrame.grid_columnconfigure(1,weight=1)
        
        self.Title=tk.Label(self.topFrame,borderwidth='218',text="Your World of Possibilities",bd=5,bg='grey80',font=('Adobe Arabic',16,''))
        self.Title.place(x=500,y=30,anchor=CENTER)
        self.exitButton=tk.Button(self.topFrame,text='Quit',command=lambda : self.back(main)).place(relx=0.98, rely=0.5, anchor=CENTER )
    #DATA & QUERIES
    
        sql = f"""SELECT departureAirportID, arrivalAirportID, min(departDate) as d,journeyID
                from (( journeysLegs NATURAL join (select * from Journey where journeyID in
                (select journeyID
                from Ticket
                where customerID = '{self.customerInfo['ID']}')))NATURAL join (SELECT legID, FlightLegs.departDate from FlightLegs))
                group by journeyID 
                order by d """
                
        queryJ="""SELECT Ticket.customerID,Ticket.ticketID ,Journey.journeyID,Journey.journeyDate
                    FROM Journey JOIN Ticket on Ticket.journeyID=Journey.journeyID
                    WHERE ticketID in
                    (SELECT Ticket.ticketID 
                    FROM Ticket , Customer as c
                    WHERE Ticket.customerID='C-55424' and Ticket.customerID=c.ID);"""
        self.importantInfo=self.db.executeSQL(queryJ,show=False)  
        table=self.db.executeSQL(sql,show=False)
       
    
    #LEFT FRAME = PAST JOURNIES
        canvasL=tk.Canvas(self.leftFrame,width=8, height=50,background="grey90", scrollregion=(0,0,3000,3000))
        scr_v1L = tk.Scrollbar(self.leftFrame,orient=VERTICAL)
        scr_v1L.pack(side=RIGHT,fill='y')
        scr_v1L.config(command=canvasL.yview)

        canvasL.config(yscrollcommand=scr_v1L.set)
        canvasL.pack(fill='both',expand=True)
        
        title=tk.Label(canvasL,text='Journey History',background="grey90",font=('Adobe Arabic',20,''))
        canvasL.create_window( 250,+65, window=title)
        todaysDate=tk.Label(canvasL,text=f'Todays date:{date.today()}',background="grey90",font=('Adobe Arabic',12,''))
        canvasL.create_window( 410,+15, window=todaysDate)
        Upcoming=tk.Label(canvasL,text='Upcoming Journeys',background="grey90",fg='blue',font=('Adobe Arabic',17,'underline'))
        canvasL.create_window( 130,+150, window=Upcoming)
        expandList=[]
        for i in range(len(table)):
            if self.comparedates(date.today(),table[i]["d"]):
                label1L=tk.LabelFrame(canvasL,height=150,width=400,bg='grey90',text=f'TicketID:{self.importantInfo[i]["ticketID"]} \n From : {table[i]["departureAirportID"]} To',bd=2,font=('Adobe Arabic',13,''))
                expandLabel=tk.Label(label1L,text='Details',bg='grey90',font=('Adobe Arabic ',12,'underline'))
                expandList.append(expandLabel)
                expandLabel.bind("<Button-1>",self.new_lambda(i))
                label2L=tk.Label(label1L,text=f'{table[i]["arrivalAirportID"]}',bd=5,bg='grey90',font=('Adobe Arabic',20,''))
                label3L=tk.Label(label1L,text=f'Departure Date :{table[i]["d"]}',bd=3,bg='grey90',font=('Adobe Arabic',15,''))
                
                expandLabel.place(relx=0.85,rely=0.0)
                label2L.place(relx=0.22,rely=0.07)
                label3L.place(relx=0.3,rely=0.6)
                canvasL.create_window( 230,(i+1)*180+80, window=label1L)
                lastPointer=(i+1)*180+80
        for i in range(len(table)):
            if  not self.comparedates(date.today(),table[i]["d"]):
                Past=tk.Label(canvasL,text='Older Journeys',background="grey90",fg='blue',font=('Adobe Arabic',17,'underline'))
                canvasL.create_window( 100,+lastPointer+150, window=Past)

                label1L=tk.LabelFrame(canvasL,height=150,width=400,bg='grey90',text=f'TicketID:{self.importantInfo[i]["ticketID"]} \n From : {table[i]["departureAirportID"]} To',bd=2,font=('Adobe Arabic',13,''))
                expandLabel=tk.Label(label1L,text='Details',bg='grey90',font=('Adobe Arabic ',12,'underline'))
                expandList.append(expandLabel)
                expandLabel.bind("<Button-1>",self.new_lambda(i))
                label2L=tk.Label(label1L,text=f'{table[i]["arrivalAirportID"]}',bd=5,bg='grey90',font=('Adobe Arabic',20,''))
                label3L=tk.Label(label1L,text=f'Departure Date :{table[i]["d"]}',bd=3,bg='grey90',font=('Adobe Arabic',15,''))
                
                expandLabel.place(relx=0.85,rely=0.0)
                label2L.place(relx=0.22,rely=0.07)
                label3L.place(relx=0.3,rely=0.6)
                canvasL.create_window( 230,lastPointer+(i+1)*180+80, window=label1L)
            

        canvasL.bbox("all")

    def back(self,main):
        for widget in self.main.winfo_children():
            widget.destroy()
        
    def new_lambda(self,i):
        return lambda x: journeyDetails(self.root,self.main,self.rightFrame,self.db,self.importantInfo[i],False)
    
    def comparedates(self,current,ticketDate):
        newcur=str(current).replace('-','/',3)
        newtick=str(ticketDate).replace('-','/',3)
        cur = datetime.strptime(newcur, "%Y/%m/%d").date()
        tick = datetime.strptime(newtick, "%Y/%m/%d").date()
        if cur>tick:
            return False
        else:
            return True
    
            
    def mainf(self):      
        Journeys(self.main,self.db)
        self.main.mainloop()

class journeyDetails():
    def __init__(self,root,MAIN,main,db,info,action=False):
        
        self.root=root
        self.MAIN=MAIN
        self.db=db
        self.main=main
        self.info=info
        for widget in self.main.winfo_children():
            widget.destroy()
        self.goBack=tk.Button(self.main,text='Go Back',bg='grey90',fg='blue',bd=0,font=('Adobe Arabic',13,'underline'),command=self.back)
        self.goBack.place(relx=0.855,rely=0.01)

        #DATA FOR EXPANDED TICKET  
        legInfoSQL=f"""SELECT legID,departureAirportID,departGate,arrivalAirportID,departDate,departTime,arrivalTime
                from (FlightLegs natural join 
                    (select journeyID,legID,journeyDate from (journeysLegs natural join Journey)
                    WHERE journeyID = {self.info['journeyID']}))
                ORDER by legID,departDate,departTime;"""

        self.legInfo=self.db.executeSQL(legInfoSQL,show=False)
        self.legInfo=self.legInfo
        if len(self.legInfo)==1:
            if not action:
                self.labelframe=tk.LabelFrame(self.main,height=300,width=300,background="grey90",text=f'Ticket ID: {self.info["ticketID"]}',bd=2,font=('Adobe Arabic',13,''))
                self.labelframe.place(relx=0.2,rely=0.2)
                LabelDeparture=tk.Label(self.labelframe,text=f'Departure  from  {self.legInfo[0]["departureAirportID"]} :',bg='grey90',font=('Adobe Arabic ',12,'underline','bold'))
                LabelGate=tk.Label(self.labelframe,text=f'Gate: {self.legInfo[0]["departGate"]}',bg='grey90',font=('Adobe Arabic ',12,''))
                LabelTime=tk.Label(self.labelframe,text=f'Departure Time: {self.legInfo[0]["departTime"]}  ,',bg='grey90',font=('Adobe Arabic ',12,''))
                LabelArrival=tk.Label(self.labelframe,text=f'Arrival  at  {self.legInfo[0]["arrivalAirportID"]} :',bg='grey90',font=('Adobe Arabic bold ',12,'underline','bold'))
                LabelArrivalTime=tk.Label(self.labelframe,text=f'Estimated Time of Arrival: {self.legInfo[0]["arrivalTime"]}',bg='grey90',font=('Adobe Arabic ',12,''))
                dur=self.duration(self.legInfo[0]["departTime"],self.legInfo[0]["arrivalTime"])
                LabelDuration=tk.Label(self.labelframe,text=f'Estimated Duration: {dur} hours',bg='grey90',font=('Adobe Arabic bold',12,'bold'))
                
                LabelDeparture.place(relx=0.01,rely=0.05)
                LabelGate.place(relx=0.6,rely=0.13)
                LabelTime.place(relx=0.01,rely=0.13)
                LabelArrival.place(relx=0.01,rely=0.3)
                LabelArrivalTime.place(relx=0.01,rely=0.385)
                LabelDuration.place(relx=0.1,rely=0.6)
            if action:
                
                self.labelframe=tk.LabelFrame(self.main,height=300,width=300,background="grey90",text=f'Ticket ID: {self.info["ticketID"]}',bd=2,font=('Adobe Arabic',13,''))
                self.labelframe.place(relx=0.2,rely=0.2)
                
                
                self.delete=tk.Button(self.labelframe,text='Delete',fg='blue',bd=0,bg='grey90',font=('Adobe Arabic ',10,''),command=self.deletTicket)
                self.update=tk.Button(self.labelframe,text='New Date/',fg='blue',bd=0,bg='grey90',font=('Adobe Arabic ',10,''),command=self.updateTicket)
                LabelDeparture=tk.Label(self.labelframe,text=f'Departure  from  {self.legInfo[0]["departureAirportID"]} :',bg='grey90',font=('Adobe Arabic ',12,'underline','bold'))
                LabelGate=tk.Label(self.labelframe,text=f'Gate: {self.legInfo[0]["departGate"]}',bg='grey90',font=('Adobe Arabic ',12,''))
                LabelTime=tk.Label(self.labelframe,text=f'Departure Time: {self.legInfo[0]["departTime"]}  ,',bg='grey90',font=('Adobe Arabic ',12,''))
                LabelArrival=tk.Label(self.labelframe,text=f'Arrival  at  {self.legInfo[0]["arrivalAirportID"]} :',bg='grey90',font=('Adobe Arabic bold ',12,'underline','bold'))
                LabelArrivalTime=tk.Label(self.labelframe,text=f'Estimated Time of Arrival: {self.legInfo[0]["arrivalTime"]}',bg='grey90',font=('Adobe Arabic ',12,''))
                dur=self.duration(self.legInfo[0]["departTime"],self.legInfo[0]["arrivalTime"])
                LabelDuration=tk.Label(self.labelframe,text=f'Estimated Duration: {dur} hours',bg='grey90',font=('Adobe Arabic bold',12,'bold'))
                
                self.delete.place(relx=0.84,rely=0.002)
                self.update.place(relx=0.63,rely=0.002)
                LabelDeparture.place(relx=0.01,rely=0.05)
                LabelGate.place(relx=0.6,rely=0.13)
                LabelTime.place(relx=0.01,rely=0.13)
                LabelArrival.place(relx=0.01,rely=0.3)
                LabelArrivalTime.place(relx=0.01,rely=0.385)
                LabelDuration.place(relx=0.1,rely=0.6)
                
     
        if len(self.legInfo)==2:
            if not action:
                self.labelframe=tk.LabelFrame(self.main,height=470,width=350,background="grey90",text=f'Ticket ID: {self.info["ticketID"]}',bd=2,font=('Adobe Arabic',13,''))
                self.labelframe.place(relx=0.1,rely=0.01)
                repeat=0.1
                counter=1
                for leg in self.legInfo:
                    FlightLabel=tk.Label(self.labelframe,text=f'Flight - {counter}',fg='blue',bg='grey90',font=('Adobe Arabic ',10,'underline','bold'))
                    LabelDeparture=tk.Label(self.labelframe,text=f'Departure  from  {leg["departureAirportID"]} :',bg='grey90',font=('Adobe Arabic ',10,'underline','bold'))
                    LabelGate=tk.Label(self.labelframe,text=f'Gate: {leg["departGate"]}',bg='grey90',font=('Adobe Arabic ',10,''))
                    LabelTime=tk.Label(self.labelframe,text=f'- Departure Time: {leg["departTime"]}  ,',bg='grey90',font=('Adobe Arabic ',10,''))
                    LabelArrival=tk.Label(self.labelframe,text=f'Arrival  at  {leg["arrivalAirportID"]} :',bg='grey90',font=('Adobe Arabic bold ',10,'underline','bold'))
                    LabelArrivalTime=tk.Label(self.labelframe,text=f'- Estimated Time of Arrival: {leg["arrivalTime"]}',bg='grey90',font=('Adobe Arabic ',10,''))
                    dur=self.duration(leg["departTime"],leg["arrivalTime"])
                    LabelDuration=tk.Label(self.labelframe,text=f'Estimated Duration: {dur} hours',bg='grey90',font=('Adobe Arabic bold',10,'bold'))
                    
                    FlightLabel.place(relx=0.4,rely=0.005+repeat)
                    LabelDeparture.place(relx=0.01,rely=0.05+repeat)
                    LabelTime.place(relx=0.03,rely=0.1+repeat)
                    LabelGate.place(relx=0.5,rely=0.1+repeat)
                    LabelArrival.place(relx=0.01,rely=0.17+repeat)
                    LabelArrivalTime.place(relx=0.03,rely=0.23+repeat)
                    LabelDuration.place(relx=0.4,rely=0.28+repeat)
                    counter+=1
                    repeat+=0.5
                    
                    
            if action:
                self.labelframe=tk.LabelFrame(self.main,height=470,width=350,background="grey90",text=f'Ticket ID: {self.info["ticketID"]}',bd=2,font=('Adobe Arabic',13,''))
                self.labelframe.place(relx=0.1,rely=0.01)
                repeat=0.1
                counter=1
                for leg in self.legInfo:
                    self.delete=tk.Button(self.labelframe,text='Delete',fg='blue',bd=0,bg='grey90',font=('Adobe Arabic ',10,''),command=self.deletTicket)
                    self.update=tk.Button(self.labelframe,text='New Date/',fg='blue',bd=0,bg='grey90',font=('Adobe Arabic ',10,''),command=self.updateTicket)
                    FlightLabel=tk.Label(self.labelframe,text=f'Flight - {counter}',fg='blue',bg='grey90',font=('Adobe Arabic ',10,'underline','bold'))
                    LabelDeparture=tk.Label(self.labelframe,text=f'Departure  from  {leg["departureAirportID"]} :',bg='grey90',font=('Adobe Arabic ',10,'underline','bold'))
                    LabelGate=tk.Label(self.labelframe,text=f'Gate: {leg["departGate"]}',bg='grey90',font=('Adobe Arabic ',10,''))
                    LabelTime=tk.Label(self.labelframe,text=f'- Departure Time: {leg["departTime"]}  ,',bg='grey90',font=('Adobe Arabic ',10,''))
                    LabelArrival=tk.Label(self.labelframe,text=f'Arrival  at  {leg["arrivalAirportID"]} :',bg='grey90',font=('Adobe Arabic bold ',10,'underline','bold'))
                    LabelArrivalTime=tk.Label(self.labelframe,text=f'- Estimated Time of Arrival: {leg["arrivalTime"]}',bg='grey90',font=('Adobe Arabic ',10,''))
                    dur=self.duration(leg["departTime"],leg["arrivalTime"])
                    LabelDuration=tk.Label(self.labelframe,text=f'Estimated Duration: {dur} hours',bg='grey90',font=('Adobe Arabic bold',10,'bold'))
                    
                    self.delete.place(relx=0.84,rely=0.002)
                    self.update.place(relx=0.63,rely=0.002)
                    FlightLabel.place(relx=0.4,rely=0.005+repeat)
                    LabelDeparture.place(relx=0.01,rely=0.05+repeat)
                    LabelTime.place(relx=0.03,rely=0.1+repeat)
                    LabelGate.place(relx=0.5,rely=0.1+repeat)
                    LabelArrival.place(relx=0.01,rely=0.17+repeat)
                    LabelArrivalTime.place(relx=0.03,rely=0.23+repeat)
                    LabelDuration.place(relx=0.4,rely=0.28+repeat)
                    counter+=1
                    repeat+=0.5
                
      
        if len(self.legInfo)==3:
            if not action:
                self.labelframe=tk.LabelFrame(self.main,height=470,width=350,background="grey90",text=f'Ticket ID: {self.info["ticketID"]}',bd=2,font=('Adobe Arabic',13,''))
                self.labelframe.place(relx=0.1,rely=0.01)
                repeat=0.0
                counter=1
                for leg in self.legInfo:
                    FlightLabel=tk.Label(self.labelframe,text=f'Flight - {counter}',fg='blue',bd=0,bg='grey90',font=('Adobe Arabic ',10,'underline','bold'))
                    LabelDeparture=tk.Label(self.labelframe,text=f'Departure  from  {leg["departureAirportID"]} :',bg='grey90',font=('Adobe Arabic ',10,'underline','bold'))
                    LabelGate=tk.Label(self.labelframe,text=f'Gate: {leg["departGate"]}',bg='grey90',font=('Adobe Arabic ',10,''))
                    LabelTime=tk.Label(self.labelframe,text=f'- Departure Time: {leg["departTime"]}  ,',bg='grey90',font=('Adobe Arabic ',10,''))
                    LabelArrival=tk.Label(self.labelframe,text=f'Arrival  at  {leg["arrivalAirportID"]} :',bg='grey90',font=('Adobe Arabic bold ',10,'underline','bold'))
                    LabelArrivalTime=tk.Label(self.labelframe,text=f'- Estimated Time of Arrival: {leg["arrivalTime"]}',bg='grey90',font=('Adobe Arabic ',10,''))
                    dur=self.duration(leg["departTime"],leg["arrivalTime"])
                    LabelDuration=tk.Label(self.labelframe,text=f'Estimated Duration: {dur} hours',bg='grey90',font=('Adobe Arabic bold',10,'bold'))
                    
                    FlightLabel.place(relx=0.4,rely=0.005+repeat)
                    LabelDeparture.place(relx=0.01,rely=0.05+repeat)
                    LabelTime.place(relx=0.03,rely=0.1+repeat)
                    LabelGate.place(relx=0.5,rely=0.1+repeat)
                    LabelArrival.place(relx=0.01,rely=0.17+repeat)
                    LabelArrivalTime.place(relx=0.03,rely=0.23+repeat)
                    LabelDuration.place(relx=0.4,rely=0.28+repeat)
                    counter+=1
                    repeat+=0.32
            if action:
                self.labelframe=tk.LabelFrame(self.main,height=470,width=350,background="grey90",text=f'Ticket ID: {self.info["ticketID"]}',bd=2,font=('Adobe Arabic',13,''))
                self.labelframe.place(relx=0.1,rely=0.01)
                repeat=0.0
                counter=1
                for leg in self.legInfo:
                    FlightLabel=tk.Label(self.labelframe,text=f'Flight - {counter}',fg='blue',bg='grey90',font=('Adobe Arabic ',10,'underline','bold'))
                    self.delete=tk.Button(self.labelframe,text='Delete',fg='blue',bd=0,bg='grey90',font=('Adobe Arabic ',10,''),command=self.deletTicket)
                    self.update=tk.Button(self.labelframe,text='New Date/',fg='blue',bg='grey90',font=('Adobe Arabic ',10,''),command=self.updateTicket)
                    LabelDeparture=tk.Label(self.labelframe,text=f'Departure  from  {leg["departureAirportID"]} :',bg='grey90',font=('Adobe Arabic ',10,'underline','bold'))
                    LabelGate=tk.Label(self.labelframe,text=f'Gate: {leg["departGate"]}',bg='grey90',font=('Adobe Arabic ',10,''))
                    LabelTime=tk.Label(self.labelframe,text=f'- Departure Time: {leg["departTime"]}  ,',bg='grey90',font=('Adobe Arabic ',10,''))
                    LabelArrival=tk.Label(self.labelframe,text=f'Arrival  at  {leg["arrivalAirportID"]} :',bg='grey90',font=('Adobe Arabic bold ',10,'underline','bold'))
                    LabelArrivalTime=tk.Label(self.labelframe,text=f'- Estimated Time of Arrival: {leg["arrivalTime"]}',bg='grey90',font=('Adobe Arabic ',10,''))
                    dur=self.duration(leg["departTime"],leg["arrivalTime"])
                    LabelDuration=tk.Label(self.labelframe,text=f'Estimated Duration: {dur} hours',bg='grey90',font=('Adobe Arabic bold',10,'bold'))
                    
                    self.delete.place(relx=0.84,rely=0.002)
                    self.update.place(relx=0.63,rely=0.002)
                    FlightLabel.place(relx=0.4,rely=0.005+repeat)
                    LabelDeparture.place(relx=0.01,rely=0.05+repeat)
                    LabelTime.place(relx=0.03,rely=0.1+repeat)
                    LabelGate.place(relx=0.5,rely=0.1+repeat)
                    LabelArrival.place(relx=0.01,rely=0.17+repeat)
                    LabelArrivalTime.place(relx=0.03,rely=0.23+repeat)
                    LabelDuration.place(relx=0.4,rely=0.28+repeat)
                    counter+=1
                    repeat+=0.32

    def duration(self,s1,s2):
        s1 = f'{s1}'+':00'
        s2 = f'{s2}'+':00'
        
        format = '%H:%M:%S'
        dur = str(datetime.strptime(s2, format) - datetime.strptime(s1, format))
        length=len(dur)
        return dur[0:length-3]
    
    def back(self):
        for widget in self.main.winfo_children():
            widget.destroy()
            
    def deletTicket(self):
        response = tkmb.askokcancel("Delete Ticket","Are you sure you want to \n\n   Delete this Ticket ?")
        tID=self.info["ticketID"]
        if response:    # If the answer was "Yes" response is True
            statement=f"""DELETE FROM Ticket
                    WHERE ticketID='{tID}';"""
            self.db.executeSQL(statement,show=False)
            self.root.withdraw()
            id=str(self.info['customerID'])
            updateInfoQuery=f"""SELECT * from Customer where ID='{id}'"""
            updatedInfo=self.db.executeSQL(updateInfoQuery,show=False)
        ### CALL ROOT TO RESET DATA OF CUSTOMER
            customerRoot=tk.Tk()
            customerApp=customerApplication(customerRoot,self.db,updatedInfo[0])
            
            
        else:           # If the answer was "No" response is False
            pass
    ### CHANGE TICKETS OF CUSTOMER
    def updateTicket(self):
        response = tkmb.askokcancel("Change Ticket","Are you sure you want to \n\n   Change this Ticket ?")
        tID=self.info["ticketID"]
        if response:    # If the answer was "Yes" response is True
            statement=f"""DELETE FROM Ticket
                    WHERE ticketID='{tID}';"""
            self.db.executeSQL(statement,show=False)   
            for widget in self.MAIN.winfo_children():
                widget.destroy()
            buyTicket(self.root,self.MAIN,self.db,self.info)
        

    def mainf(self):
        self.main.mainloop()

class Cancel():
    def __init__(self,root,main,db,info):
        self.root=root
        self.main=main
        self.customerInfo=info
        self.db=db
        
        self.topFrame=tk.Frame(self.main,background='gray80',relief='groove', highlightthickness=2)
        self.topFrame.grid(row=0, sticky='nsew')
    
        self.botFrame=tk.Frame(self.main,background='gray90', highlightthickness=2)
        self.botFrame.grid(row=1,sticky="nswe")
        
        #LEFTSIDE
        self.leftFrame=tk.Frame(self.botFrame,bg='gray90', highlightthickness=2)
        self.leftFrame.grid(row=0,column=0, sticky='nsew')
        #RIGHTSIDE   
        self.rightFrame=tk.Frame(self.botFrame,background='gray90', highlightthickness=2)
        self.rightFrame.grid(row=0,column=1, sticky='nsew')

        main.grid_rowconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=8)
        main.grid_columnconfigure(0, weight=1)
        
        
        self.botFrame.grid_rowconfigure(0,weight=1)
        self.botFrame.grid_columnconfigure(0,weight=1)
        self.botFrame.grid_columnconfigure(1,weight=1)
        
        self.Title=tk.Label(self.topFrame,borderwidth='218',text="Your World of Possibilities",bd=5,bg='grey80',font=('Adobe Arabic',16,''))
        self.Title.place(x=500,y=30,anchor=CENTER)
        self.exitButton=tk.Button(self.topFrame,text='Quit',command=lambda : self.back(main)).place(relx=0.98, rely=0.5, anchor=CENTER )
    #DATA & QUERIES
    
        sql = f"""SELECT departureAirportID, arrivalAirportID, min(departDate) as d,journeyID
                from (( journeysLegs NATURAL join (select * from Journey where journeyID in
                (select journeyID
                from Ticket
                where customerID = '{self.customerInfo['ID']}')))NATURAL join (SELECT legID, FlightLegs.departDate from FlightLegs))
                group by journeyID 
                order by d """
                
        queryJ="""SELECT Ticket.customerID,Ticket.ticketID ,Journey.journeyID,Journey.journeyDate
                    FROM Journey JOIN Ticket on Ticket.journeyID=Journey.journeyID
                    WHERE ticketID in
                    (SELECT Ticket.ticketID 
                    FROM Ticket , Customer as c
                    WHERE Ticket.customerID='C-55424' and Ticket.customerID=c.ID);"""
        self.importantInfo=self.db.executeSQL(queryJ,show=False)  
        table=self.db.executeSQL(sql,show=False)
       
    
    #LEFT FRAME 
        canvasL=tk.Canvas(self.leftFrame,width=8, height=50,background="grey90", scrollregion=(0,0,8000,8000))
        scr_v1L = tk.Scrollbar(self.leftFrame,orient=VERTICAL)
        scr_v1L.pack(side=RIGHT,fill='y')
        scr_v1L.config(command=canvasL.yview)

        canvasL.config(yscrollcommand=scr_v1L.set)
        canvasL.pack(fill='both',expand=True)
        
        title=tk.Label(canvasL,text='Journey History',background="grey90",font=('Adobe Arabic',20,''))
        canvasL.create_window( 250,+65, window=title)
        todaysDate=tk.Label(canvasL,text=f'Todays date:{date.today()}',background="grey90",font=('Adobe Arabic',12,''))
        canvasL.create_window( 410,+15, window=todaysDate)
        Upcoming=tk.Label(canvasL,text='Upcoming Journeys',background="grey90",fg='blue',font=('Adobe Arabic',17,'underline'))
        canvasL.create_window( 130,+150, window=Upcoming)
        expandList=[]
        for i in range(len(table)):
            if self.comparedates(date.today(),table[i]["d"]):
                label1L=tk.LabelFrame(canvasL,height=150,width=400,bg='grey90',text=f'TicketID:{self.importantInfo[i]["ticketID"]} \n From : {table[i]["departureAirportID"]} To',bd=2,font=('Adobe Arabic',13,''))
                expandLabel=tk.Label(label1L,text='Select',bg='grey90',font=('Adobe Arabic ',12,'underline'))
                expandList.append(expandLabel)
                expandLabel.bind("<Button-1>",self.new_lambda(i))
                label2L=tk.Label(label1L,text=f'{table[i]["arrivalAirportID"]}',bd=5,bg='grey90',font=('Adobe Arabic',20,''))
                label3L=tk.Label(label1L,text=f'Departure Date :{table[i]["d"]}',bd=3,bg='grey90',font=('Adobe Arabic',15,''))
                
                expandLabel.place(relx=0.85,rely=0.0)
                label2L.place(relx=0.22,rely=0.07)
                label3L.place(relx=0.3,rely=0.6)
                canvasL.create_window( 230,(i+1)*180+80, window=label1L)
        canvasL.bbox("all")
    
    def back(self,main):
        for widget in main.winfo_children():
            widget.destroy()
        
    def new_lambda(self,i):
        return lambda x: journeyDetails(self.root,self.main,self.rightFrame,self.db,self.importantInfo[i],True)
    
    def comparedates(self,current,ticketDate):
        newcur=str(current).replace('-','/',3)
        newtick=str(ticketDate).replace('-','/',3)
        cur = datetime.strptime(newcur, "%Y/%m/%d").date()
        tick = datetime.strptime(newtick, "%Y/%m/%d").date()
        if cur>tick:
            return False
        else:
            return True
        
    def mainf(self):       
        Cancel(self.root,self.main,self.db)
        self.main.mainloop()


 ### VALIDATE INFORMATION OF CUSTOMER TO PROCEED TO CERTAIN ACTIONS
class validationForm():
    def __init__(self,root,MAIN,main,left,db,info,string):
        self.root=root
        self.main=main
        self.MAIN=MAIN
        self.db=db
        self.leftFrame=left
        self.info=info
        self.action=string
        self.frame=tk.Frame(main,background='gray80',relief='groove', highlightthickness=2)
        self.frame.grid(row=0, sticky='nsew')
        xc=100+50
        yc=100+20
        entryx=xc+100
        entryy=yc+2
    #Labels
        titleLabel=tk.Label(self.frame,text='Validation Form', width=20,font=("bold",20) ,bg='gray90').place(x=xc-35,y=yc)
        usernameL=tk.Label(self.frame,text='Username',bg='gray80').place(x=xc+20,y=yc+40*2+3)
        passwordL=tk.Label(self.frame,text='Password',bg='gray80').place(x=xc+20+1,y=yc+40*3)
        
        
    #StringVars   
        self.username=tk.StringVar(self.frame)
        self.password=tk.StringVar(self.frame)
        
        
    #Entries & Entry Placements
        usernameE=tk.Entry(self.frame,  bd=2,textvariable=self.username) 
        passwordE=tk.Entry(self.frame,  bd=2,textvariable=self.password, show='*') 
        usernameE.place(x=entryx,y=entryy+80)
        passwordE.place(x=entryx,y=entryy+118)
        SubmitB=tk.Button(self.frame, text='Submit' , width=20,bg="black",fg='white',command=self.submit).place(x=entryx-40,y=entryy+155)
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_columnconfigure(0, weight=1)
    ##### ACTIONS AFTER USERNAME AND PASSWORD
    ##### CHANGE CUSTOMER INFO 
    ##### REVEAL HIS INFO
    def submit(self):
        if self.info['USERNAME']==self.username.get() and self.info['PASSWORD']==self.password.get():
            if self.action=='Change Info':
                for widget in self.main.winfo_children():
                    widget.destroy()
                changeInfo(self.root,self.MAIN,self.main,self.leftFrame,self.db,self.info) 
            if self.action=='Reveal Info':
                for widget in self.main.winfo_children():
                    widget.destroy()
                for widget in self.leftFrame.winfo_children():
                    widget.destroy()
                for widget in self.MAIN.winfo_children():
                    widget.destroy()

                Profile(self.root,self.MAIN,hdb.DataModel("database.db"),self.info,show=True)
                
    def mainf(self):
        CF=validationForm(self.main,self.db)
        self.main.mainloop()

class changeInfo():
    def __init__(self,root,MAIN,main,left,db,info):
        self.root=root
        self.MAIN=MAIN
        self.main=main
        self.db=db
        self.leftFrame=left
        self.info=info
        xc=90
        yc=70
        entryx=xc+100
        entryy=yc+43
        titleLabel=tk.Label(self.main,text='Select Field', width=20,font=("bold",20) ).place(x=xc+20,y=yc-60)
    #CheckButtons
        self.CV1 = tk.StringVar(self.main)
        self.CV2 = tk.StringVar(self.main)
        self.CV3 = tk.StringVar(self.main)
        self.CV4 = tk.StringVar(self.main)
        self.CV5 = tk.StringVar(self.main)
        self.CV6 = tk.StringVar(self.main)
        self.CV7 = tk.StringVar(self.main)
        self.CV8 = tk.StringVar(self.main)
        

        
        self.usernameL=tk.Checkbutton(self.main,text='Username',variable=self.CV1,onvalue = 'USERNAME', offvalue = '').place(x=xc,y=yc+40*2)
        self.passwordL=tk.Checkbutton(self.main,text='Password',variable=self.CV2,onvalue = 'PASSWORD', offvalue = '').place(x=xc+90,y=yc+40*2)
        self.PostalCodeL=tk.Checkbutton(self.main,text='Posta-Code',variable=self.CV3,onvalue = 'PostalCode', offvalue = '').place(x=xc+180,y=yc+40*2)
        self.CellphoneNumbL=tk.Checkbutton(self.main,text='Cellphone',variable=self.CV8,onvalue = 'CellphoneNumber', offvalue = '').place(x=xc+290,y=yc+40*2)
        
        
        self.CityL =tk.Checkbutton(self.main,text='City',variable=self.CV5,onvalue = 'City', offvalue ='').place(x=xc,y=yc+40*3)
        self.streetAddressL=tk.Checkbutton(self.main,text='Street Address',variable=self.CV6,onvalue = 'streetAdress', offvalue = '').place(x=xc+180,y=yc+40*3)
        self.emailL =tk.Checkbutton(self.main,text='E-mail',variable=self.CV7,onvalue = 'EMAIL', offvalue = '').place(x=xc+90,y=yc+40*3)
        self.CountryL=tk.Checkbutton(self.main,text='Country',variable=self.CV4,onvalue = 'Country', offvalue = '').place(x=xc+290,y=yc+40*3)
        self.select=tk.Button(self.main, text='Select' , width=20,bg="black",fg='white',command=self.submit).place(x=entryx-15,y=entryy+155)
        
        
        
    def submit(self):
        self.CVLIST=[self.CV1 ,self.CV2,self.CV3,self.CV4,self.CV5,self.CV6,self.CV7,self.CV8]
        c=0
        cnone=0
        self.entryList=[]
        xc=90
        yc=70
        entryx=xc+100
        entryy=yc+43
        for widget in self.main.winfo_children():
                    widget.destroy()
        titleLabel=tk.Label(self.main,text='Enter New Credentials', width=20,font=("bold",20) ).place(x=xc+20,y=yc-60)
        for var in self.CVLIST:
            txtlabel=var.get()
            if txtlabel=='':
                cnone+=1
                if c==(len(self.CVLIST)-cnone):
                    SubmitB=tk.Button(self.main, text='Submit Changes' , width=20,bg="black",fg='white',command=self.subChanges).place(x=xc+100,y=yc-60+100)
                else:continue
            else:
                newvar=tk.StringVar(self.main)
                label=tk.Label(self.main,text=f'{txtlabel}'+" :", width=10 ).place(x=xc+70,y=yc-60+100)
                entry=tk.Entry(self.main,bd=2,textvariable=newvar)
                self.entryList.append(entry)
                entry.place(x=xc+150,y=yc-60+100)
                
                yc+=50
                c+=1
                if c==(len(self.CVLIST)-cnone):
                    SubmitB=tk.Button(self.main, text='Submit Changes' , width=20,bg="black",fg='white',command=self.subChanges).place(x=xc+100,y=yc-60+100)
                else:continue
        
        
    def subChanges(self):
        finalQuery=''
        strID=str(self.info['ID'])
        start="""UPDATE Customer """
        mid=self.convertToQuery()
        end=f""" WHERE ID='{strID}'"""
        finalQuery=start+mid+end
        self.db.executeSQL(finalQuery,show=False)
        tk.messagebox.showinfo(title='Action',message='Succesful Change')
        
        for widget in self.main.winfo_children():
            widget.destroy()
        for widget in self.MAIN.winfo_children():
            widget.destroy()
        for widget in self.root.winfo_children():
            widget.destroy()
        
        
        self.root.withdraw()
        id=str(self.info['ID'])
        updateInfoQuery=f""" SELECT * from Customer where ID='{id}'"""
        updatedInfo=self.db.executeSQL(updateInfoQuery,show=False)
        customerRoot=tk.Tk()
        customerApp=customerApplication(customerRoot,self.db,updatedInfo[0])
  
    def convertToQuery(self):
        setQuery='SET '
        string=''
        i=0
        for column in self.CVLIST:
            if column.get()!='':
                value=self.entryList[i].get()
                string+=f'{column.get()}="{str(value)}",'
                i+=1
        setQuery+=string[:-1]
        return setQuery
        
    def mainf(self):        
        CF=changeInfo(self.main,self.leftFrame,self.db,self.info)
        self.main.mainloop()



import tkinter as tk
from datetime import *
class journeyDetails():
    def __init__(self,root,main,db,info):
        self.root=root
        self.db=db
        print(info)
        self.main=main
        #self.main.geometry('300x150-50-150')
        self.info=info

        self.goBack=tk.Button(self.main,text='Go Back',bg='grey90',fg='blue',bd=0,font=('Adobe Arabic',13,'underline'),command=self.back)
        self.goBack.place(relx=0.855,rely=0.01)
        
        
        
        
        #DATA FOR EXPANDED TICKET  
        legInfoSQL=f"""SELECT legID,departureAirportID,departGate,arrivalAirportID,departDate,departTime,arrivalTime
                from (FlightLegs natural join 
                    (select journeyID,legID,journeyDate from (journeysLegs natural join Journey)
                    WHERE journeyID = {self.info['journeyID']}))
                ORDER by legID,departDate,departTime;"""
                
                
                
        self.legInfo=self.db.executeSQL(legInfoSQL,show=True)
        print(self.legInfo)
        self.legInfo=self.legInfo
        if len(self.legInfo)==1:
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
            
            
        if len(self.legInfo)==2:
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
            
            
            
        if len(self.legInfo)==3:
            self.labelframe=tk.LabelFrame(self.main,height=470,width=350,background="grey90",text=f'Ticket ID: {self.info["ticketID"]}',bd=2,font=('Adobe Arabic',13,''))
            self.labelframe.place(relx=0.1,rely=0.01)
            repeat=0.0
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
                #LabelGate.place(relx=0.5,rely=0.1+repeat)
                LabelArrival.place(relx=0.01,rely=0.17+repeat)
                LabelArrivalTime.place(relx=0.03,rely=0.23+repeat)
                LabelDuration.place(relx=0.4,rely=0.28+repeat)
                counter+=1
                repeat+=0.32
        
        #Destination=tk.Label(labelframe,text=f'{self.info[1]}',bd=5,bg='white',font=('Adobe Arabic',20,''))
        #Destination.place(relx=0.01,rely=0.01)
        #
        #travelDate=tk.Label(labelframe,text=f'Departure Date :{ self.info[2]}',bd=3,bg='white',font=('Adobe Arabic',15,''))
        #travelDate.place(relx=0.01,rely=0.3)
    
    
    
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
        #main=tk.Tk()
        #journeyDetails(main,1,1,'info')
        #main.mainloop()
        self.main.mainloop()
#journeyDetails.mainf()
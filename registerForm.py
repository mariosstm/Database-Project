import tkinter as tk
from tkinter import ttk
import handleDataBase as hdb
from random import *
class registerForm():
    def __init__(self,main,db):
        self.main=main
        self.db=db
        main.title("Registration Form")
        main.geometry("500x550+350+50")

        xc=60+80
        yc=100
        entryx=xc+100
        entryy=yc+2
    #Labels
        titleLabel=tk.Label(main,text='Enter Credentials', width=20,font=("bold",20) ).place(x=xc-45,y=yc-60)
        FnameL=tk.Label(main,text='First Name').place(x=xc,y=yc)
        LnameL=tk.Label(main,text='Last Name').place(x=xc,y=yc+40)
        usernameL=tk.Label(main,text='Username').place(x=xc,y=yc+40*2)
        passwordL=tk.Label(main,text='Password').place(x=xc,y=yc+40*3)
        PostalCodeL=tk.Label(main,text='Posta-Code').place(x=xc,y=yc+40*4)
        CountryL=tk.Label(main,text='Country').place(x=xc,y=yc+40*5)
        CityL =tk.Label(main,text='City').place(x=xc,y=yc+40*6)
        streetAddressL=tk.Label(main,text='Street Address').place(x=xc,y=yc+40*7)
        emailL =tk.Label(main,text='E-mail').place(x=xc,y=yc+40*8)
        CellphoneNumbL=tk.Label(main,text='Cellphone').place(x=xc,y=yc+40*9)
        
    #StringVars   
        self.Fname=tk.StringVar(main)
        self.Lname=tk.StringVar(main)
        self.username=tk.StringVar(main)
        self.password=tk.StringVar(main)
        self.PostalCode=tk.StringVar(main)
        self.Country=tk.StringVar(main)
        self.City=tk.StringVar(main)
        self.streetAddress=tk.StringVar(main)
        self.email=tk.StringVar(main)
        self.CellphoneNumb=tk.StringVar(main)
        
    #Entries & Entry Placements

        FnameE= tk.Entry(main, bd=2,textvariable=self.Fname) 
        LnameE=tk.Entry(main,  bd=2,textvariable=self.Lname) 
        usernameE=tk.Entry(main,  bd=2,textvariable=self.username) 
        passwordE=tk.Entry(main,  bd=2,textvariable=self.password, show='*') 
        PostalCodeE=tk.Entry(main,  bd=2,textvariable=self.PostalCode) 
        CountryE=tk.Entry(main,  bd=2,textvariable=self.Country) 
        CityE=tk.Entry(main,  bd=2,textvariable=self.City) 
        streetAddressE=tk.Entry(main,  bd=2,textvariable=self.streetAddress)
        emailE=tk.Entry(main,  bd=2,textvariable=self.email)
        CellphoneNumbE=tk.Entry(main,  bd=2,textvariable=self.CellphoneNumb)
        
        FnameE.place(x=entryx,y=entryy)
        LnameE.place(x=entryx,y=entryy+40)
        usernameE.place(x=entryx,y=entryy+80)
        passwordE.place(x=entryx,y=entryy+118)
        PostalCodeE.place(x=entryx,y=entryy+118+40)
        CountryE.place(x=entryx,y=entryy+118+80)
        CityE.place(x=entryx,y=entryy+2*118)
        streetAddressE.place(x=entryx,y=entryy+2*118+40)
        emailE.place(x=entryx,y=entryy+2*118+80)
        CellphoneNumbE.place(x=entryx,y=entryy+3*118)
        
        
        SubmitB=tk.Button(main, text='Submit' , width=20,bg="black",fg='white',command=self.submitDB).place(x=entryx-50,y=entryy+3*118+40)
        
    def submitDB(self):
        
        names=['ID','Fname','Lname','USERNAME','PASSWORD','PostalCode','Country','City','streetAddress','email','CellphoneNumber']
        self.ID=str(randint(0,99999))
        val=[self.ID,self.Fname.get(),self.Lname.get(),self.username.get(),self.password.get(),self.PostalCode.get(),self.Country.get(),self.City.get(),self.streetAddress.get(),self.email.get(),self.CellphoneNumb.get()]
        CustCredentials= dict(zip(names, val))
        print(CustCredentials)
        self.db._insertIntoTable( "Customer", CustCredentials)
        self.db.readTable('Customer')
        self.main.destroy()
        self.db.close()
            
    def mainf():
        dbfile='database.db'
        db=hdb.DataModel(dbfile)
        window = tk.Tk()
        RF=registerForm(window,db)
        
        
        window.mainloop()

    
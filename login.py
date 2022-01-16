from tkinter import *
from functools import partial
#from PIL import Image, ImageTk
from tkinter.messagebox import showinfo
#import AdminUI as AdminUI
import CustomerUI as CUI
import handleDataBase as hdb
from registerForm import registerForm

	
class App():
    def __init__(self,main,dbfile):
        
        self.dbfile=dbfile
        main.geometry('500x600+40+5')  
        main.title('Welcome to TerminalA')
        self.canvas=Canvas(main,height=1200, width=1200)
        self.canvas.pack(expand=YES,fill=BOTH)
        self.my_image=PhotoImage(file='airportTerm.png')
        self.image_on_canvas=self.canvas.create_image(0,0,image=self.my_image)
        
        #username label and text entry box
        self.usernameLabel = Label(main,bg="white smoke",borderwidth=6,relief="ridge", text="Username").place(relx=0.275,rely=0.40,anchor=CENTER)
        self.username = StringVar(main)
        self.usernameEntry = Entry(main, bd=7,textvariable=self.username).place(relx=0.5,rely=0.40,anchor=CENTER)

        #password label and password entry box
        self.passwordLabel = Label(main,bg="white smoke",borderwidth=6,relief="ridge",text="Password").place(relx=0.275,rely=0.45,anchor=CENTER)
        self.password = StringVar(main)
        self.passwordEntry = Entry(main,bd=7 ,textvariable=self.password, show='*').place(relx=0.5,rely=0.45,anchor=CENTER)
        
        #login button
        self.loginButton = Button(main, text="Login", command=self.validateLogin).place(relx=0.5,rely=0.5,anchor=CENTER)
        
        
        #Register Button to Create Account
        self.Register=Button(main,text='Sign Up',command=self.registration).place(relx=0.93,rely=0.96,anchor='center')
    #Registration Form to Sign Up   
    def registration(self):
        self.dbRegister=hdb.DataModel(self.dbfile)
        newWin=Tk()
        self.regform=registerForm(newWin,self.dbRegister)
        self.regform.mainf
        
    #Validate your username and password input    
    def validateLogin(self):
        self.dbLogin=hdb.DataModel(self.dbfile)
        user=self.username.get()
        passW=self.password.get() 
        check=self.dbLogin.readTable('Customer')
        
        
        if (user=='' and passW==''):
                print("Invalid Username or Password.")
        else:
            for i in check:
                if user==i["USERNAME"] and passW==i["PASSWORD"]:
                    
                    root.withdraw() #withraw login window
                    
                    #create customer Panel
                    customerRoot=Tk()
                    customerApp=CUI.customerApplication(customerRoot,self.dbLogin,i)
                    customerRoot.mainloop()
                    
                else:
                    self.popup_window
                    
        
    
    def popup_window(self):
        window = Toplevel()

        label = Label(window, text="Hello World!")
        label.pack(fill='x', padx=50, pady=5)

        button_close = Button(window, text="Close", command=window.destroy)
        button_close.pack(fill='x')

    def popup_showinfo():
        showinfo("ShowInfo", "Invalid Username or Password.")
        
if __name__=='__main__':
    dbfile='database.db'
    
    
    root = Tk()
    app=App(root,dbfile)
    root.mainloop()
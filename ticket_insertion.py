import datetime
import sqlite3
import random
import usefulFunctions as myFuncs


def makeTicket(dbHandler,customerID,journeyID,TicketType,discount):
    
    #Ημερομηνία, TicketID, TicketType
    ticketID = str(random.randint(10000,60000)) + "-" + str(random.randint(100,3000))
    d = datetime.datetime.today()
    BuyingDate = str(d.year) +"-"+ str(d.month//10) + str(d.month%10) + "-" +str(d.day//10) + str(d.day%10)

    #Συνολική απόσταση, ημερομηνία, πλήθος κατελειμένων θέσεων ταξιδιού
    query =f"""SELECT sum(DISTINCT travelDistance) as "totalDistance", min(departDate) as "journeyDate", (SELECT count(*) from Ticket where journeyID = {journeyID}) as "seatsTaken"
    from (journeysLegs NATURAL JOIN FlightLegs)
    where journeyID = {journeyID}
    """
    data = dbHandler.executeSQL(query)[0]

    

    cost = int(data['totalDistance']*0.05) + random.randint(-10,10)
    if TicketType == "business class":
        cost*=2
        
    cost=int(cost*(1-discount))
    
    
    NVB = myFuncs.setNDaysLater(data['journeyDate'],-30)
    NVA = myFuncs.setNDaysLater(data['journeyDate'],-1)

    ticket = {"ticketID":ticketID, "Date":BuyingDate, "NVA":NVA, "NVB":NVB, "TicketType":TicketType,"customerID":customerID, "JourneyID":journeyID, "SeatNumber" : data['seatsTaken']+1, "Cost" : cost}
    dbHandler._insertIntoTable("Ticket",ticket)
    return ticket


#try: conn = sqlite3.connect("αερολιμένας1.db")

#except sqlite3.Error as e:
#    print(e)

#c = conn.cursor()

#Επιλογή ταξιδιού, πελάτη
"""
a = input("1 - Random ταξίδι, πελάτης \n2 - Χειροκίνητη επιλογή \n")
if a == '1' :
   
    N = int(input("Πόσα εισητηριά: "))
    for i in range(N):
        query = #select Customer.ID,Journey.journeyID
        from Customer, Journey
        order by random()
        limit 1
        #
        c.execute(query)

        (customerID,journeyID) = c.fetchall()[0]

        ticket = makeTicket(conn,customerID,journeyID,(["regular"]*9+["business class"])[random.randint(0,9)])
        print(i+1)
        insertToDB(conn,"Ticket",ticket)
        
        
elif a == '2':
    customerID = input("Κωδικός πελάτη: ")
    journeyID = input("Κωδικός Ταξιδιού: ")
    TicketType = ["regular","business class"][int(input("0-Regular \n1-Business class\n"))]
    discount = getDiscount(conn, customerID)
    if discount:
            print("dikaiousai ekptwsh 50%")
    ticket = makeTicket(conn,customerID,journeyID,TicketType,discount)
    insertToDB(conn,"Ticket",ticket)
    for i in ticket:
        print(i,":",ticket[i])
    print()
else :
    print("Πάτα 1 η 2")


conn.close()
"""

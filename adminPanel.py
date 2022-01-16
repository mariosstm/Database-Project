import flightSubmissionForm as flightForm
import handleDataBase
import tkinter
import usefulFunctions as myFuncs
import matplotlib.pyplot as plt

# ~~~~~~~~~~~~~~~~~~~~~~ Εισαγωγή πτήσης ~~~~~~~~~~~~~~~~~~~
def insertFlight():
    root = tkinter.Tk()
    flightForm.FlightForm(root,myDbHandler)
    root.mainloop()
    return

# ~~~~~~~~~~~~~~~~~~~~~~ Εκτύπωση λεξικού με ευανάγνωστη μορφή
def printDictRows(dictList,L):
    formatString = '{:'+str(L)+'}'
    for i in [str(j) for j in dictList[0].keys()]:
        if len(i)>L:
            i = i[0:L-2]+'..'
        print(formatString.format(i),end = '')
    print()
    print('-'*(L-1)*len(dictList[0].keys()))
    for dictionary in dictList:
        for val in [str(j) for j in dictionary.values()]:
            if len(val)>L:
                val = val[0:L]
            print(formatString.format(val),end = '')
        print()

def getLimit():
    while(True):
        N = input("Limit: ")
        if N.isdigit():
            return N

# ~~~~~~~~~~~~~~~~~~~~~~ Στατιστικα ~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~ Στατιστικά Πελατών ~~~~~~~~~~~~~~~~
#Επιλογή κορυφαίου πελάτη βάσει κάποιου κριτηρίου που υποδεικνύει το request
#request = 1: κορυφαίος βάσει πλήθους εισιτηρίων που έχει αγοράσει
#request = 2: κορυφαίος βάσει χρημάτων που έχει συνολικά πληρώσει
#request = 3: κορυφαίος βάσει μεσου  χρημ. ποσου που έχει πληρώσει ανα εισιτήριο
#request = 4: κορυφαίος βασει εναέριων χλμ που έχει διανύσει
#byMonth:  Αν true, βρίσκει τους κορυφαίους σε ένα εύρος μηνών που δίνεται στην monthList [αρχικος μηνας, τελικός μήνας]
#Ν: πλήθος πελατών που θα δείξει (πχ δειξε μου τους πρώτους Ν=10 κορυφαίους πελάτες βασει ταδε...)
def topCustomers(request,byMonth,monthList,N):
    fromTable = 'Ticket'
    dateQuery = ''
    if request == 1:
        criterion = 'count(*)'
        rowName = 'Πλήθος εισιτηρίων'
    elif request == 2:
        criterion = 'sum(cost)'
        rowName = 'Συνολικες αγορές'
    elif request == 3:
        criterion = 'round(avg(cost),2)'
        rowName = 'Κόστος ανα εισιτήριο'
    #Μονο στην τελευταια περίπτωση ο πίνακας που δίνεται στη from δεν είναι π Ticket
    elif request == 4:
        criterion = 'sum(travelDistance)'
        rowName = 'Συνολική απόσταση (χλμ)'
        fromTable = '((Ticket NATURAL join journeysLegs) NATURAL join FlightLegs)'

    #Σε περίπτωση που επιλεγει ευρος μηνών
    if byMonth:
        [m1,m2] = monthList
        earliestDate = myFuncs.setNDaysLater(f'2022-{str(m1//10)+str(m1%10)}-01',-1)
        latestDate = myFuncs.setNDaysLater(f'2022-{str(m2//10)+str(m2%10)}-01',-1)
        dateQuery = f"""where NVA >= '{earliestDate}' and NVA < '{latestDate}'"""
    
    
    nestedQuery = f"""
                    select customerID as ID,{criterion} as c
                    from {fromTable}
                    {dateQuery}
                    group by customerID
                    ORDER by {criterion} desc
                    limit {N}
                """
    totalQuery = f"""SELECT Fname,Lname,ID,c as '{rowName}'
                    from (customer natural join ({nestedQuery}))"""
    #δεικτοδότηση
    myDbHandler.executeSQL("""CREATE INDEX custIDind on Customer(ID)""")
    if byMonth:
        myDbHandler.executeSQL("""CREATE INDEX NVAind on Ticket(NVA)""")
    res = myDbHandler.executeSQL(totalQuery)
    
    myDbHandler.executeSQL("""DROP INDEX custIDind""")
    if byMonth:
        myDbHandler.executeSQL("""DROP INDEX NVAind""")
    if res:
        print()
        printDictRows(res,16)
    else:
        print("Δεν επιστράφηκαν αποτελέσματα")
    return

#Ιστορικο ταξιδιων του πελάτη με την εταιρεία
def customerHistory():
    customerID = input('Customer ID: ')

    #Query για ευρεση πληροφοριών του πελάτη
    infoQuery = f"""select * from Customer where ID = '{customerID}'"""

    #Query για ευρεση Ιστορικου Ταξιδιών του πελάτη
    journeyHistoryQuery = f"""
                            select journeyDate as 'Ημερομηνία',departureAirportID as 'Από',arrivalAirportID as 'Προς'
                            from Ticket,Journey
                            WHERE Ticket.customerID = '{customerID}'
                            and Ticket.JourneyID = Journey.journeyID
                            ORDER by journeyDate
                           """
    #Query για ευρεση στατιστικών στοιχείων του πελάτη
    statsQuery = f"""select count(*) as 'Συνολικά Ταξίδια',sum(cost) as 'Συνολικές Αγορές',round(avg(cost),2) as 'Μέσο Κόστος ανα ταξίδι',ROUND(sum(dist),2) as 'Συνολική απόσταση'

                    from (
                    (select journeyID,cost from ticket where customerID= '{customerID}') 

                    natural join 

                    (select journeyID, sum(travelDistance) as dist 
                    FROM (journeysLegs natural join FlightLegs) 
                    GROUP by journeyID)
                    )"""
    #Χρήση ευρετηρίου: Όλα τα queries αναζητουν στον πίνακα Ticket βασει του γνωρίσματος customerID του Table αυτου
    #Έτσι φτιάχνω ένα index στον συγκεκριμένο γνώρισμα
    myDbHandler.executeSQL("""CREATE INDEX custIDind on Ticket(CustomerID)""")
    
    info = myDbHandler.executeSQL(infoQuery)
    history = myDbHandler.executeSQL(journeyHistoryQuery)
    stats = myDbHandler.executeSQL(statsQuery)
    if not info:
        print("Ο πελάτης δεν υπάρχει στη βάση")
    else:
        print("\n\n~~~~ Πληροφορίες ~~~~\n")
        for i in info[0]:
            if i != 'PASSWORD':
                print(i,'->',info[0][i])
        
        if history:
            print("\n\n~~~~ Ιστορικό Πτήσεων ~~~~\n")
            printDictRows(history,13)
            
        if stats:
            print("\n\n~~~~ Στατιστικά ~~~~\n")
            for i in stats[0]:
                print(i,'->',stats[0][i])
        else:
            print('Ο πελάτης',customerID,'δεν έχει ιστορικό με την εταιρεία')
        
    
    myDbHandler.executeSQL("""DROP INDEX custIDind""")
    return


# ~~~~~~~~~~~~~~~ Στατιστικά των πελατών: ανάλογα το input διαλέγει λειτουργία
def customerStats():
    while(True):
        print()
        print("~~~~ Στατιστικά Πελατών ~~~~")
        print(" 1: Κορυφαίοι Πελάτες")
        print(" 2: Ιστορικό Πελατών")
        print("-1: Έξοδος")
        a = input('Επιλογή: ')
        if a == '1':
            
            #request
            while(True):
                print('request = 1: κορυφαίος βάσει πλήθους εισιτηρίων που έχει αγοράσει')
                print('request = 2: κορυφαίος βάσει χρημάτων που έχει συνολικά πληρώσει')
                print('request = 3: κορυφαίος βάσει μεσου  χρημ. ποσου που έχει πληρώσει ανα εισιτήριο')
                print('request = 4: κορυφαίος βασει εναέριων χλμ που έχει διανύσει')
                request = input()
                if request.isdigit():
                    request = int(request)
                if request in [1,2,3,4]:
                    break
            #Όριο
            N = getLimit();
                
            #πιλογή ευρους μηνών, προαιρέτικό
            byMonth = (input('Βάσει μηνών? 1-Ναι, 0-Οχι: ') == '1')
            monthList = []
            if byMonth:
                for i in range(2):
                    while(True):
                        month = input("Μήνας "+str(i+1)+'(1 ως 12): ')
                        if month.isdigit() and int(month) in [k for k in range (1,13)] and (len(monthList) == 0 or (len(monthList) == 1 and int(month) >= monthList[0])):
                            monthList.append(int(month))
                            break
            topCustomers(request,byMonth,monthList,N)     
            
        elif a == '2':
            customerHistory()
        elif a == '-1':
            break
        
    return

# ~~~~~~~~~~~~~~~~~~~~~~ Στατιστικά Πτήσεων ~~~~~~~~~~~~~~~~
#Request = 1: Pie chart προτιμήσεων προορισμών
#Request = 2: Δημοφιλέστεροι/Λιγότερο δημοφιλείς προορισμοι 
def destinationStats(request,byMonth,month):
    dateQuery = ""
    orderQuery = ""
    if byMonth:
        minDate = '2022-'+str(month//10)+str(month%10)+'-01'
        maxDate = '2022-'+str((month+1)//10)+str((month+1)%10)+'-01'
        dateQuery = f"""where journeyDate >= '{minDate}' and journeyDate < '{maxDate}'"""
    if request == 2:
        priority = ''
        while(True):
            print(' 1: Δημοφιλέστερα')
            print(' 2: Λιγότερο Δημοφιλή')
            a = input('Επιλογή: ')
            if a == '1':
                priority = 'desc'
                break
            elif a == '2':
                break
        N = getLimit()
        orderQuery = f"""ORDER BY count(*) {priority}
                        limit {N}"""
            
    totalQuery = f"""SELECT arrivalAirportID as 'Τοποθεσία',count(*) as 'Αριθμός Επισκέψεων'
                        from (Ticket NATURAL join Journey)
                        {dateQuery}
                        GROUP by arrivalAirportID
                        {orderQuery}"""

    myDbHandler.executeSQL("""CREATE INDEX ArrInd on journey(arrivalAirportID)""")
    if byMonth:
         myDbHandler.executeSQL("""CREATE INDEX dateInd on journey(journeyDate)""")

    destData =  myDbHandler.executeSQL(totalQuery)
    if request == 1:
        if destData:
            labels = []
            visits = []
            for i in destData:
                labels.append(i["Τοποθεσία"])
                visits.append(int(i['Αριθμός Επισκέψεων']))
            plt.pie(visits, labels=labels,autopct='%1.1f%%', shadow=True, startangle=90)
            plt.axis('equal')
            if byMonth :
                title = "Πτήσεις το μήνα " + ['Ιανουάριο',"Φεβρουάριο","Μάρτιο","Απρίλιο","Μάιο","Ιούνιο","Ιούλιο","Αυγουστο","Σεπτέμβριο","Οκτώβριο","Νοέμβριο","Δεκέμβριο"][month - 1]
            else :
                title = 'Πτήσεις όλο το χρόνο'
            plt.title(title)
            plt.show()


    elif request == 2:
        if destData:
            printDictRows(destData,15)
    
    myDbHandler.executeSQL("""DROP INDEX ArrInd""")
    if byMonth:
         myDbHandler.executeSQL("""DROP INDEX dateInd""")
    return

def megisthPlhrothta():
    while(True):
        N = input("Limit: ")
        if N.isdigit():
            break
    query = f"""select journeyID,count(*) as "Κατελλειμένες Θέσεις", min(numberOfSeats) as "διαθέσιμες θέσεις",round(cast(count(*) as float)/cast(min(numberOfSeats) as float),2) as 'Πληρότητα'
        from ((((journeysLegs NATURAL JOIN FlightLegs) NATURAL join Controls) NATURAL join (select aircraftID as airplaneID,numberOfSeats from Aircraft))natural join Ticket)
        GROUP by journeyID
        order by round(cast(count(*) as float)/cast(min(numberOfSeats) as float),2) desc
        limit {N}"""
    data = myDbHandler.executeSQL(query)
    if data:
        print("\n\n~~~~ Οι",N,"πτήσεις με τη μεγαλύτερη πληρότητα ~~~~\n")
        printDictRows(data,15)
    return

def flightPopularityStats():
    while(True):
        print()
        print("~~~~ Στατιστικά Δημοφιλίας Πτήσεων ~~~~")
        print(" 1: Συνολικά Στατιστικά Προορισμών")
        print(" 2: Δημοφιλέστεροι/Λιγότερο Δημοφιλείς προορισμοί")
        print(" 3: Πτήσεις με τη μέγιστη πληρότητα")
        print("-1: έξοδος")
        a = input('Επιλογή: ')
        if a == '1' or a == '2':
            byMonth = (input('Βάσει μηνών? 1-Ναι, 0-Οχι: ') == '1')
            month = 0
            if byMonth:
                while(True):
                    month = input("Μήνας(1 ως 12): ")
                    if month.isdigit() and int(month) in [k for k in range (1,13)]:
                        month = int(month)
                        break
            destinationStats(int(a),byMonth,month)
        if a == '3':
            megisthPlhrothta()
        if a == '-1':
            break
    return

def distanceStats():
    while(True):
        print("~~~~ Στατιστικά που αφορούν στα Μήκη των πτήσεων ~~~~")
        print(" 1: Οι μακρύτερες/πιο σύντομες πτήσεις")
        print(" 2: Ποσοστό πτήσεων πάνω και κάτω από μία δοθείσα τιμή αποστασης")
        print("-1: Έξοδος")
        a = input("Επιλογή: ")

        queryPart = """select journeyID,sum(travelDistance) as "Συνολική Εναέρια Απόσταση"
                        from ((Journey NATURAL JOIN journeysLegs)NATURAL join FlightLegs)
                        group by journeyID
                    """
        if a == '1':
            print(" 1: Μεγαλύτερες πτήσεις")
            print(" 2: Συντομότερες πτήσεις")
            choice = input("Επιλογή: ")
            N = getLimit()
            priority = ""
            if choice == '1':
                priority = 'desc'
            totalQuery = f"""{queryPart}
                             order by sum(travelDistance) {priority}
                             limit {N}
                          """
            data = myDbHandler.executeSQL(totalQuery)
            if data:
                printDictRows(data,15)
                
        elif a == '2':
            L = getLimit()
            L = float(L)
            distanceQuery1 = f"""HAVING sum(travelDistance) <= {L}"""
            distanceQuery2 = f"""HAVING sum(travelDistance) > {L}"""
            totalQuery = f"""select count(*) as "underL"
                            from ({queryPart} {distanceQuery1});
                            
                            select count(*) as "overL"
                            from ({queryPart} {distanceQuery2});
                         """
            data = myDbHandler.executeSQL(totalQuery)
            if data:
                labels = [f"<={L}",f">{L}"]
                pct = [data[0]["underL"],data[1]["overL"]]
                plt.pie(pct, labels=labels,autopct='%1.1f%%', shadow=True, startangle=90)
                plt.axis('equal')
                title = 'Μήκος Πτήσεων σε χλμ'
                plt.title(title)
                plt.show()
                
        elif a == '-1':
            break
    return

#Πληροφορίες Για τους επιβάτες μίας πτήσης
def passengerInfo():
    journeyID = input("journeyID: ")
    if not myDbHandler.executeSQL(f"""SELECT * FROM journey WHERE journeyID = '{journeyID}'"""):
        print("Το Ταξίδι αυτο δεν υπάρχει στη βάση")
        return
    queryPassengers = f"""select Fname,Mname,TicketType,SeatNumber
                        from customer,Ticket
                        WHERE Ticket.JourneyID = '{journeyID}'
                        and Ticket.customerID = ID
                        order by random()
                      """
    passengers = myDbHandler.executeSQL(queryPassengers)
    if passengers:
        print("\n\n~~~~ Όλοι οι επιβάτες για την πτήση",journeyID,"~~~~")
        printDictRows(passengers,16)
    else:
        print("Η συγκεκριμένη πτήση δεν έχει επιβάτες μέχρι στιγμήςS")
    return 



##
def flightStats():
    while(True):
        print()
        print("~~~~ Στατιστικά Πτήσεων ~~~~")
        print(" 1: Στατιστικά δημοφιλίας Πτήσεων")
        print(" 2: Στατιστικά Μήκους Ταξιδιών")
        print(" 3: Πληροφορίες Πτήσης")
        print("-1: έξοδος")
        a = input('Επιλογή: ')

        if a == '1':
            flightPopularityStats()

        elif a == '2':
            distanceStats()
        elif a == '3':
            passengerInfo()
        elif a == '-1':
            break
        
    return

def stats():
    while(True):
        print()
        print("~~~~ Στατιστικά ~~~~")
        print(" 1: Στατιστικά Πελάτων")
        print(" 2: Στατιστικά Πτήσεων")
        print("-1: έξοδος")
        a = input('Επιλογή: ')
        if a == '1':
            customerStats()
        
        elif a == '2':
            flightStats()
        
        elif a == '-1':   
            print("Επιστροφή στο Κύριο Μενού")
            break
    return

def mainMenu():
    print("\n\nΚΑΛΩΣΗΡΘΑΤΕ ADMIN")
    while(True):
        print()
        print("~~~~ ΚΥΡΙΟ ΜΕΝΟΥ ~~~~")
        print(" 1: Εισαγωγή Πτήσης")
        print(" 2: Στατιστικά Στοιχεία")
        print("-1: έξοδος")
        a = input('Επιλογή: ')
        if a == '1':
            insertFlight()
        elif a == '2':
            stats()
        elif a == '-1':
            print('Ευχαριστούμε')
            break
    return

myDbHandler = handleDataBase.DataModel('database.db')
mainMenu()

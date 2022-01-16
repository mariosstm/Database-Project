import usefulFunctions
import sqlite3


"""
 ---- REQUEST ----
request = 1 -> ολα τα ταξίδια
request = 2 -> ταξιδι μία συγκεκριμένη ημερομηνία
request = 3 -> όλα τα ταξίδια από μία ημεομηνια και μετα
request = 4 -> όλα τα ταξίδια σε ένα έυρος ημερομηνιών

numberOfLegs = πόσα πόδια θέλεις να έχει
"""
def getJourneys(dbHandler,request,whereFrom,whereTo,numberOfLegs,date1='',date2='', show = False):


    queryString = ''
    if request == 2:
        queryString = f"""and journeyDate = '{date1}'"""
    elif request == 3:
        queryString = f"""and journeyDate >= '{date1}'"""
    elif request == 4:
        queryString = f"""and '{date1}' <= journeyDate and journeyDate <= '{date2}'"""    
        
    viewName = whereFrom+'to'+whereTo
    createViewQuery = f"""CREATE VIEW {viewName}
    as
    select journeyID,departureAirportID,arrivalAirportID,journeyDate,departTime,arrivalTime,legID,travelDistance
    from ((FlightLegs natural join journeysLegs) natural join 
            (select journeyID,journeyDate
            from Journey
            WHERE departureAirportID = '{whereFrom}' 
            and arrivalAirportID = '{whereTo}'))
    where journeyDate>date('now')
    {queryString}
    ORDER by journeyDate,journeyID,departTime;"""


    queryApeutheias = f"""select journeyID,journeyDate,departureAirportID as 'From',departTime,'--' as 'Στάση 1','--' as 's1ArrTime','--' as 's1DepTime','--' as 'Στάση 2','--' as 's2ArrTime','--' as 's2DepTime',arrivalAirportID as 'To',arrivalTime,cast(round(0.05*travelDistance) as int) as 'cost'
                    FROM {viewName}
                    where departureAirportID = '{whereFrom}'
                    and arrivalAirportID = '{whereTo}'"""

    query1stash = f"""select L1.journeyID,L1.journeyDate,L1.departureAirportID as 'From',L1.departTime,L1.arrivalAirportID as 'Στάση 1',L1.arrivalTime as 's1ArrTime',L2.departTime as 's1DepTime','--' as 'Στάση 2','--' as 's2ArrTime','--' as 's2DepTime',L2.arrivalAirportID as 'To',L2.arrivalTime,cast(round(0.05*(L1.travelDistance + L2.travelDistance)) as int) as 'cost'
                    FROM {viewName} as L1 left OUTER join {viewName} as L2
                    where L1.journeyID = L2.journeyID 
                    and L1.departureAirportID ='{whereFrom}'
                    and L2.arrivalAirportID = '{whereTo}'
                    and L1.arrivalAirportID = L2.departureAirportID"""

    query2staseis = f"""select L1.journeyID,L1.journeyDate,L1.departureAirportID as 'From',L1.departTime,L1.arrivalAirportID as 'Στάση 1',L1.arrivalTime as 's1ArrTime',L2.departTime as 's1DepTime',L2.arrivalAirportID as 'Στάση 2',L2.arrivalTime as 's2ArrTime', L3.departTime as 's2DepTime',L3.arrivalAirportID as 'To',L3.arrivalTime,cast(round(0.05*(L1.travelDistance + L2.travelDistance + L3.travelDistance)) as int) as 'cost'
                        FROM {viewName} as L1 left OUTER join {viewName} as L2 LEFT OUTER join {viewName} as L3
                        where L1.journeyID = L2.journeyID 
                        and L1.journeyID = L3.journeyID
                        and L1.departureAirportID ='{whereFrom}'
                        and L3.arrivalAirportID = '{whereTo}'
                        and L1.arrivalAirportID = L2.departureAirportID
                        AND L2.arrivalAirportID = L3.departureAirportID"""

    queryDropView = f"""DROP VIEW {viewName};"""
    

    if numberOfLegs == 1:
        legQueries = queryApeutheias
    elif numberOfLegs == 2:
        legQueries = queryApeutheias+'\n\nUNION\n\n'+query1stash
    elif numberOfLegs == 3:
        legQueries = queryApeutheias+'\n\nUNION\n\n'+query1stash+'\n\nUNION\n\n'+query2staseis

    totalQuery = f"""{createViewQuery} \nSELECT* FROM\n({legQueries})\nORDER by journeyDate; \n{queryDropView}"""

    if show:
        print(totalQuery,"\n\n\n")

    journeys = dbHandler.executeSQL(totalQuery)
    if not journeys:
        return False
    return journeys


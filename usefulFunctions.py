import datetime

def dayHasChanged(time1,time2):
        now = datetime.datetime.now()
        t1 = [int(i) for i in time1.split(":")]
        t2 = [int(i) for i in time2.split(":")]
        time1 = now.replace(hour = t1[0], minute = t1[1])
        time2 = now.replace(hour = t2[0], minute = t2[1])
        return time2 < time1

def format_date(date):
        d = date.split("/")
        d = [d[2],d[0],d[1]]
        if len(d[0]) == 2:
            d[0] = '20'+d[0]
        d[1] = str(int(d[1])//10) + str(int(d[1])%10)
        d[2] = str(int(d[2])//10) + str(int(d[2])%10)
        return "-".join(d)
    
def sqliteBetterDateFormat(date):
        return  datetime.datetime.strptime(date,'%Y-%m-%d' ).strftime("%d-%m-%Y")

def setNDaysLater(date,N):
        d = [int(i) for i in date.split("-")]
        newDate = datetime.datetime(d[0],d[1],d[2]) + datetime.timedelta(days = N)
        return format_date(str(newDate.month)+"/"+str(newDate.day)+"/"+str(newDate.year))

def timeInterval(t1,t2):
    mins = int(t2.split(':')[1]) - int(t1.split(':')[1])
    hours = int(t2.split(':')[0]) - int(t1.split(':')[0])
    
    if mins < 0:
        mins+=60
        hours-=1
        
    if hours<0:
        hours+=24

    return str(hours)+'.'+str(mins//10)+str(mins%10)
    


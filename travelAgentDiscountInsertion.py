import handleDataBase
import random

d = handleDataBase.DataModel("database.db")

agents = d.executeSQL("""select travelAgentVat from TravelAgent""")
L = len(agents) - 1

#print(agents)

N = int(input("Πόσες εγγραφές? "))
query = f"""select journeyID from journey order by random() limit({N})"""
for i in range(N):
    agent = agents[random.randint(0,L)]
    jQuery = f"""select journeyID
        from journey
        where journeyID not in
        (select journeyID
        from TravelAgentDiscount
        where travelAgentVAT = '{agent['travelAgentVAT']}'
        )order by random() limit({1})"""
    journey = d.executeSQL(jQuery)[0]
    disc = {"discount":[i/20 for i in range(2,9)][random.randint(0,6)]}
    print(agent)
    print(journey)
    print(disc)
    row = agent
    row.update(journey)
    row.update(disc)
    d._insertIntoTable('TravelAgentDiscount',row)
   

    

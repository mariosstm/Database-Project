import sqlite3
import time
class DataModel():
    
    def __init__(self, filename):
        self.filename = filename
        try:
            self.con = sqlite3.connect(filename)
            self.con.row_factory = sqlite3.Row  # ώστε να πάρουμε τα ονόματα των στηλών του πίνακα
            self.cursor = self.con.cursor()
            print("Successful Connection with Database:", filename)
            sqlite_select_Query = "select sqlite_version();"
            self.cursor.execute(sqlite_select_Query)
            record = self.cursor.fetchall()
            for rec in record:
                print("SQLite Database Version is: ", rec[0])
        except sqlite3.Error as error:
                print("Connection Error with sqlite DataBase ", error)
    
    def close(self):
        self.con.commit()
        self.con.close()
        print(f"Connection with {self.filename} Closed...\n")

    def insertRow(self, query):
        try:
            for statement in query.split(";"):
                self.cursor.execute(statement)
            self.con.commit()
            return True
        except sqlite3.Error as error:
            return False
    
    def executeSQL(self, query, show=False):
        dataList=[]
        try:
            for statement in query.split(";"):
                if statement.strip():
                    self.cursor.execute(statement)            
                for row in self.cursor.fetchall():
                    if show:
                        print(", ".join([str(item)for item in row]))
                    dataList.append(dict(row))
                
            self.con.commit()
            return dataList
        except sqlite3.Error as error:
            return False

    def readTable(self, table):
        try:
            query = f'''SELECT * FROM {table};'''
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            result = []
            for row in records:
                result.append(dict(row))
            return result
        except sqlite3.Error as error:
            return False
            #print(f"Error Loading Table: {table}", error)
    
    def _insertIntoTable(self, table, row_dict):
        
        try:
            query_param = f"""INSERT INTO {table} ({",".join(row_dict.keys())}) VALUES ({", ".join((len(row_dict)-1) * ["?"])}, ?);"""
            data = tuple(row_dict.values())
            self.cursor.execute(query_param, data)
            self.con.commit()
            print(data)
            return True
        except sqlite3.Error as error:
            #print(f"Insertion Error in Table: {table}", error)
            return False
    
    
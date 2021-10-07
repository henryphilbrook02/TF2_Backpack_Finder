
import pyodbc


class AccessDB:

    def __init__(self,  newPath):
        self.path = newPath
        self.conn = self.connect()
        self.cursor = self.conn.cursor()

    def connect(self):
         return pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:'+self.path+';')

    def close(self):
        self.conn.commit()
        self.conn.close()

               #this is a list of lists
    def insetInto(self, dataList, tableName):
        for i in dataList:
            if not self.isDup(i[0]):
                self.cursor.execute('''
                        INSERT INTO '''+tableName+''' (SID, TFWorth, Asked, URL)
                        VALUES
                        ('''+i[0]+''','''+i[1]+''',False,\''''+i[2]+'''\')
                        ''')
            self.conn.commit()

    def isDup(self, id):
        self.cursor.execute('''
                    SELECT URL 
                    FROM STable1
                    WHERE SID = \''''+id+'''\'
                    ''')
        return not (self.cursor.fetchall() == [])
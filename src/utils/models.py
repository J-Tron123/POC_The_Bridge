import pymysql

class DBController():
    def __init__(self, database_route):
        self.database_route = database_route

    def querySQL(self, query, parameters=[]):
        con = pymysql.connect(self.database_route)
        cur = con.cursor()
        cur.execute(query, parameters)

        keys = []
        for item in cur.description:
            keys.append(item[0])

        responses = []
        for response in cur.fetchall():
            ix_clave = 0
            d = {}
            for column in keys:
                d[column] = response[ix_clave]
                ix_clave += 1
            responses.append(d)

        con.close()
        return responses
    
    def changeSQL(self, query, parameters):
        con = pymysql.connect(self.database_route)
        cur = con.cursor()
        cur.execute(query, parameters) 
        con.commit()
        con.close()

import numpy as np, pymysql, pickle

choices = [(None, "---Select an option---"), (7, "Week"), (28, "February"), 
(29, "February in leap year"), (30, "30 days month"), (31, "31 days month")]

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

def predictions(period, route):
    model = pickle.load(open(route,'rb'))
    predicciones = model.predict(period)
    inversed_predicciones = np.expm1(predicciones)
    return np.round(inversed_predicciones, 0)

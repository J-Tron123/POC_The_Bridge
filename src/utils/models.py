import numpy as np, pandas as pd, pymysql, pickle
from pmdarima.arima import auto_arima
from sklearn.metrics import mean_absolute_percentage_error


choices = [(None, "---Selecciona una opción---"), (7, "Semana"), (30, "Mes de 30 días"), 
(31, "Mes de 31 días"), (28, "Mes de 28 días"), (29, "Mes de 29 días")]

def predictions(period, route):

    period = int(period)

    if period in [7,28,29,30,31]:
        model = pickle.load(open(route, "rb"))
        predicciones = model.predict(period)
        inversed_predicciones = np.expm1(predicciones)
        print(model)
        return np.round(inversed_predicciones, 0)
        
    else:
        return ("Debes ingresar la cantidad de días que tiene un mes o una semana") 


def modification_data(data):
    """Modificar dataFrame ingresado, agregar columnas de day, month, year, cambiar Formato columna Date
    
    Argumentos:
        - df (DataFrame) : DataFrame a tranformar
        
    Retorno:
        - df (DataFrame)
    """
    data = pd.read_csv(data)

    data[["day", "month", "year"]] = data["Date"].str.split("/", expand=True)
    data["year"] = data["year"].astype(int)
    data["month"] = data["month"].astype(int)
    data["day"] = data["day"].astype(int)
    data["Date"] = pd.to_datetime(data[["day", "month", "year"]]).astype(str)
    print(data)
    return data  


def create_db_csv(data, host, password, user):
    """Crear base da datos, e ingresar los registros del DataFrame a la base de datos creada
    
    Argumentos:
        - df (DataFrame) : DataFrame a tranformar
        
    Retorno:
        -  (string)
    """
    
    connection = pymysql.connect(host=host, password=password, user=user, cursorclass = pymysql.cursors.DictCursor)
    crsr = connection.cursor()
    use_db = """USE DB_POC"""
    create_table = """CREATE TABLE USERS (Date VARCHAR(12), Users int(5), day int(2), month int(2), year int(4));
    """
    eliminate_table = """DROP TABLE USERS;"""
    try:
        crsr.execute(use_db)        
        crsr.execute(create_table)
    except pymysql.Error as e:
        print(e)
        crsr.execute(use_db)        
        crsr.execute(eliminate_table)
        crsr.execute(create_table)
        
    for index, row in data.iterrows():
        crsr.execute(use_db)
        crsr.execute(f"""INSERT INTO USERS (Date, Users, day, month, year) values({row.Date}, {row.Users}, {row.day}, {row.month}, {row.year})""")
    
    connection.commit()
    connection.close()
    return "Base de Datos Creada"

def modelo_entrenar(route_model, host, password, user):
    """Entrenar model, modelo Autoarima
            
    Retorno:
        -  (string)
    """
    connection = pymysql.connect(host=host, password=password, user=user, cursorclass = pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    use_db = """USE DB_POC"""
    data = """SELECT * FROM USERS""" #query
    cursor.execute(use_db)
    cursor.execute(data)
    result = cursor.fetchall()
    print(result)
    names = [description[0] for description in cursor.description]
    connection.close()
    df = pd.DataFrame(result,columns=names)
    df["Users"] = np.log1p(df["Users"])
    train = df[["Users"]][:-30]
    test = df[["Users"]][-30:]
    
    model = auto_arima(
    train,
    start_p=1,
    start_q=1,
    max_d=3,
    max_p=5,
    max_q=5,
    stationary=False,
    trace=True,
    random_state=42,
    n_jobs=-1,
    n_fits=50
    )
    
    predicciones = model.predict(len(test))
    print("MAPE:", mean_absolute_percentage_error(test.values, predicciones))
    pickle.dump(model, open(route_model, "wb"))
    return "Modelo Entrenado"

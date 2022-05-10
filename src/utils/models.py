import numpy as np, pandas as pd, sqlite3, pickle
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
    return data  


def create_db_csv(data, route):
    """Crear base da datos, e ingresar los registros del DataFrame a la base de datos creada
    
    Argumentos:
        - df (DataFrame) : DataFrame a tranformar
        
    Retorno:
        -  (string)
    """
    
    connection = sqlite3.connect(route)
    crsr = connection.cursor()
    
    create_table = """
    CREATE TABLE USERS (
    Date DATE,
    Users int(5),
    day int(5),
    month int(5),
    year int(5)
    );
    """
    eliminate_table = """
        DROP TABLE USERS;
        """
    try:        
        crsr.execute(create_table)
    except:        
        crsr.execute(eliminate_table)
        crsr.execute(create_table)
        
    for index, row in data.iterrows():
        crsr.execute("""INSERT INTO USERS (Date, Users, day, month, year) values(?,?,?,?,?)""", (row.Date, row.Users, row.day, row.month, row.year))
    
    connection.commit()
    connection.close()
    return "Base de Datos Creada"

def modelo_entrenar(route_data_base, route_model):
    """Entrenar model, modelo Autoarima
            
    Retorno:
        -  (string)
    """
    connection = sqlite3.connect(route_data_base)
    cursor = connection.cursor()
    data = "SELECT * FROM USERS" #query
    result = cursor.execute(data).fetchall()
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

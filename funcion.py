### Actualización de datos
#######################################################
# El programa debe solicitar al usuario el valor de un ticker, una fecha de inicio y una fecha de fin. Debe luego pedir los valores a la API y guardar estos datos en una base de datos SQL.

import requests
import json
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
import datetime



class bcolors:
    OK = '\033[92m' #VERDE
    ATENCION = '\033[93m' #AMARILLO
    ERROR = '\033[91m' #ROJO
    RESET = '\033[0m' #RESET COLOR
    
#################################################


####################################################################################################################################################################################
def crea_tabla():


    # Creamos una conexión con la base de datos
    con = sqlite3.connect('trabajo_final.db')

    # Creamos el curso para interactuar con los datos
    cursor = con.cursor()
    
    
    # Creo tabla primaria
    cursor.execute(f''' 
    CREATE TABLE IF NOT EXISTS primaria (
    fechas_id INTEGER PRIMARY KEY, 
    fecha_inicio DATE NOT NULL, 
    fecha_fin DATE NOT NULL, 
    ticker TEXT,
    results TEXT,
    status TEXT);
    ''')
    
    # Cerramos la conexión
    con.close()

    
####################################################################################################################################################################################




####################################################################################################################################################################################

def actualizacion():
    try:
           
        ## SE PIDEN LOS DATOS AL USUARIO ##########
        ticker = input("Ingrese ticker a pedir: "+ bcolors.OK)
        
        fecha_inicio = input(bcolors.ATENCION + "Ingrese fecha de inicio (Año-Mes-Dia): "+ bcolors.OK)
        fecha_fin = input(bcolors.ATENCION + "Ingrese fecha de fin (Año-Mes-Dia): "+ bcolors.OK)
        
        

        print(bcolors.ATENCION + "Pidiendo Datos...")
        
        chequeo_conexion()
        
        url_datos = (f'  https://api.twelvedata.com/time_series?&start_date={fecha_inicio}1&end_date={fecha_fin}&symbol={ticker}&interval=1day&apikey=98cd6f018e164b9c8b88976dfd3e746f')

        global data



        response = requests.get(url_datos)
        data = response.json()

        r=data

        meta = data['meta']
        results = data['values']
        status = data['status']

        ticker = meta['symbol']
        print(status)


        #### SE CREA LA TABLA SI NO EXISTE ######
        crea_tabla()

        #####


        con = sqlite3.connect('trabajo_final.db')

        # Creamos el curso para interactuar con los datos
        cursor = con.cursor()


        # Agrego los datos a la base SQL
        cursor.execute(f'''INSERT INTO 'primaria' (fecha_inicio, fecha_fin, ticker, results, status)   VALUES ("{fecha_inicio}", "{fecha_fin}", "{ticker}", "{data['values']}", "{data['status']}") ;
        ''')
        con.commit()



        global resumen_ticker
        resumen_ticker = (f' - Se actualizo el Ticker: {ticker}\n - Con Fecha de Inicio: {fecha_inicio}\n - Fecha de Fin: {fecha_fin}')


        ###### Datos guardados correctamente ############
        
        print(bcolors.OK +"Datos guardados correctamente")

        print("")

        print(resumen_ticker)
        print("")




        ###################    GUARDO INFO DESCARGADA EN DATA FRAME ###################################
  


        data = r['values']

        df= pd.DataFrame.from_dict(data)
        df=df.assign(Ticker=ticker)
        df


        df2 = pd.DataFrame(df, columns= ['datetime','open','high','low','close','volume','Ticker'])

        con = sqlite3.connect('trabajo_final.db')

        cursor = con.cursor()


        cursor.execute('CREATE TABLE IF NOT EXISTS secundaria ([id] INTEGER PRIMARY KEY, datetime DATE NOT NULL, [open] REAL, [high] REAL, [low] REAL, [close] REAL, [volume] REAL, [Ticker] TEXT)');


        df2 = pd.DataFrame(df,   columns= ['datetime','open','high','low','close','volume','Ticker'])
        df2.to_sql('secundaria', con,  if_exists='append', index = False)

        con.commit()

        con.close()
    
    except:
        print(bcolors.ERROR +"Hubo un error, vuelva a intentar.... procure ingresar los datos en mayúsculas y respetando los parámetros de ingreso.")

###################################################################################################################################################################################



###################################################################################################################################################################################
def detalle():
    
    try:

        ####### SE MUESTRAN TODOS LOS TICKERS GUARDADOS ##############################
        con = sqlite3.connect('trabajo_final.db')
        cursor = con.cursor()

        consulta_resumen = f' SELECT * from secundaria'

        #resultado de la consulta a data frame
        df= pd.read_sql_query(consulta_resumen, con)
        result= df.groupby("Ticker")["datetime"].aggregate(['min', 'max'])
        result= result.rename(columns={'min':'Desde','max':'Hasta'})

        print(bcolors.OK + "Los tickers guardados en la base de datos son:")
        print(result)

        #cierre conexión
        con.close()

    except:
        print(bcolors.ERROR +"Hubo un error, vuelva a intentar.... al parecer la base de datos no se encuentra disponible. Consulte al programador")
    
    
####################################################################################################################################################################################





####################################################################################################################################################################################
def grafico():
    
    try:
        
        ####### Pedimos al usuario ingresar el ticker a graficar, luego se conecta con la base de datos y se seleccionan todos
        ####### los ticker elegidos con sus fechas de inicio, fin y resultados. Todo se ordena por fecha de inicio.
   

        con = sqlite3.connect('trabajo_final.db')
        cursor = con.cursor()

        ticker_grafico = input("Ingrese Ticker a graficar:")

        consulta = f' SELECT * from secundaria WHERE Ticker= ("{ticker_grafico}") ORDER BY datetime'

        #resultado de la consulta a data frame
        df= pd.read_sql_query(consulta, con)

        #verifica el resultado de la consulta SQL
        print(df.head())



        df.index = pd.DatetimeIndex(df['datetime'])

        titulo = f' Evolución de {ticker_grafico}'

        mpf.plot(df, type='candle',
                title= titulo,
                ylabel='Price ($)')



        #resultado de la consulta a data frame
        df= pd.read_sql_query(consulta, con)

        min_periodo = df['datetime'].min()
        max_periodo = df['datetime'].max()

        print("Estadisticas descriptivas para", ticker_grafico, "desde",min_periodo,"hasta", max_periodo, "\n")
        print(df.describe().round(2))

        casos = df['datetime'].count()
        min_low= df['low'].min()
        max_high= df['high'].max()
        mean_open= df['open'].mean()
        mean_close= df['close'].mean()

        print("\n Cantidad de dias analizados en el periodo:",casos)
        print("\n Precio medio de apertura en el periodo: $", mean_open)
        print("\n Precio medio de cierre en el periodo: $", mean_close)
        print("\n Precio maximo en el periodo: $", max_high)
        print("\n Precio minimo en el periodo: $", min_low)

        #cierre conexión
        con.close()
        
    except:
        print(bcolors.ERROR +"Hubo un error, vuelva a intentar.... es probable que el Ticker que ingreso no exita en la base de datos o haya ingresado en minuscula.")


###############################################################################################################################################################################




###############################################################################################################################################################################
def documentacion():
    import webbrowser
    path = 'documentacion.pdf'
    webbrowser.open_new(path)


#################################################################################################################################################################################




########### Chequea la conexion a internet, haciendo un request a la api ########################################################################################################

def chequeo_conexion():
    try:
        request_api = requests.get("https://api.twelvedata.com/time_series?&start_date={fecha_inicio}1&end_date={fecha_fin}&symbol={ticker}&interval=1day&apikey=98cd6f018e164b9c8b88976dfd3e746f", timeout=5)
    except (requests.ConnectionError, requests_api.Timeout):
        print("Sin conexión a internet.")
    else:
        print("Conexión a internet exitosa.")
##################################################################################################################################################################################
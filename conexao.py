from ast import expr_context
from msilib.schema import Error
import mysql.connector

def conexao():
    try:
        con = mysql.connector.connect(host='burcas.ddns.net',user='lucas',password='12lucas12',database ='lanchonete')
        print("conexao")
        
    except Error as err:
        print(err)

conexao()
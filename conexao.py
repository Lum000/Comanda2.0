from ast import expr_context
from msilib.schema import Error
import mysql.connector
import Principal
con = 0
def conexao():
    global con
    try:
        con = mysql.connector.connect(host='burcas.ddns.net',user='lucas',password='12lucas12',database='lanchonete')
        if con.is_connected():
            None
    except Error as err:
        print(err)
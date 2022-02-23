from ast import Pass
from asyncio.windows_events import NULL
from http.client import OK
from random import sample
from telnetlib import ENCRYPT
from tokenize import Ignore
from PyQt5.QtGui import * 
from msilib.schema import Error
from cryptography.fernet import Fernet
from PyQt5 import uic,QtWidgets
from time import sleep
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
from PyQt5 import QtCore
import base64
from numpy import byte
from conexao import conexao
from PyQt5.QtWidgets import *
from conexao import con

app=QtWidgets.QApplication([])
login = uic.loadUi("uic/Login.ui")
inicio = uic.loadUi("uic/bemvindo.ui")
addmesa = uic.loadUi("uic/addmesas.ui")
logo = QPixmap("icones/logo.png")
bancoerro = QPixmap("icones/banco")
registro = uic.loadUi("uic/registra.ui")
login.label.setPixmap(logo)
registro.label.setPixmap(logo)
inicio.label.setPixmap(logo)



#globais
erro = 0
saveuserr = True
abremesa = 0
buttonStyle = """QPushButton{background-color: rgb(198, 198, 198);border: 2px solid rgb(248, 207, 2);border-radius:15px;color: rgb(0, 0, 0)}QPushButton:hover{border: 2px solid rgb(255, 255, 0);background-color: rgb(227, 227, 227)}QPushButton:pressed{background-color: rgb(255, 255, 255);border: 5px solid rgb(248, 207, 2);}"""
estilovermelho = """QLineEdit{border:2px solid rgb(255,0,0);border-radius:15px}
        QLineEdit:hover{border:4px solid rgb(255,0,0);border-radius:15px}"""
estilonormal = """QLineEdit{color:rgb(141, 141, 141);border:2px solid rgb(255, 212, 0);border-radius:20px}
QLineEdit:hover{border:3px solid rgb(220, 180, 0)}"""
linha = 0

### SALVA NO CAMPO O USUARIO
def saveuser():
    global saveuserr
    check = login.checkBox.isChecked()
    saveuserr = check
    if check == True:
        saveuserr = True
    else:
        saveuserr = False
### STARTA O PROGRAMA
def abretelalogin():
    global erro
    global saveuserr
    login.show()
    print(saveuserr)
    try:
        from conexao import conexao
        conexao()
        from conexao import con
    except:
        login.label_2.setPixmap(bancoerro)
        erro = 1
    cur = con.cursor()
    cur.execute("SELECT nome FROM saveuser")
    dado = cur.fetchall()
    if str(dado) == '[]':
        None
    else:
        login.lineEdit.setText(str(dado[0][0]))
    

##registro
def abreregistro():
    login.close()
    registro.show()
senha = ''
def registra():

    #CONEXAO COM OS BANCO DE DADOS
    from conexao import con
    user = registro.user.text()
    password = registro.password.text()
    email = registro.email.text()
    c_password = registro.c_password.text()
    cur = con.cursor()
    is_null = 0
    if str(user) == '' and str(email) == '':
        is_null = 3
    elif str(user) == '':
        is_null = 2
    elif str(email) == '':
        is_null = 1
    else:
        is_null == 0
    if c_password == password and is_null == 0:
        comando = "INSERT INTO usuarios (user,password,email) VALUES (%s,%s,%s)"
        senha_bytes = password.encode("ascii")
        senha_string = base64.b64encode(senha_bytes)
        dados = (user,senha_string,email)
        cur.execute(comando,dados)
        con.commit()
        QMessageBox.about(registro,'CORRETO','REGISTRO EFETUADO COM SUCESSO')
        login.show()
        registro.close()
    elif is_null == 1:
        registro.email.setStyleSheet(estilovermelho)
        registro.label_3.setText("EMAIL NÃO PODE ESTAR EM BRANCO")
        registro.user.setStyleSheet(estilonormal)
        registro.password.setStyleSheet(estilonormal)
        registro.c_password.setStyleSheet(estilonormal)
    elif is_null == 2:
        registro.user.setStyleSheet(estilovermelho)
        registro.label_3.setText("USUARIO NÃO PODE ESTAR EM BRANCO")
        registro.email.setStyleSheet(estilonormal)
        registro.password.setStyleSheet(estilonormal)
        registro.c_password.setStyleSheet(estilonormal)
    elif is_null == 3:
        registro.user.setStyleSheet(estilovermelho)
        registro.email.setStyleSheet(estilovermelho)
        registro.password.setStyleSheet(estilovermelho)
        registro.c_password.setStyleSheet(estilovermelho)
        registro.label_3.setText("CONFIRME OS DADOS")
    else:
        registro.label_3.setText("SENHAS NÃO CONFEREM")
        registro.password.setStyleSheet(estilovermelho)
        registro.c_password.setStyleSheet(estilovermelho)
        registro.email.setStyleSheet(estilonormal)
        registro.user.setStyleSheet(estilonormal)
        registro.label_3.setStyleSheet('color:rgb(255,0,0)')

    ## REGISTRO ALTERAÇOES VISUAIS
#VALIDA O LOGIN
def validalogin():
    global erro
    global saveuserr
    from conexao import con
    if erro == 1:
        QMessageBox.about(login,'login','SEM CONEXÃO COM BANCO DE DADOS !')
    else:
        cur = con.cursor()
        username = login.lineEdit.text()
        cur.execute("SELECT password FROM usuarios WHERE user = '{}'".format(str(username)))
        user = cur.fetchall()
        if str(user) == '[]':
            login.label_3.setText('  USUARIO NÃO EXISTE  ')
            login.label_3.setStyleSheet('QLabel{color:rgb(255,0,0);border:2px solid rgb(255,0,0); border-radius:10px}')
        else:
            cur.execute("SELECT nome FROM saveuser WHERE nome ='{}'".format(username))
            dado = cur.fetchall()
            if str(dado) == '[]' and saveuserr == True:
                cur.execute("INSERT INTO saveuser (nome) VALUES ('{}')".format(username))
                con.commit()
            elif str(dado) != '[]' and saveuserr == True:
                pass
            elif str(dado) != '[]' and saveuserr == False:
                cur.execute("DELETE FROM saveuser WHERE nome='{}'".format(username))
                login.lineEdit.setText('')
                con.commit()
            else:
                None
            senha_banco = user[0][0]
            senha_banco_bytes = senha_banco.encode("ascii")
            base64_string = base64.b64decode(senha_banco_bytes)
            sample_string_bytes = base64.b64decode(senha_banco_bytes)
            sample_string = sample_string_bytes.decode("ascii")
            password = login.lineEdit_2.text()
            if sample_string == password:
                login.close()
                inicio.show()
            else:
                login.label_3.setText("VERIFIQUE OS DADOS")
#ALTERA VISIBILIDADE DA SENHA
def olhosenha():
    registro.olhosenha.setCheckable(True)
    if registro.olhosenha.isChecked():
        registro.password.setEchoMode(registro.password.Password)
        registro.c_password.setEchoMode(registro.password.Password)
        registro.olhosenha.setIcon(QIcon(QPixmap('icones/fechado.png')))
    else:
        registro.password.setEchoMode(registro.password.Normal)
        registro.c_password.setEchoMode(registro.password.Normal)
        registro.olhosenha.setIcon(QIcon(QPixmap('icones/aberto.png')))

def abremesas():
    global linha
    from conexao import con
    cur = con.cursor()
    cur.execute("USE mesas")
    cur.execute("SELECT * FROM mesas")
    dado = cur.fetchall() 
    inicio.tableWidget.setRowCount(len(dado))
    inicio.tableWidget.setColumnCount(4)
    inicio.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
    for i in range(0, len(dado)):
        linhas = int(len(dado))
        for j in range(0, 4):
            inicio.tableWidget.setHorizontalHeaderLabels(["ID", "NOME", 'NUMERO', 'TOTAL COMANDA'])
            inicio.tableWidget.setColumnWidth(0, 0)
            inicio.tableWidget.setColumnWidth(1, 320)
            inicio.tableWidget.setColumnWidth(2, 320)
            inicio.tableWidget.setColumnWidth(3, 320)
            inicio.tableWidget.setAlternatingRowColors(True)
            inicio.tableWidget.setFont(QtGui.QFont('Bold',23))
            inicio.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dado[i][j])))
    linha = inicio.tableWidget.currentRow()

### MESAS
def abreaddmesas():
    addmesa.show()
    addmesa.frame_4.setStyleSheet("border-image: url(Backgrounds/backlogo.jpg)")


def addmesas():
    from conexao import con
    cur = con.cursor()
    cur.execute("USE mesas")
    com = ("INSERT INTO mesas(nome,numero) VALUES (%s,%s)")
    dados = (addmesa.nome.text(), addmesa.numero.text())
    cur.execute(com,dados)
    con.commit()
    QMessageBox.about(addmesa,'confirmado','Mesa Adicionada Com Sucesso !!')
    addmesa.close()
    abremesas()


def delmesa():
    linha = inicio.tableWidget.currentRow()
    from conexao import con
    if linha == -1:
        msgbox = QMessageBox()
        msgbox.setText("MESA NÃO SELECIONADA")
        msgbox.setWindowTitle("ERRO")
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.setStyleSheet("""color:red; font-size: 20pt; background-color:rgb(62, 62, 62)""")
        msgbox.button(QMessageBox.Ok).setStyleSheet("""QPushButton{background-color: rgb(198, 198, 198);border: 2px solid rgb(248, 207, 2);border-radius:15px;color: rgb(0, 0, 0)}QPushButton:hover{border: 2px solid rgb(255, 255, 0);background-color: rgb(227, 227, 227)}QPushButton:pressed{background-color: rgb(255, 255, 255);border: 5px solid rgb(248, 207, 2);}""")
        msgbox.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        msgbox.exec()
    else:
        cur = con.cursor()
        cur.execute("SELECT id FROM mesas")
        dado = cur.fetchall()
        if str(dado) != '[]':
            cur.execute("SELECT nome FROM mesas WHERE id={}".format(dado[linha][0]))
            nome = cur.fetchall()
            msgbox = QMessageBox()
            msgbox.setText("TEM CERTEZA QUE DESEJA EXCLUIR A MESA =  {}".format(nome[0][0]))
            msgbox.setWindowTitle("ERRO")
            msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgbox.setStyleSheet("""color:red; font-size: 20pt; background-color:rgb(62, 62, 62)""")
            msgbox.button(QMessageBox.Yes).setStyleSheet(buttonStyle)
            msgbox.button(QMessageBox.No).setStyleSheet(buttonStyle)
            msgbox.button(QMessageBox.No).setText("NÃO")
            msgbox.button(QMessageBox.Yes).setText("SIM")
            msgbox.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            returnValue = msgbox.exec()

            if returnValue == QMessageBox.Yes:
                vid = dado[linha][0]
                cur.execute("DELETE FROM mesas WHERE id={}".format(vid))
                con.commit()
                abremesas()
            else:
                abremesas()

    
abretelalogin()


#LOGIN
login.pushButton.clicked.connect(validalogin)
login.pushButton_2.clicked.connect(abreregistro)
login.checkBox.stateChanged.connect(saveuser)

#REGISTROS
registro.pushButton_2.clicked.connect(registra)
registro.olhosenha.clicked.connect(olhosenha)
registro.password.setEchoMode(registro.password.Password)
registro.c_password.setEchoMode(registro.password.Password)
registro.olhosenha.setIcon(QIcon(QPixmap('icones/fechado.png')))

##ADDMESAS
addmesa.adicionar.clicked.connect(addmesas)


##INICIOS
inicio.mesas.clicked.connect(abremesas)
inicio.adicionar.clicked.connect(abreaddmesas)
inicio.excluir.clicked.connect(delmesa)




app.exec()
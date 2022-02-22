from ast import Pass
from asyncio.windows_events import NULL
import encodings
from random import sample
from telnetlib import ENCRYPT
from PyQt5.QtGui import * 
from msilib.schema import Error
from cryptography.fernet import Fernet
from PyQt5 import uic,QtWidgets
from time import sleep
from PyQt5.QtGui import QPixmap
import base64
from numpy import byte
from conexao import conexao
from PyQt5.QtWidgets import *

app=QtWidgets.QApplication([])
login = uic.loadUi("uic/Login.ui")
inicio = uic.loadUi("uic/bemvindo.ui")
logo = QPixmap("icones/logo.png")
bancoerro = QPixmap("icones/banco")
registro = uic.loadUi("uic/registra.ui")
login.label.setPixmap(logo)
registro.label.setPixmap(logo)
inicio.label.setPixmap(logo)



#globais

erro = 0
saveuserr = False
estilovermelho = """QLineEdit{border:2px solid rgb(255,0,0);border-radius:15px}
        QLineEdit:hover{border:4px solid rgb(255,0,0);border-radius:15px}"""
estilonormal = """QLineEdit{color:rgb(141, 141, 141);border:2px solid rgb(255, 212, 0);border-radius:20px}
QLineEdit:hover{border:3px solid rgb(220, 180, 0)}"""

def abretelalogin():
    global erro
    login.show()
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
        login.checkBox.setChecked(True)

def validalogin():
    global erro
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
            senha_banco = user[0][0]
            password = login.lineEdit_2.text()
            if senha_banco == password:
                login.close()
                inicio.show()
            else:
                login.label_3.setText("VERIFIQUE OS DADOS")


def abreregistro():
    login.close()
    registro.show()
senha = ''
def registra():

    #CONEXAO COM OS BANCO DE DADOS
    from conexao import con
    global key
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


def saveuser():
    global saveuserr
    check = login.checkBox.isChecked()
    if check == True:
        saveuserr = True
    else:
        saveuserr = False

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
            if saveuserr == True:
                cur.execute("INSERT INTO saveuser (nome) VALUES ('{}')".format(username))
                con.commit()
            else:
                Pass
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

abretelalogin()

login.pushButton.clicked.connect(validalogin)
login.pushButton_2.clicked.connect(abreregistro)
registro.pushButton_2.clicked.connect(registra)
registro.olhosenha.clicked.connect(olhosenha)
registro.password.setEchoMode(registro.password.Password)
registro.c_password.setEchoMode(registro.password.Password)
login.checkBox.stateChanged.connect(saveuser)
registro.olhosenha.setIcon(QIcon(QPixmap('icones/fechado.png')))
app.exec()
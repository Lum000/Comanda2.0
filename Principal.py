from ast import Pass
from asyncio.windows_events import NULL
from http.client import OK
from random import sample
from telnetlib import ENCRYPT
from tkinter import messagebox
from tokenize import Ignore
from turtle import onclick
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
comanda = uic.loadUi("uic/comandas.ui")
login.label.setPixmap(logo)
registro.label.setPixmap(logo)
inicio.label.setPixmap(logo)
adproduto = uic.loadUi("uic/addproduto.ui")
adestoque = uic.loadUi("uic/estoquead.ui" )


#--------------------------------------------------------------------------
#globais
erro = 0
saveuserr = True
abremesa = 0
nome_nome = 0
buttonStyle = """QPushButton{background-color: rgb(198, 198, 198);border: 2px solid rgb(248, 207, 2);border-radius:15px;color: rgb(0, 0, 0)}QPushButton:hover{border: 2px solid rgb(255, 255, 0);background-color: rgb(227, 227, 227)}QPushButton:pressed{background-color: rgb(255, 255, 255);border: 5px solid rgb(248, 207, 2);}"""
estilovermelho = """QLineEdit{border:2px solid rgb(255,0,0);border-radius:15px}
        QLineEdit:hover{border:4px solid rgb(255,0,0);border-radius:15px}"""
estilonormal = """QLineEdit{color:rgb(141, 141, 141);border:2px solid rgb(255, 212, 0);border-radius:20px}
QLineEdit:hover{border:3px solid rgb(220, 180, 0)}"""
styletable = """QTableWidget{gridline-color: rgb(0, 0, 0);;font-size: 22pt;border:2px;border-image: url(Backgrounds/Back.jpg);}QHeaderView::section {background-color: rgb(62, 62, 62);padding: 4px;border:2px solid rgb(248, 207, 2);color:rgb(255, 255, 255);font: 75 12pt "MS Shell Dlg 2";}QHeaderView::section:horizontal{border-top: 2px solid rgb(248, 207, 2);font-size: 22pt;}QHeaderView::section:vertical{border-left: 2px solid rgb(248, 207, 2);	border-bottom:0px;font-size: 20pt}"""
styleButton = """QPushButton{background-color: rgba(170, 255, 255, 100);font: 12pt Arial,bold;border:2px solid black;border-radius:15px}QPushButton:hover{background-color: rgba(170, 255, 255, 200);border:3px solid black}"""
linha = 0


#--------------------------------------------------------------------------
### SALVA NO CAMPO O USUARIO
def saveuser():
    global saveuserr
    check = login.checkBox.isChecked()
    saveuserr = check
    if check == True:
        saveuserr = True
    else:
        saveuserr = False



#--------------------------------------------------------------------------
### STARTA O PROGRAMA
def abretelalogin():
    global erro
    global saveuserr
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
    
#--------------------------------------------------------------------------
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


#--------------------------------------------------------------------------
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
        elif str(user) != '[]' and str(login.lineEdit_2.text()) == '[]':
            login.label_3.setText("VERIFIQUE SEUS DADOS")
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
#--------------------------------------------------------------------------
#ABRE AS COMANDAS

def abrecomanda(nomee):
    global nome_nome
    nome_nome = nomee
    from conexao import con
    comanda.lineEdit.setText('')
    comanda.show()
    comanda.tableWidget.setColumnWidth(0, 0)
    comanda.tableWidget.setColumnWidth(1, 325)
    comanda.tableWidget.setColumnWidth(2, 325)
    comanda.tableWidget.setColumnWidth(3, 300)
    comanda.adicionar.setIcon(QtGui.QIcon('icones/adicionar.png'))
    comanda.adicionar.setStyleSheet("""QPushButton{border:2px solid rgb(197, 174, 60);}QPushButton:hover{border:3px solid rgba(85, 255,20, 255);background-color: rgba(85, 255, 0, 100);}""")
    cur = con.cursor()
    cur.execute("USE {}".format(nomee))
    cur.execute("SELECT * FROM produtos")
    comanda.tableWidget.setColumnCount(4)
    resul = cur.fetchall()
    comanda.tableWidget.setRowCount(len(resul))
    for i in range(0,len(resul)):
        for j in range(0, 4):
            comanda.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(resul[i][j])))
    comanda.mesa.setText(nomee)
    comanda.mesa.setStyleSheet("QLabel{color: rgb(0, 4, 255) }")
    comanda.frame.setStyleSheet('QFrame{border-image: url("Backgrounds/975.jpg")}')


#--------------------------------------------------------------------------
#ADICIONA NAS COMANDAS

def addprodutoa(ola):
    print(ola)

def abreaddproduto():
    from conexao import con
    cur = con.cursor()
    cur.execute("USE lanchonete")
    cur.execute("SELECT * FROM produtos")
    dado = cur.fetchall()
    adproduto.show()
    adproduto.frame.setStyleSheet("QFrame{border-image: url(Backgrounds/975.jpg)}")
    adproduto.tableWidget.setRowCount(len(dado))
    adproduto.tableWidget.setColumnCount(3)
    adproduto.tableWidget.setColumnWidth(0,0)
    adproduto.tableWidget.setColumnWidth(1,392)
    adproduto.tableWidget.setColumnWidth(2,392)
    for i in range(0, len(dado)):
        for j in range(0,3):
            adproduto.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dado[i][j])))
    adproduto.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

def addproduto():
    from conexao import con
    linha = adproduto.tableWidget.currentRow()
    cur = con.cursor()
    cur.execute("SELECT id FROM produtos")
    resultdado = cur.fetchall()
    cur.execute("SELECT * FROM produtos WHERE id={}".format(resultdado[linha][0]))
    resultado = cur.fetchall()

    



#--------------------------------------------------------------------------
#ADICIONA NO ESTOQUE

def abreaddestoque():
    adestoque.show()
    adestoque.setStyleSheet("""#MainWindow {
        background-image: url(Backgrounds/lanchonete.jpg);
        background-repeat: no-repeat;
        background-position: center;
    }""")
    adestoque.frame_4.setStyleSheet("""QFrame{border-image: url(Backgrounds/backlogo.jpg)}""")


def addestoque():
    from conexao import con
    cur = con.cursor()
    cur.execute("USE lanchonete")
    cur.execute("CREATE TABLE IF NOT EXISTS produtos(id INT PRIMARY KEY AUTO_INCREMENT,produto VARCHAR(32),preco DOUBLE)")
    con.commit()
    produto = adestoque.produto.text()
    preco = adestoque.preco.text()
    if produto == '' and preco == '':
        adestoque.erro.setText("COMPLETE OS CAMPOS !!!")
    elif produto == "":
        adestoque.erro.setText("DIGITE O PRODUTO !!")
    else:
        try:
            if preco == '':
                adestoque.erro.setText("DIGITE O PREÇO !!!")
            else:
                preco_ve = int(preco)
                com = "INSERT INTO produtos (produto,preco) VALUES (%s,%s)"
                vari = (produto,preco)
                cur.execute(com,vari)
                con.commit()
                QMessageBox.about(adproduto,'EXITO !',"PRODUTO ADICIONADO COM SUCESSO !!!")
                adestoque.close()
        except:
            adestoque.erro.setText("PREÇO NÃO É NUMERO !!")












#--------------------------------------------------------------------------
#ABRE AS MESAS


def abremesas():
    global linha
    global nome_nome
    from conexao import con
    cur = con.cursor()
    cur.execute("USE mesas")
    cur.execute("SELECT * FROM mesas")
    dado = cur.fetchall() 
    btnn = -1 
    distancia = 100
    size = 150
    linha = 0
    nome_n = -1
    numero = -1
    cur.execute("SELECT nome FROM mesas")
    nome = cur.fetchall()
    for i in range(0, len(dado)):
        nome_n += 1
        numero += 1
        if str(nome) != '[]':
            nomee = nome[nome_n][0]
            size -= 5
            btnn += 1
            button = QPushButton('Button {}'.format(nomee), inicio.frame_2)
            button.setMaximumSize(size,70)
            button.setBaseSize(200, 70)
            button.setMinimumSize(110,70)
            button.move(100, 70)
            button.setStyleSheet(styleButton)
            linha += 1
            button.setText("{}".format(nomee.upper()))
            button.show()
            button.clicked.connect(lambda ch, nomee=nomee: abrecomanda(nomee))
            if numero < 4:
                for x in range(numero, linha):
                    button.move(distancia, 70)
                    distancia = distancia + 170
            elif numero == 4:
                distanciab = 100
                button.move(distanciab,150)
            elif numero > 4:
                for y in range(numero, linha):
                    distanciab += 170
                    button.move(distanciab,150)
        else:
            QMessageBox.about(inicio,'ERRO','SEM MESAS DISPONIVEIS')


#--------------------------------------------------------------------------
### MESAS
def abreaddmesas():
    addmesa.show()
    addmesa.nome.setText('')
    addmesa.numero.setText('')
    addmesa.frame_4.setStyleSheet("border-image: url(Backgrounds/backlogo.jpg)")


def addmesas():
    from conexao import con
    import mysql.connector
    global nome_nome
    nomee = addmesa.nome.text()
    cur = con.cursor()
    try:
        cur.execute("USE mesas")
        com = ("INSERT INTO mesas(nome,numero) VALUES (%s,%s)")
        dados = (nomee,addmesa.numero.text())
        cur.execute(com,dados)
        con.commit()
        cur.execute("CREATE DATABASE IF NOT EXISTS {}".format(nomee))
        con.commit()
        cur.execute("USE {}".format(nomee))
        cur.execute("CREATE TABLE IF NOT EXISTS produtos ( id INT NOT NULL AUTO_INCREMENT , produto VARCHAR(50) NOT NULL ,quantidade INT, preco DOUBLE NOT NULL, TOTAL INT , PRIMARY KEY (id)) ENGINE = InnoDB")
        con.commit()
        QMessageBox.about(addmesa,'confirmado','Mesa Adicionada Com Sucesso !!')
        addmesa.close()
        abremesas()
    except mysql.connector.Error as err:
        QMessageBox.about(addmesa,'ERRO','ERRO AO ADICIONAR A MESA {} !!!!'.format(err))
    


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

def abreavulsos():
    None

#--------------------------------------------------------------------------
#LOGIN
login.pushButton.clicked.connect(validalogin)
login.pushButton_2.clicked.connect(abreregistro)
login.checkBox.stateChanged.connect(saveuser)
#--------------------------------------------------------------------------
#REGISTROS
registro.pushButton_2.clicked.connect(registra)
registro.olhosenha.clicked.connect(olhosenha)
registro.password.setEchoMode(registro.password.Password)
registro.c_password.setEchoMode(registro.password.Password)
registro.olhosenha.setIcon(QIcon(QPixmap('icones/fechado.png')))
#--------------------------------------------------------------------------
##ADDMESAS
addmesa.adicionar.clicked.connect(addmesas)

#--------------------------------------------------------------------------
#ESTOQUE

adestoque.adicionar.clicked.connect(addestoque)

#--------------------------------------------------------------------------
###COMANDAS

comanda.adicionar.clicked.connect(abreaddproduto)
adproduto.adicionar.clicked.connect(addproduto)

#--------------------------------------------------------------------------
##INICIOS
inicio.mesas.clicked.connect(abremesas)
inicio.adicionar.clicked.connect(abreaddmesas)
inicio.excluir.clicked.connect(delmesa)
inicio.avulsos.clicked.connect(abreavulsos)
inicio.adicionar_2.clicked.connect(abreaddestoque)



app.exec()
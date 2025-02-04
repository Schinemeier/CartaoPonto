import tkinter as tk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import messagebox,Tk, Label, Entry, Button, ttk
import datetime,sqlite3 

''' CRIA/CONECTA AO BANCO DE DADOS '''
def createConnectionDB(DB_name):
    connectDB = sqlite3.connect(DB_name)
    #print(f'Banco de dados {DB_name} criado/conectado com sucesso.')
    return connectDB

''' CRIA AS TABELAS NECESSÁRIAS NO BANCO DE DADOS '''
def createTables(connectDB):
    cursor = connectDB.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS funcionario(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,
            nome varchar (100) NOT NULL
    )''')

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS registros(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            horario_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            id_funcionario INTEGER,
            FOREIGN KEY (id_funcionario) REFERENCES funcionario(id)
    )''')

    connectDB.commit()

''' CRIA O RETANGULO PADRÃO PARA AS TELAS ''' 
def retangulo():
    ret = Label(window, text="")
    ret["padx"] = 800
    ret["pady"] = 320
    ret.place(x= 0, y=0)

    ## REDE
    '''lblRede = Label(window, text="Rede: ")
    lblRede.place(x= 240, y=370)
    
    lblRedeCon = Label(window, text="Conectado")
    lblRedeCon.place(x= 280, y=370)
    lblRedeCon.config(fg="green")
    lblRedeCon["font"] = ("verdana", "9","bold")'''

    ## DATABASE
    lblDB = Label(window, text="DataBase: ")
    lblDB.place(x= 430, y=370)
    
    if is_connectDB == True:
        lblDBCon = Label(window, text="Conectado")
        lblDBCon.place(x= 490, y=370)
        lblDBCon.config(fg="green")
        lblDBCon["font"] = ("verdana", "9","bold")
    elif is_connectDB == False:
        lblDBCon = Label(window, text="Desconectado")
        lblDBCon.place(x= 490, y=370)
        lblDBCon.config(fg="red")
        lblDBCon["font"] = ("verdana", "9","bold")

''' ATUALIZA O RELOGIO NO PROGRAMA '''
def atualizar_horario(): 
    dateTimeNow = datetime.datetime.now()
    dateTimeFormatted = dateTimeNow.strftime("%d/%m/%Y\n%H:%M:%S")
    # Atualiza o texto da label 
    lblData = Label(window, text=dateTimeFormatted)
    lblData.place(x= 280, y=20)
    lblData["font"] = ("verdana", "25","bold")
    lblData.config(text=dateTimeFormatted) 
    # Agenda a próxima atualização após 1000 ms (1 segundo) 
    window.after(1000, atualizar_horario)

''' SALVA CADA REGISTRO DE PONTO '''
def salvarRegistro(codFun):
    TimeNow = datetime.datetime.now()
    TimeFormatted = TimeNow.strftime("%d/%m/%Y - %H:%M:%S") 
    idFun = str(codFun.get())
    
    cursor = connectDB.cursor()
    cursor.execute('''
        INSERT INTO registros (id_funcionario) VALUES (?)
    ''',(idFun,))
    connectDB.commit()
    messagebox.showinfo(title="Informação", message="Registro de ponto efetuado!\nCod. Funcionário: " + idFun + "\nHorário: " + TimeFormatted)
    codFun.delete(0,15)

''' GERENCIAMENTO DE REGISTROS '''
def gerarPDF():
    pass
    
def relatorioPonto():


    def boxes():
        retangulo()
        print(opcaoRadio.get())    
        escolha = opcaoRadio.get()
        
        if escolha == "Funcionario":
            lblCodFunc = Label(window, text="Cod. Funcionário:").place(x= 255, y=110)
            codFunc = Entry(window)
            codFunc["font"] = ("verdana", "15","bold")
            codFunc.place(x= 260, y=130)

            codBusca = ""

            def busca():
                codBusca = codFunc.get()
                requisicaoSQL()
            
            def requisicaoSQL():
                
                cursor = connectDB.cursor()
            
                comando_SQL = '''SELECT re.horario_registro, re.id_funcionario, fu.nome FROM registros re 
                LEFT JOIN funcionario fu
                ON re.id_funcionario = fu.id
                WHERE re.id_funcionario = ?
                ORDER BY re.horario_registro DESC'''

                cursor.execute(comando_SQL,(codBusca,))
                colun = [descricao[0] for descricao in cursor.description]
                leitura_banco = cursor.fetchall()

                regPonto = ttk.Treeview(window, columns=colun, show="headings")

                for coluna in colun:
                    regPonto.heading(coluna, text=coluna)
                    regPonto.column(coluna,width=100)

                for linha in leitura_banco:
                    regPonto.insert("", tk.END,values=linha)

                regPonto.pack(expand=True, fill="both")
                regPonto.place(x=150, y=115, width=500, height=205)


            btnBusca = Button(window, text="BUSCAR", command= busca)
            btnBusca.config(fg="white", bg=bg_btn)
            btnBusca["padx"] = 50
            btnBusca["pady"] = 5
            btnBusca["font"] = ("Verdana", "10", "bold")
            btnBusca.place(x=310, y=330)

            btnVoltar = Button(window, text="VOLTAR", command= relatorioPonto)
            btnVoltar.config(fg="white", bg=bg_btn)
            btnVoltar["padx"] = 50
            btnVoltar["pady"] = 5
            btnVoltar["font"] = ("Verdana", "10", "bold")
            btnVoltar.place(x=600, y=330)

            

            #gerarPDF(escolha)
        if escolha == "Periodo":
            gerarPDF(escolha)
        if escolha == "Tudo":
            gerarPDF(escolha)

    retangulo()
    
    opcaoRadio = tk.StringVar(value="")

    checkBoxFuncionario = tk.Radiobutton(window,text="Por Funcionário", variable=opcaoRadio , value="Funcionario",command=None)
    checkBoxPeriodo = tk.Radiobutton(window,text="Por Período", variable=opcaoRadio , value="Periodo", command=None)
    checkBoxTudo = tk.Radiobutton(window,text="Tudo", variable=opcaoRadio , value="Tudo", command=None)
    
    checkBoxFuncionario.pack(padx=20,pady=20)
    checkBoxFuncionario.place(x=200,y=110)
    
    checkBoxPeriodo.pack(padx=20,pady=20)
    checkBoxPeriodo.place(x=370,y=110)
    
    checkBoxTudo.pack(padx=20,pady=20)
    checkBoxTudo.place(x=540,y=110)

    #print(opcaoRadio)

    btnGerar = Button(window, text="GERAR PDF", command= boxes)
    btnGerar.config(fg="white", bg=bg_btn)
    btnGerar["padx"] = 50
    btnGerar["pady"] = 5
    btnGerar["font"] = ("Verdana", "10", "bold")
    btnGerar.place(x=310, y=330)

    btnVoltar = Button(window, text="VOLTAR", command= recuperarRegistros)
    btnVoltar.config(fg="white", bg=bg_btn)
    btnVoltar["padx"] = 50
    btnVoltar["pady"] = 5
    btnVoltar["font"] = ("Verdana", "10", "bold")
    btnVoltar.place(x=600, y=330)

def recuperarRegistros():
    retangulo()

    cursor = connectDB.cursor()
    #comando_SQL = 'SELECT horario_registro, id_funcionario, nome FROM registros, funcionario ORDER BY horario_registro DESC'

    comando_SQL = '''SELECT re.horario_registro, re.id_funcionario, fu.nome FROM registros re 
    LEFT JOIN funcionario fu
    ON re.id_funcionario = fu.id
    ORDER BY re.horario_registro DESC'''
    cursor.execute(comando_SQL)
    colun = [descricao[0] for descricao in cursor.description]
    leitura_banco = cursor.fetchall()

    regPonto = ttk.Treeview(window, columns=colun, show="headings")

    for coluna in colun:
        regPonto.heading(coluna, text=coluna)
        regPonto.column(coluna,width=100)
    
    for linha in leitura_banco:
        regPonto.insert("", tk.END,values=linha)
  
    regPonto.pack(expand=True, fill="both")
    regPonto.place(x=150, y=115, width=500, height=205)

    btnRelatorio = Button(window, text="RELATÓRIO", command= relatorioPonto)
    btnRelatorio.config(fg="white", bg=bg_btn)
    btnRelatorio["padx"] = 50
    btnRelatorio["pady"] = 5
    btnRelatorio["font"] = ("Verdana", "10", "bold")
    btnRelatorio.place(x=310, y=330)

    btnVoltar = Button(window, text="VOLTAR", command= tela)
    btnVoltar.config(fg="white", bg=bg_btn)
    btnVoltar["padx"] = 50
    btnVoltar["pady"] = 5
    btnVoltar["font"] = ("Verdana", "10", "bold")
    btnVoltar.place(x=600, y=330)

''' GERENCIAMENTO DE FUNCIONÁRIOS '''    
def gerenciarFuncionario():
    retangulo()
    
    '''btnRegistros = Button(window, text="LISTAR", command=displayListFuncionario)
    btnRegistros.config(fg="white", bg=bg_btn)
    btnRegistros["padx"] = 65
    btnRegistros["pady"] = 5
    btnRegistros["font"] = ("Verdana", "10", "bold")
    btnRegistros.place(x=300, y=120)'''

    cursor = connectDB.cursor()
    cursor.execute("SELECT * FROM funcionario")
    colunas = [descricao[0] for descricao in cursor.description]
    funcionarios = cursor.fetchall()

    tree = ttk.Treeview(window,columns=colunas, show="headings")

    for coluna in colunas:
        tree.heading(coluna, text=coluna)
        tree.column(coluna,width=100)

    for linha in funcionarios:
        tree.insert("",tk.END, values=linha)

    tree.pack(expand=True, fill="both")
    tree.place(x=150, y=115, width=500, height=205)

    btnRegistros = Button(window, text="ADICIONAR", command=displayAddFuncionario)
    btnRegistros.config(fg="white", bg=bg_btn)
    btnRegistros["padx"] = 45
    btnRegistros["pady"] = 5
    btnRegistros["font"] = ("Verdana", "10", "bold")
    btnRegistros.place(x=40, y=330)

    btnRegistros = Button(window, text="REMOVER", command=displayRemoverFuncionario)
    btnRegistros.config(fg="white", bg=bg_btn)
    btnRegistros["padx"] = 45
    btnRegistros["pady"] = 5
    btnRegistros["font"] = ("Verdana", "10", "bold")
    btnRegistros.place(x=310, y=330)

    btnVoltar = Button(window, text="VOLTAR", command=tela)
    btnVoltar.config(fg="white", bg=bg_btn)
    btnVoltar["padx"] = 45
    btnVoltar["pady"] = 5
    btnVoltar["font"] = ("Verdana", "10", "bold")
    btnVoltar.place(x=600, y=330)

''' LISTAR FUNCIONÁRIOS ''' 
'''def displayListFuncionario():
    retangulo()   

    btnVoltar = Button(window, text="VOLTAR", command=gerenciarFuncionario)
    btnVoltar.config(fg="white", bg=bg_btn)
    btnVoltar["padx"] = 45
    btnVoltar["pady"] = 5
    btnVoltar["font"] = ("Verdana", "10", "bold")
    btnVoltar.place(x=600, y=330)'''

''' ADICIONA UM FUNCIONARIO NO CADASTRO '''    
def addFuncionario(addFun):
    addFunc = str(addFun.get())
    cursor = connectDB.cursor()
    cursor.execute('''
        INSERT INTO funcionario (nome) VALUES (?)
    ''',(addFunc,))
    connectDB.commit()
    addFun.delete(0,40)

    gerenciarFuncionario()

def displayAddFuncionario():
    retangulo()

    nomeFuncionario= Label(window, text="Nome do Funcionário:").place(x= 255, y=110)
    addFun = Entry(window)
    addFun["font"] = ("verdana", "15","bold")
    addFun.place(x= 260, y=130)

    btnCadastrar = Button(window, text="CADASTRAR", command= lambda: addFuncionario(addFun))
    btnCadastrar.config(fg="white", bg=bg_btn)
    btnCadastrar["padx"] = 90
    btnCadastrar["pady"] = 15
    btnCadastrar["font"] = ("Verdana", "13", "bold")
    btnCadastrar.place(x=245, y=180)

    btnVoltar = Button(window, text="VOLTAR", command=gerenciarFuncionario)
    btnVoltar.config(fg="white", bg=bg_btn)
    btnVoltar["padx"] = 45
    btnVoltar["pady"] = 5
    btnVoltar["font"] = ("Verdana", "10", "bold")
    btnVoltar.place(x=600, y=330)

''' REMOVE UM FUNCIONARIO NO CADASTRO '''
def removerFuncionario(removFunc):
    remFunc = str(removFunc.get())
    cursor = connectDB.cursor()
    cursor.execute('''
        DELETE FROM funcionario WHERE id=?
    ''',(remFunc,))
    connectDB.commit()
    removFunc.delete(0,40)

    gerenciarFuncionario()

def displayRemoverFuncionario():
    retangulo()

    idFuncionario= Label(window, text="Cod. do Funcionário:").place(x= 255, y=110)
    removeFun = Entry(window)
    removeFun["font"] = ("verdana", "15","bold")
    removeFun.place(x= 260, y=130)

    btnRemover = Button(window, text="REMOVER", command= lambda: removerFuncionario(removeFun))
    btnRemover.config(fg="white", bg=bg_btn)
    btnRemover["padx"] = 100
    btnRemover["pady"] = 15
    btnRemover["font"] = ("Verdana", "13", "bold")
    btnRemover.place(x=245, y=180)

    btnVoltar = Button(window, text="VOLTAR", command=gerenciarFuncionario)
    btnVoltar.config(fg="white", bg=bg_btn)
    btnVoltar["padx"] = 45
    btnVoltar["pady"] = 5
    btnVoltar["font"] = ("Verdana", "10", "bold")
    btnVoltar.place(x=600, y=330)

''' TELA INICIAL '''
def tela():
    window.title("Registro de Ponto")
    window.geometry("800x400")  
    retangulo()
    atualizar_horario()
    
    ## TELA INICIAL
    lblCodFunc = Label(window, text="Cod. Funcionário:").place(x= 255, y=110)
    codFunc = Entry(window)
    codFunc["font"] = ("verdana", "15","bold")
    codFunc.place(x= 260, y=130)

    btnPonto = Button(window, text="BATER PONTO", command=lambda:salvarRegistro(codFunc))
    btnPonto.config(fg="white", bg=bg_btn)
    btnPonto["padx"] = 90
    btnPonto["pady"] = 15
    btnPonto["font"] = ("Verdana", "13", "bold")
    btnPonto.place(x=235, y=180)
    
    btnRegistros = Button(window, text="REGISTROS", command=recuperarRegistros)
    btnRegistros.config(fg="white", bg=bg_btn)
    btnRegistros["padx"] = 120
    btnRegistros["pady"] = 5
    btnRegistros["font"] = ("Verdana", "10", "bold")
    btnRegistros.place(x=235, y=280)

    btnCadFunc = Button(window, text="FUNCIONÁRIOS", command=gerenciarFuncionario)
    btnCadFunc.config(fg="white", bg=bg_btn)
    btnCadFunc["padx"] = 105
    btnCadFunc["pady"] = 5
    btnCadFunc["font"] = ("Verdana", "10", "bold")
    btnCadFunc.place(x=235, y=320)    

    window.mainloop()
    
if __name__ == '__main__':
    tamanho_x = 110
    tamanho_y = 15
    is_connectDB = False
    bg_btn = "#008B8B"
    window = Tk()
    connectDB = createConnectionDB("Cartao_Ponto.db") # Nome do database
    createTables(connectDB)
    
    if connectDB:
        is_connectDB = True
    
    tela()    
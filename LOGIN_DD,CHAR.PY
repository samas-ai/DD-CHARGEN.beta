
import tkinter as tk
from tkinter import Toplevel
import customtkinter as ctk
import sqlite3 
from tkinter import *
from tkinter import messagebox
class BackEnd():
 
    def conecta_db(self):
        self.conn = sqlite3.connect("DD_CHARGEN.db")
        self.cursor = self.conn.cursor()
        print("Banco de dados Conectado")
    def desconecta_db(self):
        self.conn.close()
        print("Banco de dados Desconectado")

    def criar_tabela(self):
        self.conecta_db()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Senha TEXT NOT NULL,
                Confirma_Senha TEXT NOT NULL

            );
        """)
        self.conn.commit()
        print("Tabela criada com sucesso")
        self.desconecta_db()


    def cadastrar_usuario_bdd(self):
        self.usarname_cadastro_bd = self.cadastro_user.get()
        self.senha_cadastro_bd = self.cadastro_senha.get()
        self.csenha_cadastro_bd = self.confirmar_senha.get()

        self.conecta_db()

        self.cursor.execute("""
            INSERT INTO Usuarios (Username, Senha, Confirma_senha)
            VALUES (?, ?, ?)""", (self.usarname_cadastro_bd, self.senha_cadastro_bd, self.csenha_cadastro_bd))
        try:
            if(self.usarname_cadastro_bd == "" or self.senha_cadastro_bd == "" or self.csenha_cadastro_bd == ""):
                messagebox.showerror(title="Sistema de login", message= "ERROR!!! \nPor favor preencha todos os campos!")
        
            elif (len(self.usarname_cadastro_bd) <= 4):
                messagebox.showwarning(title="Sistema de login", message="Nome de Usuario deve ter mais do que 4 caracteres")

            elif (len(self.senha_cadastro_bd) <= 4):
                messagebox.showwarning(title="Sistema de login", message="A senha deve ter mais do que 4 caracteres")

            
            elif (self.senha_cadastro_bd != self.csenha_cadastro_bd):
                messagebox.showerror(title="Sistema de login", message= "ERROR \n As senhas não coincidem.")
            
            else:
                self.conn.commit()
                messagebox.showinfo(title="Sistema de Login", message=(f"Parabéns {self.usarname_cadastro_bd} \nSua conta foi criada com sucesso"))
                self.desconecta_db()
                self.limpar_entry_cadastro()
        except:
            messagebox.showerror(title= "Sistema de Login",message= "ERROR NO PROCESSAMENTO DO CADASTRO")
            self.desconecta_db()
    def verifica_login(self):
        self.username_login = self.user.get()
        self.senha_login = self.senha.get()

        self.conecta_db()
        
        self.cursor.execute("""SELECT * FROM Usuarios WHERE (Username = ? AND Senha = ?)""", (self.username_login, self.senha_login))
        self.verifica_dados = self.cursor.fetchone() #percorrendo a Tabela de usuarios

        try:
            if self.username_login in self.verifica_dados and self.senha_login in self.verifica_dados:
                messagebox.showinfo(title="Sistema de Login", message=f"Parabéns {self.username_login}\nLogin feito com sucesso")
                self.menu()
                self.desconecta_db()
                self.limpar_entry_login()
            else:
                messagebox.showerror(title="Sistema de login", message="Login inválido")
                self.desconecta_db()
        except:
            self.desconecta_db()

class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.Cores()
        self.configurar_janela_inicial()
        self.tela_login()
        self.criar_tabela()
    def Cores(self):
        self.c1 = "#000000"  # preto
        self.c2 = "#FFFFFF"  # branco                                                       
        self.c3 = "#F8F6EA"  # branco/bege
        self.c4 = "#000711"  # AZUL FOSCO/MAR
        self.c5 = "#1F1F1F"  # transparente
        self.c6 = "#560000"  # vermelho
        self.c7 = "#5A6770"  # cinza/dragao
        self.c8 = "#838383"  # cinza/borda

    def configurar_janela_inicial(self):
        self.geometry("1920x1080")
        self.title("DD CHAR GEN")
        

    def tela_login(self):
        # Frame GERAL
        self.tela_frame = ctk.CTkFrame(self, width= 1920, height= 1080)
        self.tela_frame.place(x = 0, y = 0)
        # BACKGROUND
        self.background_img = PhotoImage(file = "imagens\POHA-PFVR.png")
        self.back_img = ctk.CTkLabel(self.tela_frame, text=None, image= self.background_img)
        self.back_img.grid(row = 1, column = 0,)
        # FRAME LOGIN
        self.login_frame = ctk.CTkFrame(self.tela_frame, width=400, height=353, border_width= 2, border_color= self.c1, fg_color = "#FFD8BB" )
        self.login_frame.place(x = 930, y = 358)

        # WIDGETS V

        # Usuario
        self.user = ctk.CTkEntry(self.login_frame, width= 332, height= 52, placeholder_text= "Nome de Usuario", font=("PtSerif", 20), text_color= self.c2,fg_color = ("#061121"),border_color= self.c7, border_width= 3, corner_radius= 10)
        self.user.place(x = 32, y = 33)

        # Senha

        self.senha = ctk.CTkEntry(self.login_frame, width= 332, height= 52, placeholder_text= "Senha", font=("PtSerif", 20), text_color= self.c2,fg_color = ("#061121"), border_color= self.c7,border_width= 3, corner_radius= 10, show = "*")
        self.senha.place(x = 32, y = 121)

        # Botão para ver senhaz

        self.ver_senha = ctk.CTkCheckBox(self.login_frame, text= "Clique para ver a Senha", font=("PtSerif", 12), text_color= self.c1, corner_radius= 10)
        self.ver_senha.place(x = 45, y = 194)

        # Botão entrar

        self.entrar = ctk.CTkButton(self.login_frame, width= 300, height= 45, text= "ENTRAR", font=("PtSerif", 20), fg_color = ("#061121"),border_color= self.c7, border_width= 3, corner_radius= 15, command= self.verifica_login)
        self.entrar.place(x = 45, y = 230)

        # Botão criar conta

        self.criar_conta = ctk.CTkButton(self.login_frame, text="CRIAR CONTA", font=("PtSerif", 12), fg_color=self.c6, border_color=self.c1, hover_color="#3E0101", border_width= 3, width=150, height=39, corner_radius= 15, command= self.tela_de_cadastro)
        self.criar_conta.place(x = 123, y = 289)
    def tela_de_cadastro(self):
        # REMOVENDO TELA DE LOGIN
        self.login_frame.place_forget()

        # Widgets tela de cadastro

        self.registro_frame = ctk.CTkFrame(self, width= 400, height= 433, border_width= 2, border_color= self.c1, fg_color= "#ffd8bb")
        self.registro_frame.place(x = 930, y =358)

        # CADASTRAR Usuario
        self.cadastro_user = ctk.CTkEntry(self.registro_frame, width= 332, height= 52, placeholder_text= "Nome de Usuario", font=("PtSerif", 20), text_color= self.c2,fg_color = ("#061121"),border_color= self.c7, border_width= 3, corner_radius= 10)
        self.cadastro_user.place(x = 32, y = 33)
        
        # CADASTRAR Senha

        self.cadastro_senha = ctk.CTkEntry(self.registro_frame, width= 332, height= 52, placeholder_text= "Senha", font=("PtSerif", 20), text_color= self.c2,fg_color = ("#061121"), border_color= self.c7,border_width= 3, corner_radius= 10, show = "*")
        self.cadastro_senha.place(x = 32, y = 116)

        # CONFIRMAR Senha

        self.confirmar_senha = ctk.CTkEntry(self.registro_frame, width= 332, height= 52, placeholder_text= "Confirmar Senha", font=("PtSerif", 20), text_color= self.c2,fg_color = ("#061121"), border_color= self.c7,border_width= 3, corner_radius= 10, show = "*")
        self.confirmar_senha.place(x = 32, y = 198)

        # REGISTRE-SE

        self.registre_se = ctk.CTkButton(self.registro_frame, width= 300, height= 45, text= "Registre-se", font=("PtSerif", 20), fg_color = ("#061121"),border_color= self.c7, border_width= 3, corner_radius= 15, command= self.cadastrar_usuario_bdd)
        self.registre_se.place(x = 45, y = 280)


        # OU 
        self.ou_lb = ctk.CTkLabel(self.registro_frame, width= 30, height= 16, text= "OU", text_color= self.c1, font=("PtSerif", 20))
        self.ou_lb.place(x = 187, y = 330)

        # VOLTAR

        self.voltar = ctk.CTkButton(self.registro_frame, text="VOLTAR", font=("PtSerif", 12), fg_color=self.c6, border_color=self.c1, hover_color="#3E0101", border_width= 3, width=150, height=39, corner_radius= 15, command= self.voltar_login)
        self.voltar.place(x = 125, y = 364)
    
    def menu(self):
        self.tela_frame.destroy()

        #FRAME MENU
        self.frame_menu = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_menu.place(x = 0, y = 0)
    
        # BACKGROUND MENU
        self.background_menu = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_menu = ctk.CTkLabel(self.frame_menu,text= None, image= self.background_menu)
        self.label_menu.place(x= 0, y = 0)
        
        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_menu, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_menu, text=None, image=self.imagem_menu, bd=0, highlightthickness=0)
        self.botao_menu.place(x=0, y=125)

        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_menu, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_menu, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_menu, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO CLASSES
        self.classes = PhotoImage(file="imagens/Menu/CLASSES.png")
        self.botao_classes = Button(self.frame_menu, text=None, image=self.classes, highlightthickness=0, bd=0, command=self.homepage)
        self.botao_classes.place(x=320, y=150)

        #BOTÃO RAÇAS
        self.racas = PhotoImage(file="imagens/Menu/RAÇAS.png")
        self.botao_racas = Button(self.frame_menu, text=None, image=self.racas, highlightthickness=0, bd=0, command=self.raças)
        self.botao_racas.place(x=860, y=150)

        #BOTÃO EQUIPAMENTOS
        self.equipamentos = PhotoImage(file="imagens/Menu/EQUIPAMENTOS.png")
        self.botao_equipamentos = Button(self.frame_menu, text=None, image=self.equipamentos, highlightthickness=0, bd=0)
        self.botao_equipamentos.place(x=1400, y=150)

        #BOTAO MAGIAS
        self.magias = PhotoImage(file="imagens/Menu/MAGIAS.png")
        self.botao_magias = Button(self.frame_menu, text=None, image=self.magias, highlightthickness=0, bd=0)
        self.botao_magias.place(x=635, y=600)



    def homepage(self):
        self.tela_frame.destroy()
        
        # FRAME PRINCIPAL HOMEPAGE
        self.frame_homepage = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_homepage.place(x = 0, y = 0)
        
        # BACKGROUND IMAGE
        self.background_homepage = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_homepage = ctk.CTkLabel(self.frame_homepage,text= None, image= self.background_homepage)
        self.label_homepage.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_homepage, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)
        
        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_homepage, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_homepage, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_homepage, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_homepage, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #----------------CLASSES----------------------#

        #BOTÃO BÁRBARO
        self.barbaro = PhotoImage(file="imagens/Classes/BARBARO.png")
        self.botao_barbaro = Button(self.frame_homepage, text=None, image=self.barbaro, bd=0, highlightthickness=0, command=self.tela_barbaro)
        self.botao_barbaro.place(x=350, y=130)

        #BOTÃO MONGE
        self.monge = PhotoImage(file="imagens/Classes/Monge.png")
        self.botao_monge = Button(self.frame_homepage, text=None, image=self.monge, bd=0, highlightthickness=0, command=self.tela_monge)
        self.botao_monge.place(x=350, y=400)

        #BOTÃO BRUXO
        self.bruxo = PhotoImage(file="imagens/Classes/Bruxo.png")
        self.botao_bruxo = Button(self.frame_homepage, text=None, image=self.bruxo, bd=0, highlightthickness=0, command=self.tela_bruxo)
        self.botao_bruxo.place(x=350, y=670)

        #BOTÃO BARDO
        self.bardo = PhotoImage(file="imagens/Classes/BARDO.png")
        self.botao_bardo = Button(self.frame_homepage, text=None, image=self.bardo, bd=0, highlightthickness=0, command=self.tela_bardo)
        self.botao_bardo.place(x=660, y=130)

        #BOTÃO CLERIGO
        self.clerigo = PhotoImage(file="imagens/Classes/Clerigo.png")
        self.botao_clerigo = Button(self.frame_homepage, text=None, image=self.clerigo, bd=0, highlightthickness=0, command=self.tela_clerigo)
        self.botao_clerigo.place(x=970, y=130)

        #BOTÃO DRUIDA
        self.druida = PhotoImage(file="imagens/Classes/DRUIDA.png")
        self.botao_druida = Button(self.frame_homepage, text=None, image=self.druida, bd=0, highlightthickness=0, command=self.tela_druida)
        self.botao_druida.place(x=1280, y=130)

        #BOTÃO GUERREIRO
        self.guerreiro = PhotoImage(file="imagens/Classes/Guerreiro.png")
        self.botao_guerreiro = Button(self.frame_homepage, text=None, image=self.guerreiro, bd=0, highlightthickness=0, command=self.tela_guerreiro)
        self.botao_guerreiro.place(x=1590, y=130)

        #BOTÃO PALADINO
        self.paladino = PhotoImage(file="imagens/Classes/Paladino.png")
        self.botao_paladino = Button(self.frame_homepage, text=None, image=self.paladino, bd=0, highlightthickness=0, command=self.tela_paladino)
        self.botao_paladino.place(x=660, y=400)

        #BOTÃO RANGER
        self.ranger = PhotoImage(file="imagens/Classes/Ranger.png")
        self.botao_ranger = Button(self.frame_homepage, text=None, image=self.ranger, bd=0, highlightthickness=0, command=self.tela_ranger)
        self.botao_ranger.place(x=970, y=400)

        #BOTÃO ASSASSINO
        self.assassino = PhotoImage(file="imagens/Classes/Assassino.png")
        self.botao_assassino = Button(self.frame_homepage, text=None, image=self.assassino, bd=0, highlightthickness=0, command=self.tela_ladino)
        self.botao_assassino.place(x=1280, y=400)

        #BOTÃO FEITICEIRO
        self.feiticeiro = PhotoImage(file="imagens/Classes/Feiticeiro.png")
        self.botao_feiticeiro = Button(self.frame_homepage, text=None, image=self.feiticeiro, bd=0, highlightthickness=0, command=self.tela_feiticeiro)
        self.botao_feiticeiro.place(x=1590, y=400)

        #BOTÃO MAGO
        self.mago = PhotoImage(file="imagens/Classes/MAGO.png")
        self.botao_mago = Button(self.frame_homepage, text=None, image=self.mago, bd=0, highlightthickness=0, command=self.tela_mago)
        self.botao_mago.place(x=660, y=670)



    def tela_barbaro(self):
        self.tela_frame.destroy()

        self.frame_barbaro = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_barbaro.place(x = 0, y = 0)

        self.background_barbaro = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_barbaro = ctk.CTkLabel(self.frame_barbaro,text= None, image= self.background_homepage)
        self.label_barbaro.place(x= 0, y = 0)

         #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_barbaro, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)
        

        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_barbaro, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_barbaro, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_barbaro, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_barbaro, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_barbaro, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.homepage)
        self.botao_retornar.place(x=1810, y=0)

        self.maior_barbaro = PhotoImage(file ="imagens/Telas classes/Tela barbaro/BARBARO.png")
        self.label_maior_barbaro = ctk.CTkLabel(self.frame_barbaro,text= None, image= self.maior_barbaro)
        self.label_maior_barbaro.place(x= 270, y = 110)

        self.texto_barbaro = PhotoImage(file ="imagens/Telas classes/Tela barbaro/Texto barbaro.png")
        self.label_texto_barbaro = ctk.CTkLabel(self.frame_barbaro,text= None, image= self.texto_barbaro)
        self.label_texto_barbaro.place(x= 670, y = 30)

        self.texto_barbaro2 = PhotoImage(file ="imagens/Telas classes/Tela barbaro/Texto barbaro 2.png")
        self.label_texto_barbaro2 = ctk.CTkLabel(self.frame_barbaro,text= None, image= self.texto_barbaro2)
        self.label_texto_barbaro2.place(x= 665, y = 430)

        self.texto_barbaro3 = PhotoImage(file ="imagens/Telas classes/Tela barbaro/Texto barbaro 3.png")
        self.label_texto_barbaro3 = ctk.CTkLabel(self.frame_barbaro,text= None, image= self.texto_barbaro3)
        self.label_texto_barbaro3.place(x= 270, y = 470)


    def tela_bardo(self):
        self.tela_frame.destroy()

        self.frame_bardo = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_bardo.place(x = 0, y = 0)

        self.background_bardo = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_bardo = ctk.CTkLabel(self.frame_bardo,text= None, image= self.background_homepage)
        self.label_bardo.place(x= 0, y = 0)

         #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_bardo, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)
        

        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_bardo, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_bardo, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_bardo, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_bardo, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_bardo, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.homepage)
        self.botao_retornar.place(x=1810, y=0)

        self.maior_bardo = PhotoImage(file ="imagens/Telas classes/Tela bardo/BARDO.png")
        self.label_maior_bardo = ctk.CTkLabel(self.frame_bardo,text= None, image= self.maior_bardo)
        self.label_maior_bardo.place(x= 270, y = 110)

        self.texto_bardo = PhotoImage(file ="imagens/Telas classes/Tela bardo/Texto bardo.png")
        self.label_texto_bardo = ctk.CTkLabel(self.frame_bardo,text= None, image= self.texto_bardo)
        self.label_texto_bardo.place(x= 670, y = 30)

        self.texto_bardo2 = PhotoImage(file ="imagens/Telas classes/Tela bardo/Texto bardo 2.png")
        self.label_texto_bardo2 = ctk.CTkLabel(self.frame_bardo,text= None, image= self.texto_bardo2)
        self.label_texto_bardo2.place(x= 665, y = 430)

        self.texto_bardo3 = PhotoImage(file ="imagens/Telas classes/Tela bardo/Texto bardo 3.png")
        self.label_texto_bardo3 = ctk.CTkLabel(self.frame_bardo,text= None, image= self.texto_bardo3)
        self.label_texto_bardo3.place(x= 270, y = 470)

        
    def tela_clerigo(self):
        self.tela_frame.destroy()

        self.frame_clerigo = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_clerigo.place(x = 0, y = 0)

        self.background_clerigo = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_clerigo = ctk.CTkLabel(self.frame_clerigo,text= None, image= self.background_homepage)
        self.label_clerigo.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_clerigo, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)


        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_clerigo, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_clerigo, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_clerigo, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_clerigo, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_clerigo, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.homepage)
        self.botao_retornar.place(x=1810, y=0)


        self.maior_clerigo = PhotoImage(file ="imagens/Telas classes/Tela clerigo/CLERIGO.png")
        self.label_maior_clerigo = ctk.CTkLabel(self.frame_clerigo,text= None, image= self.maior_clerigo)
        self.label_maior_clerigo.place(x= 270, y = 110)

        self.texto_clerigo = PhotoImage(file ="imagens/Telas classes/Tela clerigo/Texto clerigo.png")
        self.label_texto_clerigo = ctk.CTkLabel(self.frame_clerigo,text= None, image= self.texto_clerigo)
        self.label_texto_clerigo.place(x= 670, y = 30)

        self.texto_clerigo2 = PhotoImage(file ="imagens/Telas classes/Tela clerigo/Texto clerigo 2.png")
        self.label_texto_clerigo2 = ctk.CTkLabel(self.frame_clerigo,text= None, image= self.texto_clerigo2)
        self.label_texto_clerigo2.place(x= 665, y = 430)

        self.texto_clerigo3 = PhotoImage(file ="imagens/Telas classes/Tela clerigo/Texto clerigo 3.png")
        self.label_texto_clerigo3 = ctk.CTkLabel(self.frame_clerigo,text= None, image= self.texto_clerigo3)
        self.label_texto_clerigo3.place(x= 270, y = 470)


    def tela_druida(self):
        self.tela_frame.destroy()

        self.frame_druida = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_druida.place(x = 0, y = 0)

        self.background_druida = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_druida = ctk.CTkLabel(self.frame_druida,text= None, image= self.background_homepage)
        self.label_druida.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_druida, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)
        

        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_druida, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_druida, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_druida, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_druida, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_druida, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.homepage)
        self.botao_retornar.place(x=1810, y=0)


        self.maior_druida = PhotoImage(file ="imagens/Telas classes/Tela druida/DRUIDA.png")
        self.label_maior_druida = ctk.CTkLabel(self.frame_druida,text= None, image= self.maior_druida)
        self.label_maior_druida.place(x= 270, y = 110)

        self.texto_druida = PhotoImage(file ="imagens/Telas classes/Tela druida/Texto druida.png")
        self.label_texto_druida = ctk.CTkLabel(self.frame_druida,text= None, image= self.texto_druida)
        self.label_texto_druida.place(x= 670, y = 30)

        self.texto_druida2 = PhotoImage(file ="imagens/Telas classes/Tela druida/Texto druida 2.png")
        self.label_texto_druida2 = ctk.CTkLabel(self.frame_druida,text= None, image= self.texto_druida2)
        self.label_texto_druida2.place(x= 665, y = 430)

        self.texto_druida3 = PhotoImage(file ="imagens/Telas classes/Tela druida/Texto druida 3.png")
        self.label_texto_druida3 = ctk.CTkLabel(self.frame_druida,text= None, image= self.texto_druida3)
        self.label_texto_druida3.place(x= 270, y = 470)


    def tela_bruxo(self):
        self.tela_frame.destroy()

        self.frame_bruxo = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_bruxo.place(x = 0, y = 0)

        self.background_bruxo = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_bruxo = ctk.CTkLabel(self.frame_bruxo,text= None, image= self.background_homepage)
        self.label_bruxo.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_bruxo, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)


        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_bruxo, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_bruxo, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_bruxo, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_bruxo, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_bruxo, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.homepage)
        self.botao_retornar.place(x=1810, y=0)

        self.maior_bruxo = PhotoImage(file ="imagens/Telas classes/Tela bruxo/BRUXO.png")
        self.label_maior_bruxo = ctk.CTkLabel(self.frame_bruxo,text= None, image= self.maior_bruxo)
        self.label_maior_bruxo.place(x= 270, y = 110)

        self.texto_bruxo = PhotoImage(file ="imagens/Telas classes/Tela bruxo/Texto bruxo.png")
        self.label_texto_bruxo = ctk.CTkLabel(self.frame_bruxo,text= None, image= self.texto_bruxo)
        self.label_texto_bruxo.place(x= 670, y = 30)

        self.texto_bruxo2 = PhotoImage(file ="imagens/Telas classes/Tela bruxo/Texto bruxo 2.png")
        self.label_texto_bruxo2 = ctk.CTkLabel(self.frame_bruxo,text= None, image= self.texto_bruxo2)
        self.label_texto_bruxo2.place(x= 665, y = 430)

        self.texto_bruxo3 = PhotoImage(file ="imagens/Telas classes/Tela bruxo/Texto bruxo 3.png")
        self.label_texto_bruxo3 = ctk.CTkLabel(self.frame_bruxo,text= None, image= self.texto_bruxo3)
        self.label_texto_bruxo3.place(x= 270, y = 470)


    def tela_feiticeiro(self):
        self.tela_frame.destroy()

        self.frame_feiticeiro = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_feiticeiro.place(x = 0, y = 0)

        self.background_feiticeiro = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_feiticeiro = ctk.CTkLabel(self.frame_feiticeiro,text= None, image= self.background_homepage)
        self.label_feiticeiro.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_feiticeiro, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)
        

        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_feiticeiro, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_feiticeiro, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_feiticeiro, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_feiticeiro, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_feiticeiro, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.homepage)
        self.botao_retornar.place(x=1810, y=0)

        self.maior_feiticeiro = PhotoImage(file ="imagens/Telas classes/Tela feiticeiro/FEITICEIRO.png")
        self.label_maior_feiticeiro = ctk.CTkLabel(self.frame_feiticeiro,text= None, image= self.maior_feiticeiro)
        self.label_maior_feiticeiro.place(x= 270, y = 110)

        self.texto_feiticeiro = PhotoImage(file ="imagens/Telas classes/Tela feiticeiro/Texto feiticeiro.png")
        self.label_texto_feiticeiro = ctk.CTkLabel(self.frame_feiticeiro,text= None, image= self.texto_feiticeiro)
        self.label_texto_feiticeiro.place(x= 670, y = 30)

        self.texto_feiticeiro2 = PhotoImage(file ="imagens/Telas classes/Tela feiticeiro/Texto feiticeiro 2.png")
        self.label_texto_feiticeiro2 = ctk.CTkLabel(self.frame_feiticeiro,text= None, image= self.texto_feiticeiro2)
        self.label_texto_feiticeiro2.place(x= 665 , y = 430)

        self.texto_feiticeiro3 = PhotoImage(file ="imagens/Telas classes/Tela feiticeiro/Texto feiticeiro 3.png")
        self.label_texto_feiticeiro3 = ctk.CTkLabel(self.frame_feiticeiro,text= None, image= self.texto_feiticeiro3)
        self.label_texto_feiticeiro3.place(x= 270, y = 470)


    def tela_guerreiro(self):
        self.tela_frame.destroy()

        self.frame_guerreiro = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_guerreiro.place(x = 0, y = 0)

        self.background_guerreiro = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_guerreiro = ctk.CTkLabel(self.frame_guerreiro,text= None, image= self.background_homepage)
        self.label_guerreiro.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_guerreiro, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)
        

        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_guerreiro, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_guerreiro, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_guerreiro, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_guerreiro, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_guerreiro, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.homepage)
        self.botao_retornar.place(x=1810, y=0)

        self.maior_guerreiro = PhotoImage(file ="imagens/Telas classes/Tela guerreiro/GUERREIRO.png")
        self.label_maior_guerreiro = ctk.CTkLabel(self.frame_guerreiro,text= None, image= self.maior_guerreiro)
        self.label_maior_guerreiro.place(x= 270, y = 110)

        self.texto_guerreiro = PhotoImage(file ="imagens/Telas classes/Tela guerreiro/Texto guerreiro.png")
        self.label_texto_guerreiro = ctk.CTkLabel(self.frame_guerreiro,text= None, image= self.texto_guerreiro)
        self.label_texto_guerreiro.place(x= 670, y = 30)

        self.texto_guerreiro2 = PhotoImage(file ="imagens/Telas classes/Tela guerreiro/Texto guerreiro 2.png")
        self.label_texto_guerreiro2 = ctk.CTkLabel(self.frame_guerreiro,text= None, image= self.texto_guerreiro2)
        self.label_texto_guerreiro2.place(x= 665 , y = 430)

        self.texto_guerreiro3 = PhotoImage(file ="imagens/Telas classes/Tela guerreiro/Texto guerreiro 3.png")
        self.label_texto_guerreiro3 = ctk.CTkLabel(self.frame_guerreiro,text= None, image= self.texto_guerreiro3)
        self.label_texto_guerreiro3.place(x= 270, y = 470)


    def tela_monge(self):
        self.tela_frame.destroy()

        self.frame_monge = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_monge.place(x = 0, y = 0)

        self.background_monge = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_monge = ctk.CTkLabel(self.frame_monge,text= None, image= self.background_homepage)
        self.label_monge.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_monge, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)

        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_monge, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_monge, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_monge, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_monge, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_monge, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.homepage)
        self.botao_retornar.place(x=1810, y=0)

        self.maior_monge = PhotoImage(file ="imagens/Telas classes/Tela monge/MONGE.png")
        self.label_maior_monge = ctk.CTkLabel(self.frame_monge,text= None, image= self.maior_monge)
        self.label_maior_monge.place(x= 270, y = 110)

        self.texto_monge = PhotoImage(file ="imagens/Telas classes/Tela monge/Texto monge.png")
        self.label_texto_monge = ctk.CTkLabel(self.frame_monge,text= None, image= self.texto_monge)
        self.label_texto_monge.place(x= 670, y = 30)

        self.texto_monge2 = PhotoImage(file ="imagens/Telas classes/Tela monge/Texto monge 2.png")
        self.label_texto_monge2 = ctk.CTkLabel(self.frame_monge,text= None, image= self.texto_monge2)
        self.label_texto_monge2.place(x= 665 , y = 430)

        self.texto_monge3 = PhotoImage(file ="imagens/Telas classes/Tela monge/Texto monge 3.png")
        self.label_texto_monge3 = ctk.CTkLabel(self.frame_monge,text= None, image= self.texto_monge3)
        self.label_texto_monge3.place(x= 270, y = 470)



    def tela_mago(self):
        self.tela_frame.destroy()

        self.frame_mago = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_mago.place(x = 0, y = 0)

        self.background_mago = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_mago = ctk.CTkLabel(self.frame_mago,text= None, image= self.background_homepage)
        self.label_mago.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_mago, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)

        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_mago, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_mago, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_mago, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_mago, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_mago, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.homepage)
        self.botao_retornar.place(x=1810, y=0)

        self.maior_mago = PhotoImage(file ="imagens/Telas classes/Tela mago/MAGO.png")
        self.label_maior_mago = ctk.CTkLabel(self.frame_mago,text= None, image= self.maior_mago)
        self.label_maior_mago.place(x= 270, y = 110)

        self.texto_mago = PhotoImage(file ="imagens/Telas classes/Tela mago/Texto mago.png")
        self.label_texto_mago = ctk.CTkLabel(self.frame_mago,text= None, image= self.texto_mago)
        self.label_texto_mago.place(x= 670, y = 30)

        self.texto_mago2 = PhotoImage(file ="imagens/Telas classes/Tela mago/Texto mago 2.png")
        self.label_texto_mago2 = ctk.CTkLabel(self.frame_mago,text= None, image= self.texto_mago2)
        self.label_texto_mago2.place(x= 665 , y = 430)

        self.texto_mago3 = PhotoImage(file ="imagens/Telas classes/Tela mago/Texto mago 3.png")
        self.label_texto_mago3 = ctk.CTkLabel(self.frame_mago,text= None, image= self.texto_mago3)
        self.label_texto_mago3.place(x= 270, y = 470)  



    def tela_ranger(self):
        self.tela_frame.destroy()

        self.frame_ranger = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_ranger.place(x = 0, y = 0)

        self.background_ranger = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_ranger = ctk.CTkLabel(self.frame_ranger,text= None, image= self.background_homepage)
        self.label_ranger.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_ranger, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)

        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_ranger, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_ranger, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_ranger, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_ranger, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_ranger, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.homepage)
        self.botao_retornar.place(x=1810, y=0)

        self.maior_ranger = PhotoImage(file ="imagens/Telas classes/Tela ranger/RANGER.png")
        self.label_maior_ranger = ctk.CTkLabel(self.frame_ranger,text= None, image= self.maior_ranger)
        self.label_maior_ranger.place(x= 270, y = 110)

        self.texto_ranger = PhotoImage(file ="imagens/Telas classes/Tela ranger/Texto ranger.png")
        self.label_texto_ranger = ctk.CTkLabel(self.frame_ranger,text= None, image= self.texto_ranger)
        self.label_texto_ranger.place(x= 670, y = 30)

        self.texto_ranger2 = PhotoImage(file ="imagens/Telas classes/Tela ranger/Texto ranger 2.png")
        self.label_texto_ranger2 = ctk.CTkLabel(self.frame_ranger,text= None, image= self.texto_ranger2)
        self.label_texto_ranger2.place(x= 665 , y = 430)

        self.texto_ranger3 = PhotoImage(file ="imagens/Telas classes/Tela ranger/Texto ranger 3.png")
        self.label_texto_ranger3 = ctk.CTkLabel(self.frame_ranger,text= None, image= self.texto_ranger3)
        self.label_texto_ranger3.place(x= 270, y = 470)


    def tela_paladino(self):
        self.tela_frame.destroy()

        self.frame_paladino = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_paladino.place(x = 0, y = 0)

        self.background_paladino = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_paladino = ctk.CTkLabel(self.frame_paladino,text= None, image= self.background_homepage)
        self.label_paladino.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_paladino, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)
        

        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_paladino, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_paladino, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_paladino, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_paladino, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_paladino, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.homepage)
        self.botao_retornar.place(x=1810, y=0)

        self.maior_paladino = PhotoImage(file ="imagens/Telas classes/Tela paladino/PALADINO.png")
        self.label_maior_paladino = ctk.CTkLabel(self.frame_paladino,text= None, image= self.maior_paladino)
        self.label_maior_paladino.place(x= 270, y = 110)

        self.texto_paladino = PhotoImage(file ="imagens/Telas classes/Tela paladino/Texto paladino.png")
        self.label_texto_paladino = ctk.CTkLabel(self.frame_paladino,text= None, image= self.texto_paladino)
        self.label_texto_paladino.place(x= 670, y = 30)

        self.texto_paladino2 = PhotoImage(file ="imagens/Telas classes/Tela paladino/Texto paladino 2.png")
        self.label_texto_paladino2 = ctk.CTkLabel(self.frame_paladino,text= None, image= self.texto_paladino2)
        self.label_texto_paladino2.place(x= 665 , y = 430)

        self.texto_paladino3 = PhotoImage(file ="imagens/Telas classes/Tela paladino/Texto paladino 3.png")
        self.label_texto_paladino3 = ctk.CTkLabel(self.frame_paladino,text= None, image= self.texto_paladino3)
        self.label_texto_paladino3.place(x= 270, y = 470)


    def tela_ladino(self):
        self.tela_frame.destroy()

        self.frame_ladino = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_ladino.place(x = 0, y = 0)

        self.background_ladino = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_ladino = ctk.CTkLabel(self.frame_ladino,text= None, image= self.background_homepage)
        self.label_ladino.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_ladino, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)

        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_ladino, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_ladino, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_ladino, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_ladino, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_ladino, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.homepage)
        self.botao_retornar.place(x=1810, y=0)

        self.maior_ladino = PhotoImage(file ="imagens/Telas classes/Tela ladino/LADINO.png")
        self.label_maior_ladino = ctk.CTkLabel(self.frame_ladino,text= None, image= self.maior_ladino)
        self.label_maior_ladino.place(x= 270, y = 110)

        self.texto_ladino = PhotoImage(file ="imagens/Telas classes/Tela ladino/Texto ladino.png")
        self.label_texto_ladino = ctk.CTkLabel(self.frame_ladino,text= None, image= self.texto_ladino)
        self.label_texto_ladino.place(x= 670, y = 30)

        self.texto_ladino2 = PhotoImage(file ="imagens/Telas classes/Tela ladino/Texto ladino 2.png")
        self.label_texto_ladino2 = ctk.CTkLabel(self.frame_ladino,text= None, image= self.texto_ladino2)
        self.label_texto_ladino2.place(x= 665 , y = 400)

        self.texto_ladino3 = PhotoImage(file ="imagens/Telas classes/Tela ladino/Texto ladino 3.png")
        self.label_texto_ladino3 = ctk.CTkLabel(self.frame_ladino,text= None, image= self.texto_ladino3)
        self.label_texto_ladino3.place(x= 270, y = 470)


    def raças(self):
        self.tela_frame.destroy()
        
        # FRAME PRINCIPAL RAÇAS
        self.frame_raças = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_raças.place(x = 0, y = 0)
        
        # BACKGROUND IMAGE
        self.background_homepage = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_homepage = ctk.CTkLabel(self.frame_raças,text= None, image= self.background_homepage)
        self.label_homepage.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_raças, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)
        
        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_raças, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_raças, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_raças, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_raças, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO HUMANO
        self.humano = PhotoImage(file="imagens/raças/HUMANO.png")
        self.botao_humano = Button(self.frame_raças, text=None, image=self.humano, highlightthickness=0, bd=0, command=self.tela_humano)
        self.botao_humano.place(x=350, y=130)

        #BOTÃO ANÃO
        self.anao = PhotoImage(file="imagens/raças/ANÃO.png")
        self.botao_anao = Button(self.frame_raças, text=None, image=self.anao, highlightthickness=0, bd=0, command=self.tela_anao)
        self.botao_anao.place(x=660, y=130)

        #BOTÃO HALFLING
        self.half = PhotoImage(file="imagens/raças/HALFLING.png")
        self.botao_half = Button(self.frame_raças, text=None, image=self.half, highlightthickness=0, bd=0, command=self.tela_halfling)
        self.botao_half.place(x=970, y=130)

        #BOTÃO ELFO
        self.elfo = PhotoImage(file="imagens/raças/ELFO.png")
        self.botao_elfo = Button(self.frame_raças, text=None, image=self.elfo, highlightthickness=0, bd=0, command=self.tela_elfo)
        self.botao_elfo.place(x=1280, y=130)

        #BOTÃO DRACONATO
        self.draco = PhotoImage(file="imagens/raças/DRACONATO.png")
        self.botao_draco = Button(self.frame_raças, text=None, image=self.draco, highlightthickness=0, bd=0, command=self.tela_draco)
        self.botao_draco.place(x=1590, y=130)

        #BOTÃO GNOMO
        self.gnomo = PhotoImage(file="imagens/raças/GNOMO.png")
        self.botao_gnomo = Button(self.frame_raças, text=None, image=self.gnomo, highlightthickness=0, bd=0, command=self.tela_gnomo)
        self.botao_gnomo.place(x=350, y=400)
        
        #BOTÃO MEIO ELFO
        self.meio_elfo = PhotoImage(file="imagens/raças/MEIO-ELFO.png")
        self.botao_meio_elfo = Button(self.frame_raças, text=None, image=self.meio_elfo, highlightthickness=0, bd=0, command=self.tela_meio_elfo)
        self.botao_meio_elfo.place(x=660, y=400)
        
        #BOTÃO MEIO ORC
        self.meio_orc = PhotoImage(file="imagens/raças/MEIO-ORC.png")
        self.botao_meio_orc = Button(self.frame_raças, text=None, image=self.meio_orc, highlightthickness=0, bd=0, command=self.tela_meio_orc)
        self.botao_meio_orc.place(x=970, y=400)

        #BOTÃO TIEFLIG
        self.tiefling = PhotoImage(file="imagens/raças/TIEFLING.png")
        self.botao_tiefling = Button(self.frame_raças, text=None, image=self.tiefling, highlightthickness=0, bd=0, command=self.tela_tiefling)
        self.botao_tiefling.place(x=1280, y=400)


    def tela_humano(self):
        self.tela_frame.destroy()

        self.frame_humano = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_humano.place(x = 0, y = 0)

        self.background_humano = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_humano = ctk.CTkLabel(self.frame_humano,text= None, image= self.background_homepage)
        self.label_humano.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_humano, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)

        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_humano, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_humano, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_humano, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_humano, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_humano, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.raças)
        self.botao_retornar.place(x=1810, y=0)

        self.maior_humano = PhotoImage(file ="imagens/Telas raças/Tela humano/HUMANO.png")
        self.label_maior_humano = ctk.CTkLabel(self.frame_humano,text= None, image= self.maior_humano)
        self.label_maior_humano.place(x= 270, y = 110)

        self.texto_humano = PhotoImage(file ="imagens/Telas raças/Tela humano/Texto humano.png")
        self.label_texto_humano = ctk.CTkLabel(self.frame_humano,text= None, image= self.texto_humano)
        self.label_texto_humano.place(x= 670, y = 30)

        self.texto_humano2 = PhotoImage(file ="imagens/Telas raças/Tela humano/Texto humano 2.png")
        self.label_texto_humano2 = ctk.CTkLabel(self.frame_humano,text= None, image= self.texto_humano2)
        self.label_texto_humano2.place(x= 665 , y = 430)

    def tela_anao(self):
        self.tela_frame.destroy()

        self.frame_anao = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_anao.place(x = 0, y = 0)

        self.background_anao = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_anao = ctk.CTkLabel(self.frame_anao,text= None, image= self.background_homepage)
        self.label_anao.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_anao, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)

        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_anao, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_anao, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_anao, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_anao, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_anao, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.raças)
        self.botao_retornar.place(x=1810, y=0)

        self.maior_anao = PhotoImage(file ="imagens/Telas raças/Tela anão/ANÃO.png")
        self.label_maior_anao = ctk.CTkLabel(self.frame_anao,text= None, image= self.maior_anao)
        self.label_maior_anao.place(x= 270, y = 110)

        self.texto_anao = PhotoImage(file ="imagens/Telas raças/Tela anão/Texto anão.png")
        self.label_texto_anao = ctk.CTkLabel(self.frame_anao,text= None, image= self.texto_anao)
        self.label_texto_anao.place(x= 670, y = 30)

        self.texto_anao2 = PhotoImage(file ="imagens/Telas raças/Tela anão/Texto anão 2.png")
        self.label_texto_anao2 = ctk.CTkLabel(self.frame_anao,text= None, image= self.texto_anao2)
        self.label_texto_anao2.place(x= 665 , y = 430)

        self.texto_anao3 = PhotoImage(file ="imagens/Telas raças/Tela anão/Texto anão 3.png")
        self.label_texto_anao3 = ctk.CTkLabel(self.frame_anao,text= None, image= self.texto_anao3)
        self.label_texto_anao3.place(x= 270, y = 470)


    def tela_halfling(self):
        self.tela_frame.destroy()

        self.frame_half = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_half.place(x = 0, y = 0)

        self.background_half = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_half = ctk.CTkLabel(self.frame_half,text= None, image= self.background_homepage)
        self.label_half.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_half, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)

        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_half, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_half, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_half, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_half, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_half, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.raças)
        self.botao_retornar.place(x=1810, y=0)

        self.maior_half = PhotoImage(file ="imagens/Telas raças/Tela Halfling/HALFLING.png")
        self.label_maior_half = ctk.CTkLabel(self.frame_half,text= None, image= self.maior_half)
        self.label_maior_half.place(x= 270, y = 110)

        self.texto_half = PhotoImage(file ="imagens/Telas raças/Tela halfling/Texto halfling.png")
        self.label_texto_half = ctk.CTkLabel(self.frame_half,text= None, image= self.texto_half)
        self.label_texto_half.place(x= 670, y = 30)

        self.texto_half2 = PhotoImage(file ="imagens/Telas raças/Tela halfling/Texto halfling 2.png")
        self.label_texto_half2 = ctk.CTkLabel(self.frame_half,text= None, image= self.texto_half2)
        self.label_texto_half2.place(x= 665 , y = 430)

        self.texto_half3 = PhotoImage(file ="imagens/Telas raças/Tela halfling/Texto halfling 3.png")
        self.label_texto_half3 = ctk.CTkLabel(self.frame_half,text= None, image= self.texto_half3)
        self.label_texto_half3.place(x= 270, y = 470)

    def tela_elfo(self):
        self.tela_frame.destroy()

        self.frame_elfo = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_elfo.place(x = 0, y = 0)

        self.background_elfo = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_elfo = ctk.CTkLabel(self.frame_elfo,text= None, image= self.background_homepage)
        self.label_elfo.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_elfo, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)

        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_elfo, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_elfo, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_elfo, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_elfo, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_elfo, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.raças)
        self.botao_retornar.place(x=1810, y=0)

        self.maior_elfo = PhotoImage(file ="imagens/Telas raças/Tela elfo/ELFO.png")
        self.label_maior_elfo = ctk.CTkLabel(self.frame_elfo,text= None, image= self.maior_elfo)
        self.label_maior_elfo.place(x= 270, y = 110)

        self.texto_elfo = PhotoImage(file ="imagens/Telas raças/Tela elfo/Texto elfo.png")
        self.label_texto_elfo = ctk.CTkLabel(self.frame_elfo,text= None, image= self.texto_elfo)
        self.label_texto_elfo.place(x= 670, y = 30)

        self.texto_elfo2 = PhotoImage(file ="imagens/Telas raças/Tela elfo/Texto elfo 2.png")
        self.label_texto_elfo2 = ctk.CTkLabel(self.frame_elfo,text= None, image= self.texto_elfo2)
        self.label_texto_elfo2.place(x= 665 , y = 430)

        self.texto_elfo3 = PhotoImage(file ="imagens/Telas raças/Tela elfo/Texto elfo 3.png")
        self.label_texto_elfo3 = ctk.CTkLabel(self.frame_elfo,text= None, image= self.texto_elfo3)
        self.label_texto_elfo3.place(x= 270, y = 470)

    def tela_draco(self):
        self.tela_frame.destroy()

        self.frame_draco = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_draco.place(x = 0, y = 0)

        self.background_draco = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_draco = ctk.CTkLabel(self.frame_draco,text= None, image= self.background_homepage)
        self.label_draco.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_draco, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)

        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_draco, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_draco, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_draco, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_draco, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_draco, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.raças)
        self.botao_retornar.place(x=1810, y=0)

        self.maior_draco = PhotoImage(file ="imagens/Telas raças/Tela draconato/DRACONATO.png")
        self.label_maior_draco = ctk.CTkLabel(self.frame_draco,text= None, image= self.maior_draco)
        self.label_maior_draco.place(x= 270, y = 110)

        self.texto_draco = PhotoImage(file ="imagens/Telas raças/Tela draconato/Texto draco.png")
        self.label_texto_draco = ctk.CTkLabel(self.frame_draco,text= None, image= self.texto_draco)
        self.label_texto_draco.place(x= 670, y = 50)

        self.texto_draco2 = PhotoImage(file ="imagens/Telas raças/Tela draconato/Texto draco 2.png")
        self.label_texto_draco2 = ctk.CTkLabel(self.frame_draco,text= None, image= self.texto_draco2)
        self.label_texto_draco2.place(x= 665 , y = 450)

        self.texto_draco3 = PhotoImage(file ="imagens/Telas raças/Tela draconato/Texto draco 3.png")
        self.label_texto_draco3 = ctk.CTkLabel(self.frame_draco,text= None, image= self.texto_draco3)
        self.label_texto_draco3.place(x= 270, y = 470)

        self.imagem_dragao = PhotoImage(file="imagens/Telas raças/Tela draconato/botao dragao.png")
        self.botao_dragao = Button(self.frame_draco, text=None, image=self.imagem_dragao, bd=0, highlightthickness=0, command=self.tabela_dragoes)
        self.botao_dragao.place(x=414, y=854)


    def tabela_dragoes(self):
        nova_janela = Toplevel(self.frame_draco)
        nova_janela.title("Tabela dos Dragões")

        tabela = PhotoImage(file="imagens/Telas raças/Tela draconato/Tabela draco.png")
        rotulo_tabela = Label(nova_janela, image=tabela)
        rotulo_tabela.pack()

        rotulo_tabela.image = tabela

    def tela_gnomo(self):
        self.tela_frame.destroy()

        self.frame_gnomo = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_gnomo.place(x = 0, y = 0)

        self.background_gnomo = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_gnomo = ctk.CTkLabel(self.frame_gnomo,text= None, image= self.background_homepage)
        self.label_gnomo.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_gnomo, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)

        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_gnomo, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_gnomo, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_gnomo, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_gnomo, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_gnomo, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.raças)
        self.botao_retornar.place(x=1810, y=0)

        self.maior_gnomo = PhotoImage(file ="imagens/Telas raças/Tela gnomo/GNOMO.png")
        self.label_maior_gnomo = ctk.CTkLabel(self.frame_gnomo,text= None, image= self.maior_gnomo)
        self.label_maior_gnomo.place(x= 270, y = 110)

        self.texto_gnomo = PhotoImage(file ="imagens/Telas raças/Tela gnomo/Tela gnomo.png")
        self.label_texto_gnomo = ctk.CTkLabel(self.frame_gnomo,text= None, image= self.texto_gnomo)
        self.label_texto_gnomo.place(x= 670, y = 30)

        self.texto_gnomo2 = PhotoImage(file ="imagens/Telas raças/Tela gnomo/Tela gnomo 2.png")
        self.label_texto_gnomo2 = ctk.CTkLabel(self.frame_gnomo,text= None, image= self.texto_gnomo2)
        self.label_texto_gnomo2.place(x= 660 , y = 565)

        self.texto_gnomo3 = PhotoImage(file ="imagens/Telas raças/Tela gnomo/Tela gnomo 3.png")
        self.label_texto_gnomo3 = ctk.CTkLabel(self.frame_gnomo,text= None, image= self.texto_gnomo3)
        self.label_texto_gnomo3.place(x= 270, y = 470)


    def tela_meio_elfo(self):
        self.tela_frame.destroy()

        self.frame_meioelfo = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_meioelfo.place(x = 0, y = 0)

        self.background_meioelfo = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_meioelfo = ctk.CTkLabel(self.frame_meioelfo,text= None, image= self.background_homepage)
        self.label_meioelfo.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_meioelfo, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)

        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_meioelfo, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_meioelfo, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_meioelfo, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO SELEÇÃO
        self.seleçao = PhotoImage(file="imagens/seleção.png")
        self.botao_seleçao = Button(self.frame_meioelfo, text=None, image=self.seleçao, highlightthickness=0, bd=0)
        self.botao_seleçao.place(x=280, y=0)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_meioelfo, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.raças)
        self.botao_retornar.place(x=1810, y=0)

        self.maior_meioelfo = PhotoImage(file ="imagens/Telas raças/Tela meio-elfo/MEIO ELFO.png")
        self.label_maior_meioelfo = ctk.CTkLabel(self.frame_meioelfo,text= None, image= self.maior_meioelfo)
        self.label_maior_meioelfo.place(x= 270, y = 110)

        self.texto_meioelfo = PhotoImage(file ="imagens/Telas raças/Tela meio-elfo/Texto meioelfo.png")
        self.label_texto_meioelfo = ctk.CTkLabel(self.frame_meioelfo,text= None, image= self.texto_meioelfo)
        self.label_texto_meioelfo.place(x= 670, y = 30)

        self.texto_meioelfo2 = PhotoImage(file ="imagens/Telas raças/Tela meio-elfo/Texto meioelfo 2.png")
        self.label_texto_meioelfo2 = ctk.CTkLabel(self.frame_meioelfo,text= None, image= self.texto_meioelfo2)
        self.label_texto_meioelfo2.place(x= 665 , y = 490)

        self.texto_meioelfo3 = PhotoImage(file ="imagens/Telas raças/Tela meio-elfo/Texto meioelfo 3.png")
        self.label_texto_meioelfo3 = ctk.CTkLabel(self.frame_meioelfo,text= None, image= self.texto_meioelfo3)
        self.label_texto_meioelfo3.place(x= 270, y = 470)

    def tela_meio_orc(self):
        self.tela_frame.destroy()

        self.frame_meioorc = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_meioorc.place(x = 0, y = 0)

        self.background_meioorc = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_meioorc = ctk.CTkLabel(self.frame_meioorc,text= None, image= self.background_homepage)
        self.label_meioorc.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_meioorc, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)

        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_meioorc, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_meioorc, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_meioorc, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_meioorc, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.raças)
        self.botao_retornar.place(x=1810, y=0)

        self.maior_meioorc = PhotoImage(file ="imagens/Telas raças/Tela meio-orc/MEIO ORC.png")
        self.label_maior_meioorc = ctk.CTkLabel(self.frame_meioorc,text= None, image= self.maior_meioorc)
        self.label_maior_meioorc.place(x= 270, y = 30)

        self.texto_meioorc = PhotoImage(file ="imagens/Telas raças/Tela meio-orc/meioorc texto.png")
        self.label_texto_meioorc = ctk.CTkLabel(self.frame_meioorc,text= None, image= self.texto_meioorc)
        self.label_texto_meioorc.place(x= 670, y = 30)

        self.texto_meioorc2 = PhotoImage(file ="imagens/Telas raças/Tela meio-orc/meioorc texto 2.png")
        self.label_texto_meioorc2 = ctk.CTkLabel(self.frame_meioorc,text= None, image= self.texto_meioorc2)
        self.label_texto_meioorc2.place(x= 665 , y = 490)

        self.texto_meioorc3 = PhotoImage(file ="imagens/Telas raças/Tela meio-orc/meioorc texto 3.png")
        self.label_texto_meioorc3 = ctk.CTkLabel(self.frame_meioorc,text= None, image= self.texto_meioorc3)
        self.label_texto_meioorc3.place(x= 270, y = 370)


    def tela_tiefling(self):
        self.tela_frame.destroy()

        self.frame_tiefling = ctk.CTkEntry(self, width= 1920, height= 1080)
        self.frame_tiefling.place(x = 0, y = 0)

        self.background_meioorc = PhotoImage(file ="imagens\HOMEPAGE.png")
        self.label_meioorc = ctk.CTkLabel(self.frame_tiefling,text= None, image= self.background_homepage)
        self.label_meioorc.place(x= 0, y = 0)

        #BOTÃO MENU
        self.imagem_menu = PhotoImage(file="imagens/menu.png")
        self.botao_menu = Button(self.frame_tiefling, text=None, image=self.imagem_menu, bd=0, highlightthickness=0, command=self.menu)
        self.botao_menu.place(x=0, y=125)

        #BOTÃO CRIAR PERSONAGEM
        self.criar = PhotoImage(file="imagens/Criar personagem.png")
        self.botao_criar = Button(self.frame_tiefling, text=None, image=self.criar, bd=0, highlightthickness=0)
        self.botao_criar.place(x=0, y=200)

        #BOTÃO MEUS PERSONAGENS
        self.personagens = PhotoImage(file="imagens/Meus personagens.png")
        self.botao_personagens = Button(self.frame_tiefling, text=None, image=self.personagens, bd=0, highlightthickness=0)
        self.botao_personagens.place(x=0, y=275)

        #BOTÃO MINHA CONTA
        self.m_conta = PhotoImage(file="imagens/Minha conta.png")
        self.botao_m_conta = Button(self.frame_tiefling, text=None, image=self.m_conta, bd=0, highlightthickness=0)
        self.botao_m_conta.place(x=0, y=920)

        #BOTÃO RETORNAR
        self.retornar = PhotoImage(file="imagens/retornar.png")
        self.botao_retornar = Button(self.frame_tiefling, text=None, image=self.retornar, highlightthickness=0, bd=0, command=self.raças)
        self.botao_retornar.place(x=1810, y=0)

        self.maior_tiefling = PhotoImage(file ="imagens/Telas raças/Tela tiefling/TIEFLING.png")
        self.label_maior_tiefling = ctk.CTkLabel(self.frame_tiefling,text= None, image= self.maior_tiefling)
        self.label_maior_tiefling.place(x= 270, y = 30)

        self.texto_tiefling = PhotoImage(file ="imagens/Telas raças/Tela tiefling/tiefling texto.png")
        self.label_texto_tiefling = ctk.CTkLabel(self.frame_tiefling,text= None, image= self.texto_tiefling)
        self.label_texto_tiefling.place(x= 670, y = 100)

        self.texto_tiefling2 = PhotoImage(file ="imagens/Telas raças/Tela tiefling/tiefling texto 2.png")
        self.label_texto_tiefling2 = ctk.CTkLabel(self.frame_tiefling,text= None, image= self.texto_tiefling2)
        self.label_texto_tiefling2.place(x= 665 , y = 470)

        self.texto_tiefling3 = PhotoImage(file ="imagens/Telas raças/Tela tiefling/tiefling texto 3.png")
        self.label_texto_tiefling3 = ctk.CTkLabel(self.frame_tiefling,text= None, image= self.texto_tiefling3)
        self.label_texto_tiefling3.place(x= 270, y = 400)















        

    def voltar_login(self):
        self.registro_frame.place_forget()
        self.tela_login()
    def limpar_entry_cadastro(self):
        self.cadastro_user.delete(0, END)
        self.cadastro_senha.delete(0, END)
        self.confirmar_senha.delete(0, END)
        self.cadastro_user.delete(0, END)
    def limpar_entry_login(self):
        self.user.delete(0, END)
        self.senha.delete(0, END)
if __name__ == "__main__":
    app = App()
    app.mainloop()


encoding="utf-8"
from rich. console import Console
from rich.table import Table
from time import sleep
from datetime import datetime
import json

console = Console()
class Functions():
    def __init__(self):
        self.outcome = self.openread("despesa.json")
        self.income = self.openread("receita.json")
        
    def bemvindo(self):
        table = Table(title="💰Sistema Financeiro Drax - Bem-vindo💰") #Cria a tabela com um titulo
        
        table.add_column("Opção", justify="center") #Adiciona coluna
        table.add_column("Descrição", justify="center")
        
        table.add_row("1","Despesas", style="red") #Adiciona fileira
        table.add_row("2", "Ganhos", style="green")
        table.add_row("3", "Ver balanço geral", style="blue")
        table.add_row("4", "Busca avançada", style="purple")
        table.add_row("5", "Limpar tudo", style="red")
        console.print(table) # Printa a mensagem de boas vindas!
        
        useropt = input('')
        while useropt not in ["1", "2", "3", "4", "5"]: #Verifica se o usuario escolheu umao opção válida.
            useropt = console.input('[red]Opção Inválida, tente novamente!:[red/] ')

        if useropt == "1": #Se o user escolheu Despesas
            self.generalmenu(name="Despesa(s)")

        elif useropt == "2":
            self.generalmenu(name="Ganho(s)")
              
        elif useropt == "3":
            self.general_balance()
        
        elif useropt == "4":
            self.datefilter()
        
        elif useropt == "5":
            self.removeall()
    
    def removeall(self): #Apaga completamente todas as listas do sistema.
        confirm = console.input("Você tem certeza que vai excluir todas as listas!? (S/N):   ").capitalize()
        while confirm not in ["S","N"]:
            self.removeall()
        if confirm == "S":
            vazio = []
            self.save("despesa.json", vazio)
            self.save("receita.json", vazio)
            self.outcome = vazio
            self.income = vazio
            
        else:
            console.print("Ação cancelada, Voltando ao menu...")
        return
    
    def prodtable(self,filename,color = "white"): #Tabela geral dos produtos.
        maintable = Table(title="")
        maintable.add_column("Opção", justify="center")
        maintable.add_column("Produto", justify="center")
        maintable.add_column("Valor", justify="center")
        total = 0
        cont = 0

        dados = self.openread(filename)
        for item in dados:
            total += item["Valor"]
            
        for item in dados:
            cont += 1
            maintable.add_row(f"{cont}", f"{item["Nome"]}", f"{item["Valor"]} R$")
        maintable.add_row("", "", "")
        maintable.add_row("Total", "Total", f"{total:.2f} R$")
            
        
        console.print(maintable, style= color)  
    
    def general_balance(self): # função q mostra o balanço geral.
        outtotal = 0
        intotal = 0
        finaltotal = 0
        for item in self.outcome:
            outtotal += item["Valor"]
        for item in self.income:
            intotal += item["Valor"]
        finaltotal = intotal - outtotal
            
        table = Table(title="Sistema financeiro drax")
        table.add_column("Nome")
        table.add_column("Valor")
        
        table.add_row("Entrada total", f"{intotal:.2f}", style="green")
        table.add_row("Saida total", f"{outtotal:.2f}", style="red")
        table.add_row("Saldo final", f"{finaltotal:.2f}", style="blue")
        
        
        console.print(table)
        sleep(3)
        self.bemvindo()
    
    
    def generalmenu(self, name): #Menu de escolhas - Despesas
            despmenu = Table(title="")
            despmenu.add_column("Opção", justify="center")
            despmenu.add_column("Descrição", justify="center")
            despmenu.add_row("1", f"Adicionar {name}")
            despmenu.add_row("2", f"Listar {name}")
            despmenu.add_row("3", f"Remover {name}")
            despmenu.add_row("4","Sair" )
            console.print(despmenu) #printa a tabela.
            
            answer = input('Digite a opção desejada: ')
            while answer not in ["1", "2", "3", "4"]:
                answer = console.input('[red]Opção Inválida! Digite novamente: [red/] ')
            
            if answer == "1": #Se o user escolheu adicionar uma nova despesa.
                if name == "Despesa(s)":
                    self.addnew(filename = "despesa.json", name = "Despesas(s)", color ="red")
                elif name == "Ganho(s)":
                    self.addnew(filename = "receita.json", name = "Receita(s)", color="green")
                
            elif answer == "2":
                if name == "Despesa(s)":
                    self.list(filename = "despesa.json")
                elif name == "Ganho(s)":
                    self.list(filename = "receita.json")
            elif answer == "3":
                if name == "Despesa(s)":
                    self.remove(filename = "despesa.json", name="Despesa(s)", color="red")
                elif name == "Ganho(s)":
                    self.remove(filename = "receita.json", name="Ganho(s)", color="green")
            
                
            elif answer == "4":
                console.print("[red]Saindo...[red/]")
                sleep(2)
                exit()
            
            
    #Função que funciona tanto para adicionar receitas quanto para despesas.            
    def addnew(self, filename, name, color): #Adiciona uma nova despesa.
        
        nameout = console.input(f"[{color}]Qual o nome da {name}?:[/{color}] ").capitalize()
        nameout = self.duplicated(filename, nameout)
        
        valueout = 0
        while True:
            try:
                valueout = float(console.input(f"[{color}]Qual o valor da {name}: {nameout}?: [/{color}]"))
                break
            except ValueError:
                print("Valor inválido, por favor digite um valor válido apenas com números!")
            
            if valueout.is_integer() == True:
                valueout = int(valueout)
            else:
                valueout = float(valueout)
            
        
        dados = self.openread(filename)
        self.outcome = dados
        newout = {"Nome": nameout, 
                  "Valor": valueout, 
                  "Data": datetime.now().strftime("%d/%m/%Y")} 
        dados.append(newout)
        
        self.save(filename, dados)
        
    def list(self, filename): # Função que lista as despesas.
        if filename == "receita.json":
            color ="green"
        elif filename == "despesa.json":
            color = "red"
        self.prodtable(filename, color)
        sleep(3)
        
    def remove(self, filename, name, color): # Função que remove as despesas ou receitas.
        self.prodtable(filename, color)
        cont = 0
        for item in self.outcome: #Conta a quantidade de itens válidos.
            cont += 1
        while True:
            try:
                option = int(console.input(f"[{color}]Digite o número equivalente a {name} a ser removida:[/{color}] "))
                break
            except ValueError:
                console.print("[red]Opção inválida tente novamente!:[/red]")
        
        while option > cont:
            option = int(input("[red]Opção Inválida tente novamente!: [/red]"))
        dados = self.openread(filename)
        dados.pop(option - 1)
            
        self.save(filename, dados = dados)
        self.prodtable(filename)
        sleep(3)
    
    def datefilter(self):
        filename = ""
        name = ''
        while True:
            method = input("Você quer pesquisar as despesas, receitas ou ambas?: (1- Despesas 2- Receitas 3- Ambas)")
            if method == "1":
                filename = "despesa.json"
                name = "Despesa(s)"
                break
            elif method == "2":
                filename = "receita.json"
                name = "Receitas(s)"
                break
            elif method == "3":
                print("Sistema em manutenção!!")
                self.datefilter()
                break
            else:
                console.print("[red]Opção inválida tente novamente!: [/red]")
        dados1 = self.openread(filename)
        for i in dados1:
            i["Data"] = datetime.strptime(i["Data"], "%d/%m/%Y")
        while True:    
            userchoice = input("Digite o dia, ano ou mês que deseja buscar Exemplo: 08/04/2026:  \nou Digite X caso queira sair: ")
            
            if userchoice in ["x", "X"]:
                self.bemvindo()
            try:
                userchoice = datetime.strptime(userchoice, "%d/%m/%Y")
            except ValueError:
                if "/" in userchoice:
                    userchoice = userchoice.replace("/", "")
                    print(userchoice)
                    for i in dados1:
                        if i["Data"].day == int(userchoice[:2]) and i["Data"].month == int(userchoice[2:5]):
                            console.print(f"[red]Nome: {i["Nome"]} | Valor: {i["Valor"]} | Data: {i["Data"].strftime("%d/%m/%Y")}[red/]")
                            break
                else:
                    console.print(f"Buscando por {name}...")
                    for i in dados1:
                        sleep(2)
                        if i["Data"].day == int(userchoice):
                            console.print(f"[red]Nome: {i["Nome"]} | Valor: {i["Valor"]} | Data: {i["Data"].strftime("%d/%m/%Y")}[red/]")
                            found = True
                            break
            console.print(f"[red]Nenhuma {name} encontrada![/red]")
            

    def duplicated(self,filename, nameout):
            dados = self.openread(filename)
            while any(e["Nome"] == nameout for e in dados):    
                nameout = console.input("O nome já está na lista!. Escolha outro nome!: ").capitalize()
            return nameout
            
                
            
                    
                        
                      
    def openread(self, filename): 
        try:
            with open(filename, "r", encoding="utf-8") as f:
                dados = json.load(f)
                if not isinstance(dados, list):
                    dados = [] 
                return dados   
        except (FileNotFoundError, json.JSONDecodeError):
            return []
            
        
    
    def save(self, filename, dados): #Salva a modificação feita na memória do programa. (O dados é um placeholder pro "vazio" da função removeall.)
            with open(filename, "w", encoding="utf-8" ) as f:
                json.dump(dados, f)
            
        
    

    
            
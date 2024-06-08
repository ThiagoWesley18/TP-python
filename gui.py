import os
import tkinter as tk
import matplotlib
import pandas as pd

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

class App(tk.Tk):
    def __init__(self, dados):
        super().__init__()

        self.title('Desemprego IBGE')
        self.dados = dados
        self.last_modified = os.path.getmtime('dadosBD.csv') # Pega o tempo da última modificação do arquivo
        self.after(1000, self.check_file) # Verifica se o arquivo foi modificado a cada 1 segundo e chama o método check_file
        self.create_widgets() # Cria os widgets da aplicação

    # Método para limpar os widgets da aplicação
    def clear_widgets(self):
        # Destroi todos os widgets filhos do frame principal da aplicação
        for widget in self.winfo_children():
            widget.destroy()

    # Método para criar os widgets da aplicação
    def create_widgets(self):
        # Cria um dicionário com os dados que serão plotados
        data = {
            "Taxa de desemprego": self.dados.iloc[0,0],
            "Taxa de Subtilização": self.dados.iloc[0,3]
        }
        indices = data.keys()
        valores = data.values()

        # Cria uma nova area de plotagem para o gráfico
        figure = Figure(figsize=(6, 4), dpi=100)

        # Adiciona um subplot ao gráfico para plotar o gráfico de barras
        figure_canvas = FigureCanvasTkAgg(figure, self)

        # Cria a barra de ferramentas
        NavigationToolbar2Tk(figure_canvas, self)

        # Cria um subplot para o gráfico
        axes = figure.add_subplot()

        # Plota o gráfico
        axes.bar(indices, valores)
        axes.set_title('Desemprego x Subtilização')
        axes.set_ylabel('Porcentagem (%)')
        axes.set_ymargin(0.1)

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Cria um frame para exibir os dados da tabela
        frame = tk.Frame(self)
        frame.pack()

        total_rows = self.dados.shape[0] 
        total_columns = self.dados.shape[1] 
        column_labels = ["Desempregados (Milhões)", "Taxa de Desemprego (%)", "Ocupados (Milhões)", "Taxa de Subtilização (%)"]

        # Cria os rótulos das colunas
        for j in range(total_columns):
            label = tk.Label(frame, text=column_labels[j], font=('Arial', 10, 'bold'))
            label.grid(row=0, column=j)

        # Cria as entradas com os dados do DataFrame
        for i in range(total_rows): 
            for j in range(total_columns): 
                e = tk.Entry(frame, width=20, fg='blue', font=('Arial',10)) 
                e.grid(row=i+1, column=j)  
                e.insert(tk.END, str(self.dados.iloc[i,j])) 
    
    # Método para verificar se o arquivo foi modificado
    def check_file(self):
        current_time = os.path.getmtime('dadosBD.csv') # Pega o tempo da última modificação do arquivo
        if current_time != self.last_modified:
            self.last_modified = current_time
            self.dados = pd.read_csv('dadosBD.csv')
            self.clear_widgets() # Limpa os widgets da aplicação
            self.create_widgets() # Cria os widgets da aplicação
        self.after(1000, self.check_file) # Chama o método check_file a cada 1 segundo 

if __name__ == '__main__':
    # Criando um DataFrame com os dados do arquivo teste.csv
    dados = pd.read_csv('dadosBD.csv')
    
    app = App(dados)
    app.mainloop()
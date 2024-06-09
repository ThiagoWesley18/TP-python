import tkinter as tk
import matplotlib
import pandas as pd
import sqlite3

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Desemprego IBGE')
        self.con = sqlite3.connect('desempregados.db')
        self.dados = pd.read_sql_query("SELECT * FROM desempregados", self.con)
        self.last_change_count = self.con.total_changes
        self.create_widgets() # Cria os widgets da aplicação
        self.check_update() # Verifica se a base de dados foi atualizada
        self.after(1000, self.check_update) # Verifica novamente após 1 segundo

    # Método para limpar os widgets da aplicação
    def clear_widgets(self):
        # Destroi todos os widgets filhos do frame principal da aplicação
        for widget in self.winfo_children():
            widget.destroy()

    # Método para criar os widgets da aplicação
    def create_widgets(self):
        # Cria um dicionário com os dados que serão plotados
        data = {
            "Taxa de desemprego": self.dados.iloc[1,2],
            "Taxa de Subtilização": self.dados.iloc[3,2]
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

        # Cria um Canvas
        canvas = tk.Canvas(self)
        canvas.pack(side=tk.LEFT, fill='both', expand=True)  # Alterado aqui

        # Cria uma barra de rolagem e a associa ao Canvas
        scrollbar = tk.Scrollbar(self, command=canvas.yview)
        scrollbar.pack(side=tk.LEFT, fill='y')  # Alterado aqui

        # Configura o Canvas para usar a barra de rolagem
        canvas.configure(yscrollcommand=scrollbar.set)

        # Cria um frame para exibir os dados da tabela e coloca dentro do Canvas
        frame = tk.Frame(canvas)
        canvas.create_window((0,0), window=frame, anchor='nw')

        # Atualiza a barra de rolagem para acompanhar o conteúdo do Canvas
        def update_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox('all'))

        frame.bind('<Configure>', update_scrollregion)

        total_rows = self.dados.shape[0] 
        total_columns = self.dados.shape[1] 
        column_labels = ["id", "Titulo", "Valor", "Periodo"]

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

    def fetch_data(self):
        self.con.close()
        self.con = sqlite3.connect('desempregados.db')
        self.dados = pd.read_sql_query("SELECT * FROM desempregados", self.con) 

    # Método para verificar se a base de dados foi atualizada
    def check_update(self):
        current_change_count = self.con.total_changes
        if current_change_count > self.last_change_count:
            self.fetch_data()
            print("A base de dados foi atualizada.")
            self.last_change_count = current_change_count
            self.clear_widgets() # Limpa os widgets da aplicação
            self.create_widgets() # Cria os widgets da aplicação 
        self.after(1000, self.check_update) # Verifica novamente após 1 segundo

if __name__ == '__main__':
   app = App()
   app.mainloop()
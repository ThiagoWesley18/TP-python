from urllib.request import urlopen
from html.parser import HTMLParser
import pandas as pd
import sqlite3

# parser para extrair dados da pagina web
class DesempregoParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.dados = []
        self.current_data = {}
        self.in_title = False   #flag para verificar a existencia do titulo
        self.in_value = False   #flag para verificar a existencia do valor
        self.in_period = False  #flag para verificar a existencia do periodo
        self.current_tag = None

    # lê e e faz o parse da tag inicial do dado
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag == 'h3' and ('class', 'variavel-titulo') in attrs:
            self.in_title = True
        elif tag == 'p' and ('class', 'variavel-dado') in attrs:
            self.in_value = True
        elif tag == 'p' and ('class', 'variavel-periodo') in attrs:
            self.in_period = True

    # lê e e faz o parse da tag que fecha a tag inicial
    def handle_endtag(self, tag):
        if tag == 'h3' and self.in_title:
            self.in_title = False
        elif tag == 'p' and self.in_value:
            self.in_value = False
        elif tag == 'p' and self.in_period:
            self.in_period = False

    # faz o parse dos dados que estão nas tags procuradas
    def handle_data(self, dados):
        if self.in_title:
            self.current_data['Titulo'] = dados.strip()
        elif self.in_value:
            self.current_data['Valor'] = dados.strip()
        elif self.in_period:
            self.current_data['Periodo'] = dados.strip()
            # Assuming that each 'variavel' has exactly one 'Title', 'Value', and 'Periodo'
            self.dados.append(self.current_data)
            self.current_data = {}



# Abre a pagina web, extrai o conteudo html e faz o parser
url = 'https://www.ibge.gov.br/explica/desemprego.php'
response = urlopen(url)
html_content = response.read().decode()
parser = DesempregoParser()
parser.feed(html_content)

# Organiza os dados em um dataFrame
df = pd.DataFrame(parser.dados)
print(df)

# Cria o banco de dados e conexão com ele
conn = sqlite3.connect('desempregados.db')
cur = conn.cursor()

# Cria tabela onde serão armazenados os dados
cur.execute('''
CREATE TABLE IF NOT EXISTS desempregados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Titulo TEXT,
    Valor TEXT,
    Periodo TEXT
)
''')

# Insere os dados na tabela
for index, linha in df.iterrows():
    cur.execute('''
    INSERT INTO desempregados (Titulo, Valor, Periodo)
    VALUES (?, ?, ?)
    ''', (linha['Titulo'], linha['Valor'], linha['Periodo']))

# Salva alterações e fecha conexão com o banco de dados
conn.commit()
conn.close()

print("Dados inseridos com sucesso")

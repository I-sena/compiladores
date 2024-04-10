import re

class Token:
    """Classe que representa um token"""
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __str__(self):
        return f"Token({self.tipo}, {self.valor})"

class AnalisadorLexico:
    palavra_reservada = ["fun","int", "char", "long", "short", "float", "double", "void",
                         "if", "else", "for", "do", "break", "continue",  "struct", "switch",
                         "case", "default", "return", "var",  "while", "print", "true", "false",
                         "nil", "this", "or", "and"]

    #             || ou && ou == ou != ou
    operadores = r"\|\||&&|==|!=|<|>|<=|>=|\+|-|\*|/|%|--|\+\+|->|!|\.|="

    #            ( ou ) ou [ ou ] ou { ou } ou ; ou ,
    delimitadores = r"\(|\)|\[|\]|\{|\}|;|,"

    #       começa com letra ou _ seguida de 0 ou + letras e/ou numeros, _
    identificadores = r'[a-zA-Z_][a-zA-Z0-9_]*\b'

    # pode ou nao ter sinal do numero mas deve ter um numero de  0-9
    inteiros = r'[+-]?\d+\b'

   # pode ou nao ter sinal do numero mas deve ter um numero de  0-9, ter que have rum . e tem que ter ao menos um digitos de 0-9
    ponto_flutuante = r'[+-]?\d+\.\d+'

    # Começa com " ou ', seguida de 0 ou mais ocorrencias de qualquer coisa que nao seja " ou ' deve ter no final " ou ' (identifica strings)
    constante_textual = r'["\'][^"\']*["\']'

    def __init__(self, arquivo):
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:

                # armazena o conteudo do arquivo lido na variavel 'conteudo'
                conteudo = f.read()

                # Remover linhas de comentario (procurar // seguidos de 0 ou mais caracteres menos \n esubstitui por espaço em branco)
                conteudo = re.sub('//.*', ' ', conteudo)

                # Remover linhas de comentario (procurar /* seguidos de 0 ou mais caracteres ou \n e substitui por espaço em branco)
                conteudo = re.sub('(/\*(.|\n)*?\*/)', ' ', conteudo)

                # Gera e identifica todos os tokens do arquivo
                self.tokens = self.tokenizar(conteudo)

                self.indice = 0
                self.token_atual = None

        except FileNotFoundError:
            print(f"Arquivo '{arquivo}' não encontrado.")

    def tokenizar(self, conteudo):
        """Separa as palavras do arquivo e retorna como uma lista com elas ja tokenizar com o tipo. Ex: identificar, operadores;"""

        # Cria um objeto que contem todas as possiveis formas de se ER
        regex = re.compile(
             r'\+|\d+[a-zA-Z_]*\b|[a-zA-Z_]+[a-zA-Z0-9_]*\b|["\'][^"\']*["\']|[+-]?\d+\.\d+|->|&&|\|\||\-\-|\+\+|[-+*/%&=!><\|]=?|[-+*/%&=!><\|]|\||\(|\)|\[|\]|\{|\}|\.|,|;')

        # Separa as palavras do arquivo de acordo com as regras acima
        valores_tokens = regex.findall(conteudo)

        # Pega cada palavra separada no arquivo e analisa se ela é um token valido da linguagem
        tokens = [self.obter_tipo_token(valor) for valor in valores_tokens]

        # Adiciona na lista de tokens o token de final do arquivo
        tokens.append(Token("Delimitador", "EOF"))

        return tokens

    def obter_tipo_token(self, valor):
        """Analisa um valor passado para saber se ele é um token da linguagem."""
        if valor in self.palavra_reservada:
            return Token("Palavra reservada", valor)
        elif re.match(self.operadores, valor):
            return Token("Operador", valor)
        elif re.match(self.inteiros, valor):
            return Token("Inteiro", valor)
        elif re.match(self.ponto_flutuante, valor):
            return Token("Ponto Flutuante", valor)
        elif valor in self.delimitadores:
            return Token("Delimitador", valor)
        elif re.match(self.identificadores, valor):
            return Token("Identificador", valor)
        elif re.match(self.constante_textual, valor):
            return Token("Constante Textual", valor)
        else:
            return Token("Desconhecido", valor)



    def printTokens(self):
        for token in self.tokens:
            if re.match(r'\d+[a-zA-Z_]+\b|[a-zA-Z_]+[™]\b', token.valor):
                token.tipo = "Erro Léxico"
                token.valor = f"Erro: token inválido {token.valor}"

            print(f"Tipo: {token.tipo } Valor: {token.valor}")
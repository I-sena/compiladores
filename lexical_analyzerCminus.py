import re

class Token:
    """Classe que representa um token"""
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __str__(self):
        return f"Token({self.tipo}, {self.valor})"

class AnalisadorLexico:
    """Classe responsavel por fazer a analise lexica."""

    palavra_reservada = ["else", "if", "int", "float", "char", "return", "void", "while", "for", "printf"]

    operadores = r"\|\||&&|==|!=|<|>|<=|>=|\+\+|-|\*|/|%|--|\+|!|\.|="

    delimitadores = r"\(|\)|\[|\]|\{|\}|;|,"

    identificadores = r'[a-zA-Z_][a-zA-Z0-9_]*\b'

    inteiros = r'[+-]?\d+\b'

    ponto_flutuante = r'[+-]?\d+\.\d+'

    constante_textual = r'["\'][^"\']*["\']'

    def __init__(self, arquivo):
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:

                conteudo = f.read()

                conteudo = re.sub(r'//.*', ' ', conteudo)

                conteudo = re.sub(r'(/\*(.|\n)*?\*/)', ' ', conteudo)

                self.tokens = self.tokenizar(conteudo)

        except FileNotFoundError:
            print(f"Arquivo '{arquivo}' não encontrado.")

    def tokenizar(self, conteudo):
        """Separa as palavras presentes no arquivo e retorna uma lista com elas separadas de acordo com as ER compiladas."""

        # Cria um objeto que contem todas as possiveis formas de ER
        regex = re.compile(
             r'\+\+|\d+[a-zA-Z_]*\b|[a-zA-Z_]+[a-zA-Z0-9_]*\b|["\'][^"\']*["\']|[+-]?\d+\.\d+|->|&&|\|\||\-\-|[-+*/%&=!><\|]=?|[-+*/%&=!><\|]|\||\(|\)|\[|\]|\{|\}|\.|,|;')

        # Separa as palavras do arquivo de acordo com as ER compiladas acima.
        valores_tokens = regex.findall(conteudo)

        # Pega cada palavra separada no arquivo e analisa se ela é um token valido da linguagem.
        tokens = [self.obter_tipo_token(valor) for valor in valores_tokens]

        # Adiciona na lista de tokens o token de final do arquivo.
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
        """Imprime os tipos e valores dos tokens encontradas no arquivo"""
        print(f"TIPO | VALOR")
        print(f":---------- | :----------")

        for token in self.tokens:
            if re.match(r'\d+[a-zA-Z_]+\b|[a-zA-Z_]+[™]\b', token.valor):
                token.tipo = "Erro Léxico"
                token.valor = f"Erro: token inválido {token.valor}"

            print(f"* Tipo: {str(token.tipo).ljust(25)} | Valor: {token.valor}  ")

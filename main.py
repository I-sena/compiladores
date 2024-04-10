from lexical_analyzerCminus import AnalisadorLexico

def main():
    arquivo = "exemplos/exemplo3.cm"

    analisador_lexico = AnalisadorLexico(arquivo)
    analisador_lexico.printTokens()

if __name__ == "__main__":
    main()





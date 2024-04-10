from lexical_analyzerCminus import AnalisadorLexico

def main():
    arquivo = "exemplos/exemplo.cm"

    analisador_lexico = AnalisadorLexico(arquivo)
    analisador_lexico.printTokens()

if __name__ == "__main__":
    main()





from analisador_lexico import analisador_lexico

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def token_atual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', '')

    def consumir(self, tipo_esperado):
        tipo, valor = self.token_atual()
        if tipo == tipo_esperado:
            self.pos += 1
            return valor
        raise SyntaxError(f"Esperado {tipo_esperado}, encontrado {tipo} ({valor})")

    def parse(self):
        self.cmd_list()
        print("Análise sintática concluída com sucesso!")

    def cmd_list(self):
        while self.token_atual()[0] in ['KEYWORD', 'ID']:
            self.cmd()

    def cmd(self):
        tipo, val = self.token_atual()

        if val == 'if':
            self.consumir('KEYWORD')  # if
            self.consumir('SYMBOL')   # (
            self.exp()
            self.consumir('SYMBOL')   # )
            self.bloco()
        elif val == 'while':
            self.consumir('KEYWORD')
            self.consumir('SYMBOL')
            self.exp()
            self.consumir('SYMBOL')
            self.bloco()
        elif val == 'for':
            self.consumir('KEYWORD')
            self.consumir('SYMBOL')  # (
            self.atribuicao()
            self.consumir('SYMBOL')  # ;
            self.exp()
            self.consumir('SYMBOL')  # ;
            self.atribuicao()
            self.consumir('SYMBOL')  # )
            self.bloco()
        elif val == 'return':
            self.consumir('KEYWORD')
            self.exp()
            self.consumir('SYMBOL')  # ;
        elif tipo == 'ID':
            self.atribuicao()
            self.consumir('SYMBOL')  # ;
        else:
            raise SyntaxError(f"Comando inválido: {val}")

    def atribuicao(self):
        self.consumir('ID')
        self.consumir('OP')  # espera "="
        self.exp()

    def exp(self):
        self.term()
        while self.token_atual()[1] in ['+', '-']:
            self.consumir('OP')
            self.term()

    def term(self):
        self.factor()
        while self.token_atual()[1] in ['*', '/']:
            self.consumir('OP')
            self.factor()

    def factor(self):
        tipo, val = self.token_atual()
        if tipo == 'NUMBER':
            self.consumir('NUMBER')
        elif tipo == 'ID':
            self.consumir('ID')
        elif val == '(':
            self.consumir('SYMBOL')
            self.exp()
            self.consumir('SYMBOL')
        else:
            raise SyntaxError(f"Fator inválido: {val}")

    def bloco(self):
        self.consumir('SYMBOL')  # {
        self.cmd_list()
        self.consumir('SYMBOL')  # }

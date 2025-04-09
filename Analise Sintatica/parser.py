import json
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
        ast = self.cmd_list()
        print(json.dumps(ast, indent=2))
        return ast

    def cmd_list(self):
        comandos = []
        while self.token_atual()[0] in ['KEYWORD', 'ID']:
            comandos.append(self.cmd())
        return {'type': 'CMD_LIST', 'body': comandos}

    def cmd(self):
        tipo, val = self.token_atual()

        if val == 'if':
            self.consumir('KEYWORD')
            self.consumir('SYMBOL')  
            cond = self.exp()
            self.consumir('SYMBOL') 
            bloco = self.bloco()
            return {'type': 'IF', 'cond': cond, 'body': bloco}

        elif val == 'while':
            self.consumir('KEYWORD')
            self.consumir('SYMBOL')
            cond = self.exp()
            self.consumir('SYMBOL')
            bloco = self.bloco()
            return {'type': 'WHILE', 'cond': cond, 'body': bloco}

        elif val == 'for':
            self.consumir('KEYWORD')
            self.consumir('SYMBOL')  
            init = self.atribuicao()
            self.consumir('SYMBOL')  
            cond = self.exp()
            self.consumir('SYMBOL')  
            update = self.atribuicao()
            self.consumir('SYMBOL')  
            bloco = self.bloco()
            return {'type': 'FOR', 'init': init, 'cond': cond, 'update': update, 'body': bloco}

        elif val == 'return':
            self.consumir('KEYWORD')
            expr = self.exp()
            self.consumir('SYMBOL')  
            return {'type': 'RETURN', 'value': expr}

        elif tipo == 'ID':
            atrib = self.atribuicao()
            self.consumir('SYMBOL')  
            return {'type': 'ASSIGN', **atrib}

        else:
            raise SyntaxError(f"Comando inválido: {val}")

    def atribuicao(self):
        var = self.consumir('ID')
        op = self.consumir('OP')  
        expr = self.exp()
        return {'var': var, 'op': op, 'value': expr}

    def exp(self):
        node = self.term()
        while self.token_atual()[1] in ['+', '-']:
            op = self.consumir('OP')
            right = self.term()
            node = {'type': 'BIN_OP', 'op': op, 'left': node, 'right': right}
        return node

    def term(self):
        node = self.factor()
        while self.token_atual()[1] in ['*', '/']:
            op = self.consumir('OP')
            right = self.factor()
            node = {'type': 'BIN_OP', 'op': op, 'left': node, 'right': right}
        return node

    def factor(self):
        tipo, val = self.token_atual()
        if tipo == 'NUMBER':
            self.consumir('NUMBER')
            return {'type': 'NUMBER', 'value': int(val)}
        elif tipo == 'ID':
            self.consumir('ID')
            return {'type': 'ID', 'name': val}
        elif val == '(':
            self.consumir('SYMBOL')
            expr = self.exp()
            self.consumir('SYMBOL')
            return expr
        else:
            raise SyntaxError(f"Fator inválido: {val}")

    def bloco(self):
        self.consumir('SYMBOL')  
        comandos = self.cmd_list()
        self.consumir('SYMBOL') 
        return comandos

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
        while self.token_atual()[0] in ['KEYWORD', 'ID'] or self.token_atual()[1] == 'func':  # Modificado para incluir 'func'
            comandos.append(self.cmd())
        return {'type': 'CMD_LIST', 'body': comandos}

    def cmd(self):
        tipo, val = self.token_atual()

        if val == 'if':
            self.consumir('KEYWORD')
            self.consumir('SYMBOL')  # (
            cond = self.exp()
            self.consumir('SYMBOL')  # )
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
            self.consumir('SYMBOL')  # (
            init = self.atribuicao()
            self.consumir('SYMBOL')  # ;
            cond = self.exp()
            self.consumir('SYMBOL')  # ;
            update = self.atribuicao()
            self.consumir('SYMBOL')  # )
            bloco = self.bloco()
            return {'type': 'FOR', 'init': init, 'cond': cond, 'update': update, 'body': bloco}

        elif val == 'return':
            self.consumir('KEYWORD')
            expr = self.exp()
            self.consumir('SYMBOL')  # ;
            return {'type': 'RETURN', 'value': expr}

        elif val == 'func':  # Alterado para reconhecer 'func' como palavra-chave
            self.consumir('KEYWORD')  # A palavra 'func' é uma KEYWORD
            nome = self.consumir('ID')
            self.consumir('SYMBOL')  # (
            params = self.param_list()
            self.consumir('SYMBOL')  # )
            body = self.bloco()
            return {'type': 'FUNC_DECL', 'name': nome, 'params': params, 'body': body}

        elif tipo == 'ID':
            lookahead = self.tokens[self.pos + 1][1] if self.pos + 1 < len(self.tokens) else ''
            if lookahead == '(':
                func_call = self.factor()
                self.consumir('SYMBOL')  # ;
                return {'type': 'FUNC_CALL_STMT', 'call': func_call}
            else:
                atrib = self.atribuicao()
                self.consumir('SYMBOL')  # ;
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
            nome = self.consumir('ID')
            if self.token_atual()[1] == '(':
                self.consumir('SYMBOL')
                args = self.arg_list()
                self.consumir('SYMBOL')
                return {'type': 'FUNC_CALL', 'name': nome, 'args': args}
            else:
                return {'type': 'ID', 'name': nome}
        elif val == '(':
            self.consumir('SYMBOL')
            expr = self.exp()
            self.consumir('SYMBOL')
            return expr
        else:
            raise SyntaxError(f"Fator inválido: {val}")

    def bloco(self):
        self.consumir('SYMBOL')  # {
        comandos = self.cmd_list()
        self.consumir('SYMBOL')  # }
        return comandos

    def param_list(self):
        params = []
        if self.token_atual()[0] == 'ID':
            params.append(self.consumir('ID'))
            while self.token_atual()[1] == ',':
                self.consumir('SYMBOL')
                params.append(self.consumir('ID'))
        return params

    def arg_list(self):
        args = []
        if self.token_atual()[0] != 'SYMBOL' or self.token_atual()[1] != ')':
            args.append(self.exp())
            while self.token_atual()[1] == ',':
                self.consumir('SYMBOL')
                args.append(self.exp())
        return args

import json
from analisador_lexico import analisador_lexico
from parser import Parser

class SymbolTableBuilder:
    def __init__(self):
        self.symbols = []
        self.scope_stack = ["global"]
        self.errors = []

    def current_scope(self):
        return "::".join(self.scope_stack)

    def add_symbol(self, name, tipo="variável", value=None):
        # Verifica se a variável ou função já foi declarada
        if self.symbol_exists(name):
            self.errors.append(f"Erro: {name} já foi declarado no escopo {self.current_scope()}")
        else:
            entry = {
                "nome": name,
                "tipo": tipo,
                "escopo": self.current_scope()
            }
            if value is not None:
                entry["valor"] = value
            self.symbols.append(entry)

    def symbol_exists(self, name):
        for simbolo in self.symbols:
            if simbolo["nome"] == name and simbolo["escopo"] == self.current_scope():
                return True
        return False

    def build(self, ast):
        self.visit(ast)
        return self.symbols

    def visit(self, node):
        node_type = node.get("type")

        if node_type == "CMD_LIST":
            for cmd in node["body"]:
                self.visit(cmd)

        elif node_type == "ASSIGN":
            var_name = node["var"]
            value_node = node["value"]
            value = self.extract_value(value_node)
            self.add_symbol(var_name, value=value)

        elif node_type == "RETURN":
            self.visit(node["value"])

        elif node_type == "FUNC_DECL":
            func_name = node["name"]
            self.add_symbol(func_name, tipo="função")
            self.scope_stack.append(func_name)  # Entra no escopo da função
            for param in node["params"]:
                self.add_symbol(param, tipo="variável")  # Parametro da função
            self.visit(node["body"])
            self.scope_stack.pop()  # Sai do escopo da função

        elif node_type in ["IF", "WHILE", "FOR"]:
            self.scope_stack.append(node_type.lower())  # Bloco de controle
            self.visit(node["cond"])
            self.visit(node["body"])
            self.scope_stack.pop()

        elif node_type == "BIN_OP":
            self.visit(node["left"])
            self.visit(node["right"])

        elif node_type == "ID":
            self.add_symbol(node["name"])

    def extract_value(self, node):
        if node["type"] == "NUMBER":
            return node["value"]
        return None


class AnalisadorSemantico:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def verificar(self, ast):
        self.visit(ast)

    def visit(self, node):
        node_type = node.get("type")

        if node_type == "CMD_LIST":
            for cmd in node["body"]:
                self.visit(cmd)

        elif node_type == "ASSIGN":
            var_name = node["var"]
            if not self.symbol_exists(var_name):
                self.symbol_table.errors.append(f"Erro semântico: Variável '{var_name}' não declarada")
            self.visit(node["value"])

        elif node_type == "RETURN":
            self.visit(node["value"])

        elif node_type == "FUNC_DECL":
            func_name = node["name"]
            self.check_function_return_type(func_name, node)
            self.visit(node["body"])

        elif node_type == "ID":
            if not self.symbol_exists(node["name"]):
                self.symbol_table.errors.append(f"Erro semântico: Variável ou função '{node['name']}' não declarada")

        elif node_type == "BIN_OP":
            self.visit(node["left"])
            self.visit(node["right"])

    def symbol_exists(self, name):
        for simbolo in self.symbol_table.symbols:
            if simbolo["nome"] == name:
                return True
        return False

    def check_function_return_type(self, func_name, node):
        # Verifica o tipo de retorno da função
        return_type = self.extract_type(node["body"])
        if return_type != "NUMBER" and return_type != "ID":
            self.symbol_table.errors.append(f"Erro semântico: Tipo de retorno esperado para '{func_name}' não corresponde")

    def extract_type(self, body):
        # Simples extração de tipo de retorno
        if body and body["type"] == "RETURN":
            return "ID"  # Para simplificar, trata tudo como ID
        return "UNKNOWN"

    def imprimir_erros(self):
        if self.symbol_table.errors:
            print("Erros encontrados:")
            for erro in self.symbol_table.errors:
                print(erro)
        else:
            print("Nenhum erro semântico encontrado.")



if __name__ == "__main__":
    codigo = '''
    func soma(a, b) {
        return a + b;
    }

    func identidade(x) {
        return x;
    }

    x = soma(3, 4);
    y = soma(10);
    z = soma(x, y);
    w = identidade(5);

    k = resultado + 1;  //
    '''

    tokens = analisador_lexico(codigo)
    parser = Parser(tokens)
    ast = parser.parse()

    # Geração da Tabela de Símbolos
    builder = SymbolTableBuilder()
    tabela_simbolos = builder.build(ast)

    # Verificação Semântica
    semantico = AnalisadorSemantico(builder)
    semantico.verificar(ast)
    semantico.imprimir_erros()

    # Imprimir Tabela de Símbolos
    print("\nTabela de símbolos:")
    for simbolo in tabela_simbolos:
        print(simbolo)

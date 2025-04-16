import json
from parser import Parser
from analisador_lexico import analisador_lexico

class SymbolTableBuilder:
    def __init__(self):
        self.symbols = []
        self.scope_stack = ["global"]

    def current_scope(self):
        return "::".join(self.scope_stack)

    def add_symbol(self, name, tipo="variável", value=None):
        entry = {
            "nome": name,
            "tipo": tipo,
            "escopo": self.current_scope()
        }
        if value is not None:
            entry["valor"] = value
        self.symbols.append(entry)

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

        elif node_type in ["IF", "WHILE"]:
            self.visit(node["cond"])
            self.scope_stack.append(node_type.lower())
            self.visit(node["body"])
            self.scope_stack.pop()

        elif node_type == "FOR":
            self.scope_stack.append("for")
            self.visit(node["init"])
            self.visit(node["cond"])
            self.visit(node["update"])
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

# Exemplo de uso
if __name__ == "__main__":
    codigo = ''' 
    if (x + 2) {
        return x;
    }
    y = 5;
    return y + 1;
    '''

    tokens = analisador_lexico(codigo)
    parser = Parser(tokens)
    ast = parser.parse()

    builder = SymbolTableBuilder()
    tabela = builder.build(ast)

    print("\nTabela de símbolos:")
    for simbolo in tabela:
        print(simbolo)

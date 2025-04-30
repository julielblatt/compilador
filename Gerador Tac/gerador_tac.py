class GeradorTAC:
    def __init__(self):
        self.temp_count = 0
        self.instrucoes = []

    def novo_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def gerar(self, node):
        tipo = node.get("type")

        if tipo == "CMD_LIST":
            for cmd in node["body"]:
                self.gerar(cmd)

        elif tipo == "ASSIGN":
            temp = self.gerar(node["value"])
            self.instrucoes.append(f"{node['var']} = {temp}")

        elif tipo == "RETURN":
            temp = self.gerar(node["value"])
            self.instrucoes.append(f"return {temp}")

        elif tipo == "BIN_OP":
            esquerda = self.gerar(node["left"])
            direita = self.gerar(node["right"])
            temp = self.novo_temp()
            self.instrucoes.append(f"{temp} = {esquerda} {node['op']} {direita}")
            return temp

        elif tipo == "NUMBER":
            return str(node["value"])

        elif tipo == "ID":
            return node["name"]

        elif tipo == "FUNC_CALL":
            args = [self.gerar(arg) for arg in node["args"]]
            temp = self.novo_temp()
            self.instrucoes.append(f"{temp} = call {node['name']}({', '.join(args)})")
            return temp

        elif tipo == "FUNC_CALL_STMT":
            self.gerar(node["call"])

        elif tipo == "FUNC_DECL":
            self.instrucoes.append(f"func {node['name']}({', '.join(node['params'])})")
            self.gerar(node["body"])
            self.instrucoes.append(f"endfunc")

    def imprimir(self):
        print("Código TAC gerado:")
        for instr in self.instrucoes:
            print(instr)



            

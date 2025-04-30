from parser import Parser
from analisador_lexico import analisador_lexico
from gerador_tac import GeradorTAC
from analise_semantica import AnalisadorSemantico
from analise_semantica import SymbolTableBuilder

codigo = """
func soma(a, b, c) {
    return a + b;
}
x = soma(2, 3);
"""

tokens = analisador_lexico(codigo)
parser = Parser(tokens)
ast = parser.parse()

builder = SymbolTableBuilder()
tabela_simbolos = builder.build(ast)
semantico = AnalisadorSemantico(builder)
semantico.verificar(ast)
semantico.imprimir_erros()

tac = GeradorTAC()
tac.gerar(ast)
tac.imprimir()

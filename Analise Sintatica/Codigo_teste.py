from analisador_lexico import analisador_lexico
from parser import Parser

codigo = """
if (x + 2) {
    return x;
}
y = 5;
return y + 1;
"""



tokens = analisador_lexico(codigo)
print("TOKENS:")
for tok in tokens:
    print(tok)
parser = Parser(tokens)
parser.parse()







// PRIMEIRO CODIGO

if (x + 2) {
    return x;
}
y = 5;
return y + 1;

// SEGUNDO CODIGO

x = 0;
while (x < 10) {
    x = x + 1;
    y = y * 2;
}
return x;

// TERCEIRO CODIGO

for (i = 0; i < 10; i = i + 1) {
    if (i * 2) {
        y = y + i;
    }
}
return y;

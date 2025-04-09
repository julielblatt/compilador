import re

# Definição dos tokens com suas expressões regulares
token_specification = [
    ('KEYWORD',   r'\b(if|while|return)\b'),   # Palavras-chave
    ('ID',        r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),  # Identificadores
    ('NUMBER',    r'\b\d+\b'),                 # Números inteiros
    ('OP',        r'[+\-*/]'),                 # Operadores
    ('SYMBOL',    r'[;(){}]'),                 # Símbolos
    ('SKIP',      r'[ \t\n]+'),                # Espaços em branco e quebras de linha
    ('MISMATCH',  r'.'),                       # Qualquer outro caractere
]

# Compilando em uma expressão regular única
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

def analisador_lexico(codigo_fonte):
    tokens = []
    for match in re.finditer(token_regex, codigo_fonte):
        tipo = match.lastgroup
        valor = match.group()

        if tipo == 'SKIP':
            continue
        elif tipo == 'MISMATCH':
            print(f'Erro: Caractere inválido "{valor}"')
        else:
            tokens.append((tipo, valor))
    return tokens

# Exemplo de uso
if __name__ == "__main__":
    entrada = """
    if (x1 + 23) {
        return x1;
    } else {
        while (x2 - 7) {
            y = y * 2;
        }
    }
    """

    resultado = analisador_lexico(entrada)
    for tipo, valor in resultado:
        print(f'{tipo}: {valor}')

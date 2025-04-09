Tokens reconhecidos:
- Palavras-chave: if, while, for, return
- Identificadores (letras, números, underline)
- Números inteiros
- Operadores: +, -, *, /, =
- Símbolos: ; ( ) { }
Gramática Livre de Contexto (GLC):
----------------------------------
S -> CMD_LIST
CMD_LIST -> CMD CMD_LIST | ε
CMD -> if (EXP) BLOCO
| while (EXP) BLOCO
| for (ATRIB ; EXP ; ATRIB) BLOCO
| return EXP ;
| ATRIB ;
ATRIB -> ID = EXP
EXP -> TERM REST_EXP
REST_EXP -> + TERM REST_EXP | - TERM REST_EXP | ε
TERM -> FACTOR REST_TERM
REST_TERM -> * FACTOR REST_TERM | / FACTOR REST_TERM | ε
FACTOR -> (EXP) | NUMBER | ID
BLOCO -> { CMD_LIST }
Três códigos de teste foram desenvolvidos contendo: estruturas de repetição, condicionais,
expressões matemáticas e uso de variáveis.

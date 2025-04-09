//PRIMEIRO CODIGO

S
└── CMD_LIST
    ├── CMD (if)
    │   └── if (EXP) BLOCO
    │       ├── EXP → TERM + TERM
    │       │   ├── TERM → FACTOR (ID: x)
    │       │   └── TERM → FACTOR (NUMBER: 2)
    │       └── BLOCO
    │           └── { CMD_LIST → CMD (return) → return x ; }
    ├── CMD (ATRIB) → y = 5 ;
    └── CMD (return) → return y + 1 ;

//SEGUNDO CODIGO

S
└── CMD_LIST
    ├── CMD → x = 0 ;
    ├── CMD (while)
    │   └── while (x < 10) BLOCO
    │       └── BLOCO → { CMD_LIST }
    │           ├── CMD → x = x + 1 ;
    │           └── CMD → y = y * 2 ;
    └── CMD → return x ;


//TERCEIRO CODIGO

S
└── CMD_LIST
    ├── CMD (for)
    │   └── for (ATRIB; EXP; ATRIB) BLOCO
    │       ├── ATRIB → i = 0
    │       ├── EXP → i < 10
    │       ├── ATRIB → i = i + 1
    │       └── BLOCO → {
            CMD_LIST
                └── CMD (if)
                    └── if (EXP → i * 2) BLOCO
                        └── BLOCO → { CMD → y = y + i ; }
          }
    └── CMD → return y ;

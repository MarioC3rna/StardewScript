# Construir el lexer
import ply.lex as lex


# Tokens del lenguaje StardewScript
tokens = (
    'ID',             # Identificadores (nombres de variables)
    'NUM',            # Números
    'STRING',         # Cadenas de texto
    'PLUS',           # +
    'MINUS',          # -
    'MUL',            # *
    'DIV',            # /
    'EQUAL',          # =
    'UBICAR',         # :=
    'CORRAL_OPEN',    # (
    'CORRAL_CLOSE',   # )
    'PUERTA_OPEN',    # {
    'PUERTA_CLOSE',   # }
    'CIERRE_FINAL',   # ;
    'VALLA',          # ,
    'NOT_EQUAL',      # !=
   
)

# Palabras reservadas
reserved = {
    'GRANJA': 'GRANJA',
    'CIERRE': 'CIERRE',
    'SEMILLA': 'SEMILLA',
    'PLANTAR': 'PLANTAR',
    'SIEMBRA': 'SIEMBRA',
    'ENTONCES': 'ENTONCES',
    'COSECHA': 'COSECHA',
    'MIENTRAS': 'MIENTRAS',
    'DIA': 'DIA',
    'MOSTRAR': 'MOSTRAR',
    'RECETA': 'RECETA',
    'ENTREGAR': 'ENTREGAR',
    'INVERNADERO': 'INVERNADERO',
    'Y': 'Y',
    'O': 'O',
    'MAYOR': 'MAYOR',
    'MENOR': 'MENOR',
    'MAYOR_O_IGUAL': 'MAYOR_O_IGUAL',
    'MENOR_O_IGUAL': 'MENOR_O_IGUAL',
}

# Agregar palabras reservadas a tokens
tokens = tokens + tuple(reserved.values())

# Expresiones regulares para tokens
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MUL = r'\*'
t_DIV = r'\/'
t_EQUAL = r'='
t_UBICAR = r':='
t_CORRAL_OPEN = r'\('
t_CORRAL_CLOSE = r'\)'
t_PUERTA_OPEN = r'\{'
t_PUERTA_CLOSE = r'\}'
t_CIERRE_FINAL = r';'
t_VALLA = r','
t_NOT_EQUAL = r'!='
t_MENOR = r'<'
t_MAYOR = r'>'
t_MENOR_O_IGUAL = r'<='
t_MAYOR_O_IGUAL = r'>='


# Regex complejas que acepta 
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUM(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t


def t_STRING(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]
    return t


# Ignorar espacios en blanco
t_ignore = ' \t'


# Saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Manejo de errores
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)


# Construir el lexer
lexer = lex.lex()
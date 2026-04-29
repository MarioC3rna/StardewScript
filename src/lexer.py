import ply.lex as lex

# Variable global para registrar errores
_error_table = None

def set_error_table(error_table):
    """Establecer tabla de errores para registrar errores del lexer"""
    global _error_table
    _error_table = error_table

tokens = (
    'ID', 'NUM', 'STRING',
    'PLUS', 'MINUS', 'MUL', 'DIV',
    'UBICAR', 'CORRAL_OPEN', 'CORRAL_CLOSE',
    'CIERRE_FINAL',
    'MAYOR', 'MENOR', 'MAYOR_O_IGUAL', 'MENOR_O_IGUAL', 'IGUAL',
    'GRANJA', 'CIERRE', 'SEMILLA', 'PLANTAR', 'SIEMBRA', 'ENTONCES',
    'COSECHA', 'MIENTRAS', 'DIA', 'MOSTRAR', 'RECETA', 'ENTREGAR',
    'INVERNADERO', 'Y', 'O', 'SINO',
)

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
    'MAYOR': 'MAYOR',
    'MENOR': 'MENOR',
    'MAYOR_O_IGUAL': 'MAYOR_O_IGUAL',
    'MENOR_O_IGUAL': 'MENOR_O_IGUAL',
    'IGUAL': 'IGUAL',
    'Y': 'Y',
    'O': 'O',
    'SINO': 'SINO',
}

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MUL = r'\*'
t_DIV = r'\/'
t_UBICAR = r':='
t_CORRAL_OPEN = r'\('
t_CORRAL_CLOSE = r'\)'
t_CIERRE_FINAL = r';'
t_MAYOR = r'>'
t_MENOR = r'<'
t_MAYOR_O_IGUAL = r'>='
t_MENOR_O_IGUAL = r'<='
t_IGUAL = r'=='


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


t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    if _error_table:
        _error_table.add_error('Léxico', t.lexer.lineno, t.lexpos, f"Carácter ilegal '{t.value[0]}'")
    print(f"Carácter ilegal '{t.value[0]}' en línea {t.lexer.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()

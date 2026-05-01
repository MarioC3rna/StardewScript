import ply.yacc as yacc
from src.lexer import tokens  # noqa: F401

# Variable global para registrar errores
_error_table = None

def set_error_table(error_table):
    """Establecer tabla de errores para registrar errores del parser"""
    global _error_table
    _error_table = error_table

precedence = (
    ('left', 'O'),
    ('left', 'Y'),
    ('left', 'MAYOR', 'MENOR', 'MAYOR_O_IGUAL', 'MENOR_O_IGUAL',
     'IGUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV'),
)

 # aqui se estructura el arbol 
 
def p_programa(p):
    '''programa : GRANJA instrucciones CIERRE'''
    p[0] = ('programa', p[2])


def p_instrucciones_single(p):
    '''instrucciones : instruccion'''
    p[0] = [p[1]]


def p_instrucciones_multiple(p):
    '''instrucciones : instrucciones instruccion'''
    p[0] = p[1] + [p[2]]


def p_instruccion(p):
    '''instruccion : declaracion
                   | mostrar
                   | condicional
                   | bucle_mientras
                   | bucle_dia'''
    p[0] = p[1]


def p_declaracion(p):
    '''declaracion : SEMILLA ID UBICAR expresion CIERRE_FINAL'''
    p[0] = ('declaracion', p[2], p[4])


def p_mostrar(p):
    '''mostrar : MOSTRAR expresion CIERRE_FINAL'''
    p[0] = ('mostrar', p[2])


def p_condicional_sin_else(p):
    '''condicional : SIEMBRA expresion ENTONCES instrucciones COSECHA'''
    p[0] = ('condicional', p[2], p[4], None)


def p_condicional_con_sino(p):
    '''condicional : SIEMBRA expresion ENTONCES instrucciones COSECHA SINO \
                   instrucciones'''
    p[0] = ('condicional', p[2], p[4], p[7])


def p_condicional_con_sino_si(p):
    '''condicional : SIEMBRA expresion ENTONCES instrucciones COSECHA SINO SI \
                   expresion ENTONCES instrucciones COSECHA'''
    # Crea un condicional anidado: si la primera condición es falsa, evalúa la segunda
    inner_cond = ('condicional', p[8], p[10], None)
    p[0] = ('condicional', p[2], p[4], [inner_cond])


def p_condicional_con_sino_si_else(p):
    '''condicional : SIEMBRA expresion ENTONCES instrucciones COSECHA SINO SI \
                   expresion ENTONCES instrucciones COSECHA SINO instrucciones'''
    # SINO SI con SINO final
    inner_cond = ('condicional', p[8], p[10], p[13])
    p[0] = ('condicional', p[2], p[4], [inner_cond])


def p_bucle_mientras(p):
    '''bucle_mientras : MIENTRAS expresion INVERNADERO \
                      instrucciones CIERRE'''
    p[0] = ('mientras', p[2], p[5])


def p_bucle_dia_sin_cierre_extra(p):
    '''bucle_dia : DIA ID UBICAR NUM INVERNADERO instrucciones'''
    p[0] = ('dia', p[2], ('num', p[4]), p[6])


def p_expresion_or(p):
    '''expresion : expresion_y O expresion
                 | expresion_y'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])


def p_expresion_and(p):
    '''expresion_y : expresion_comp Y expresion_y
                   | expresion_comp'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])


def p_expresion_comp(p):
    '''expresion_comp : suma MAYOR suma
                      | suma MENOR suma
                      | suma MAYOR_O_IGUAL suma
                      | suma MENOR_O_IGUAL suma
                      | suma IGUAL suma
                      | suma'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])


def p_suma(p):
    '''suma : producto PLUS suma
            | producto MINUS suma
            | producto'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])


def p_producto(p):
    '''producto : factor MUL producto
                | factor DIV producto
                | factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])


def p_factor_num(p):
    '''factor : NUM'''
    p[0] = ('num', p[1])


def p_factor_id(p):
    '''factor : ID'''
    p[0] = ('id', p[1])


def p_factor_string(p):
    '''factor : STRING'''
    p[0] = ('string', p[1])


def p_factor_expr(p):
    '''factor : CORRAL_OPEN expresion CORRAL_CLOSE'''
    p[0] = p[2]


def p_error(p):
    if p:
        if _error_table:
            column = _error_table.get_column_from_lexpos(p.lineno, p.lexpos)
            _error_table.add_parser_error(p.lineno, column, p.value)
        print(f"Error sintáctico en '{p.value}'")
    else:
        if _error_table:
            _error_table.add_error('Sintáctico', 0, 0, 'Error sintáctico en EOF')
        print("Error sintáctico en EOF")


parser = yacc.yacc(debug=False, write_tables=False)


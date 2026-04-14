import ply.yacc as yacc
from src.lexer import tokens  # noqa: F401

precedence = (
    ('left', 'MAYOR', 'MENOR', 'MAYOR_O_IGUAL', 'MENOR_O_IGUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV'),
)


# Reglas de gramática
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


def p_expresion(p):
    '''expresion : expresion PLUS expresion
                 | expresion MINUS expresion
                 | expresion MUL expresion
                 | expresion DIV expresion
                 | expresion MAYOR expresion
                 | expresion MENOR expresion
                 | expresion MAYOR_O_IGUAL expresion
                 | expresion MENOR_O_IGUAL expresion
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


def p_condicional(p):
    '''condicional : SIEMBRA expresion ENTONCES instrucciones COSECHA'''
    p[0] = ('condicional', p[2], p[4], None)


def p_condicional_else(p):
    '''condicional : SIEMBRA expresion ENTONCES instrucciones
                     COSECHA instrucciones'''
    p[0] = ('condicional', p[2], p[4], p[6])


def p_bucle_mientras(p):
    '''bucle_mientras : MIENTRAS expresion INVERNADERO instrucciones CIERRE'''
    p[0] = ('mientras', p[2], p[4])


def p_bucle_dia(p):
    '''bucle_dia : DIA ID UBICAR NUM INVERNADERO instrucciones CIERRE'''
    p[0] = ('dia', p[2], ('num', p[4]), p[6])


# Error
def p_error(p):
    if p:
        print(f"Error sintáctico en '{p.value}'")
    else:
        print("Error sintáctico en EOF")


# Construir parser
parser = yacc.yacc(debug=False)
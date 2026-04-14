from src.lexer import lexer
from src.parser import parser

# Leer el archivo de prueba
with open('src/tests/valid_programs/prog_condicional.sdw', 'r') as f:
    code = f.read()

print("=== CÓDIGO FUENTE ===")
print(code)
print("\n=== ANÁLISIS SINTÁCTICO ===")

# Analizar
result = parser.parse(code, lexer=lexer)

print("\n=== ÁRBOL DE DERIVACIÓN ===")
print(result)
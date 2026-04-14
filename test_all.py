import os
from src.lexer import lexer
from src.parser import parser
from src.error_table import ErrorTable

error_table = ErrorTable()


def test_program(filepath, is_valid):
    """Probar un programa"""
    print(f"\n{'='*60}")
    print(f"Archivo: {filepath}")
    print(f"{'='*60}")
    
    with open(filepath, 'r') as f:
        code = f.read()
    
    print("Código:")
    print(code)
    print("\nAnálisis:")
    
    try:
        result = parser.parse(code, lexer=lexer)
        if result:
            print("✓ Programa válido")
        else:
            print("✗ Error sintáctico")
            error_table.add_error("Sintáctico", 1, 1, "Estructura inválida")
    except Exception as e:
        print(f"✗ Error: {e}")
        error_table.add_error("Léxico/Sintáctico", 1, 1, str(e))


# Pruebas válidas
print("\n" + "="*60)
print("PRUEBAS VÁLIDAS")
print("="*60)

valid_dir = 'src/tests/valid_programs'
for file in sorted(os.listdir(valid_dir)):
    if file.endswith('.sdw'):
        test_program(os.path.join(valid_dir, file), True)

# Pruebas inválidas
print("\n" + "="*60)
print("PRUEBAS INVÁLIDAS")
print("="*60)

invalid_dir = 'src/tests/invalid_programs'
for file in sorted(os.listdir(invalid_dir)):
    if file.endswith('.sdw'):
        test_program(os.path.join(invalid_dir, file), False)

# Mostrar tabla de errores
error_table.print_table()
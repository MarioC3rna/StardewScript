
# StardewScript

Lenguaje de programación compilado inspirado en StardewValley.

## ¿Qué es StardewScript?

StardewScript es un lenguaje funcional diseñado con temática agrícola basada en el juego StardewValley. Permite escribir programas con sintaxis creativa usando palabras como GRANJA, SEMILLA, SIEMBRA, COSECHA, etc.

## Estructura del Proyecto

src/
├── lexer.py # Analizador léxico (tokenización)
├── parser.py # Analizador sintáctico (ast)
├── symbol_table.py # Tabla de símbolos (variables)
├── error_table.py # Tabla de errores
└── tests/
├── valid_programs/ # Programas correctos
└── invalid_programs/ # Programas con errores


## Cómo ejecutar

Desde la raíz del proyecto:

```bash
python main.py                # Ejecuta un programa de prueba
python test_all.py            # Ejecuta todas las pruebas

Requisitos
Python 3.7+
PLY (Python Lex-Yacc)

Flujo de compilación
Análisis léxico (lexer.py): Divide el código en tokens
Análisis sintáctico (parser.py): Construye el árbol de derivación
Validación: Se registran errores en tabla
Salida: Imprime el árbol sintáctico resultante


---

**Para qué sirve:**
- Documentación básica del proyecto
- Instrucciones de instalación y ejecución
- Explicación de la estructura

Cuando termines, dime **"Hecho"** y pasamos al MANUAL.md.---

**Para qué sirve:**
- Documentación básica del proyecto
- Instrucciones de instalación y ejecución
- Explicación de la estructura


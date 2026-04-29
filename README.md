# StardewScript - Compilador Web

Lenguaje de programación inspirado en StardewValley con interfaz web completa, compilador en Python con análisis léxico, sintáctico y semántico, visualización de AST, tabla de símbolos con evaluación de expresiones y reproductor de música persistente.

---

## 📖 Tabla de Contenidos

1. [Palabras Reservadas](#palabras-reservadas)
2. [Qué se Puede Hacer](#qué-se-puede-hacer)
3. [Ejemplos de Programas](#ejemplos-de-programas)
4. [Arquitectura General](#arquitectura-general)
5. [Archivos Importantes](#archivos-importantes)
6. [Archivos Secundarios](#archivos-secundarios)
7. [Configuración y Ejecución](#configuración-y-ejecución)

---

## 📝 Palabras Reservadas

StardewScript define 19 palabras clave. Las acciones y estructuras se escriben usando la semántica de StardewValley:

### Estructura General
- **GRANJA** - Inicia un programa
- **CIERRE** - Finaliza un programa

### Variables
- **SEMILLA** - Declara una variable con un valor inicial
  ```
  SEMILLA contador := 5;
  SEMILLA resultado := contador + 3;
  ```

### Entrada/Salida
- **MOSTRAR** - Imprime una expresión o variable
  ```
  MOSTRAR "Hola mundo";
  MOSTRAR resultado;
  ```

### Condicionales
- **SIEMBRA** - Inicia un bloque condicional
- **ENTONCES** - Rama verdadera del condicional
- **COSECHA** - Cierra la rama verdadera
- **SINO** - Rama falsa (else)
- **SI** - Segunda condición en else-if
  ```
  SIEMBRA contador MAYOR 10 ENTONCES
    MOSTRAR "Mayor a 10";
  COSECHA
  SINO SI contador MAYOR 5 ENTONCES
    MOSTRAR "Mayor a 5";
  COSECHA
  SINO
    MOSTRAR "Menor o igual a 5";
  ```

### Bucles
- **MIENTRAS** - Bucle condicional
- **INVERNADERO** - Abre el bloque de instrucciones del bucle
  ```
  MIENTRAS contador MENOR 10 INVERNADERO
    MOSTRAR contador;
  CIERRE
  ```

- **DIA** - Bucle con iterador (for-like)
  ```
  DIA i := 1 INVERNADERO
    MOSTRAR i;
  ```

### Operadores Lógicos
- **Y** - AND lógico
- **O** - OR lógico

---

## ✨ Qué se Puede Hacer

### 1. Declaración de Variables
Declara variables con inicialización de expresiones. El compilador evalúa la expresión inmediatamente:
```
SEMILLA x := 5;
SEMILLA y := 10;
SEMILLA suma := x + y;  // suma = 15
```

### 2. Operaciones Aritméticas
- Suma: `+`
- Resta: `-`
- Multiplicación: `*`
- División: `/`

```
SEMILLA resultado := (10 + 5) * 2;  // resultado = 30
```

### 3. Comparaciones
- Mayor que: `MAYOR`
- Menor que: `MENOR`
- Mayor o igual: `MAYOR_O_IGUAL`
- Menor o igual: `MENOR_O_IGUAL`
- Igual: `IGUAL`

```
SIEMBRA x MAYOR 5 ENTONCES
  MOSTRAR "x es mayor a 5";
COSECHA
```

### 4. Lógica Booleana
Combina condiciones con `Y` (AND) y `O` (OR):

```
SIEMBRA x MAYOR 5 Y x MENOR 20 ENTONCES
  MOSTRAR "x está entre 5 y 20";
COSECHA
```

### 5. Condicionales Anidados (SINO SI)
Encadena múltiples condiciones sin usar muchos niveles de indentación:

```
SIEMBRA edad MAYOR 18 ENTONCES
  MOSTRAR "Es adulto";
COSECHA
SINO SI edad MAYOR 13 ENTONCES
  MOSTRAR "Es adolescente";
COSECHA
SINO
  MOSTRAR "Es niño";
```

### 6. Bucles
Repite código mientras se cumple una condición:

```
MIENTRAS contador MENOR 10 INVERNADERO
  MOSTRAR contador;
CIERRE
```

O usa un bucle con iterador (número de repeticiones):

```
DIA i := 1 INVERNADERO
  MOSTRAR "Iteración " i;
```

### 7. Detecta Errores en Tres Niveles
- **Léxico**: Caracteres ilegales
- **Sintáctico**: Estructura de código incorrecta
- **Semántico**: Variables no declaradas o duplicadas

Cada error muestra el contexto con caret visual:
```
[Sintáctico] Línea 3, Columna 8
Token inesperado: extra
CIERRE extra
       ^
```

---

## 📚 Ejemplos de Programas

### Ejemplo 1: Declaración y Aritmética
```
GRANJA
SEMILLA x := 10;
SEMILLA y := 20;
SEMILLA suma := x + y;
MOSTRAR suma;
CIERRE
```

### Ejemplo 2: Condicional Simple
```
GRANJA
SEMILLA dinero := 100;
SIEMBRA dinero MAYOR 50 ENTONCES
  MOSTRAR "Tengo mucho dinero";
COSECHA
SINO
  MOSTRAR "Necesito trabajar más";
CIERRE
```

### Ejemplo 3: Condicional Múltiple
```
GRANJA
SEMILLA puntos := 75;
SIEMBRA puntos MAYOR 90 ENTONCES
  MOSTRAR "Excelente";
COSECHA
SINO SI puntos MAYOR 70 ENTONCES
  MOSTRAR "Bueno";
COSECHA
SINO
  MOSTRAR "Necesitas mejorar";
CIERRE
```

### Ejemplo 4: Bucle
```
GRANJA
SEMILLA contador := 1;
MIENTRAS contador MENOR 5 INVERNADERO
  MOSTRAR contador;
CIERRE
```

---

## 🏗️ Arquitectura General

```
┌─────────────────────────────────────────────────────────┐
│                    StardewScript IDE                     │
│                   (Frontend: HTML/JS)                    │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  [Editor] ──> [Botón Compilar] ──> [API /compile]      │
│                                                           │
│  ◄─ [Tokens] ◄─ [Errores] ◄─ [AST] ◄─ [Símbolos] ◄─  │
│                                                           │
└─────────────────────────────────────────────────────────┘
                            ↓↑
              ┌─────────────────────────────────┐
              │   Flask Backend (app.py)        │
              ├─────────────────────────────────┤
              │ 1. Lexer (src/lexer.py)        │
              │    → Tokens                     │
              │ 2. Parser (src/parser.py)      │
              │    → AST                        │
              │ 3. Validator (src/validator.py)│
              │    → Errores semánticos         │
              │ 4. Extractor (app.py)          │
              │    → Tabla de símbolos         │
              └─────────────────────────────────┘
```

**Flujo de compilación:**
1. Usuario escribe código en editor
2. Presiona "COMPILAR CÓDIGO"
3. Frontend envía código a `/compile`
4. Backend ejecuta: Lexer → Parser → Validator → Extractor
5. Retorna JSON con: AST, Tokens, Errores, Símbolos
6. Frontend renderiza todos los resultados

---

## 📂 Archivos Importantes

### `app.py` - Backend Principal
**Propósito**: Servidor Flask que coordina todo el compilador.

**Componentes clave**:
- `@app.route('/compile', methods=['POST'])` - Endpoint principal
  - Recibe código fuente en JSON
  - Configura lexer, parser, validador
  - Retorna: AST, tokens, errores, símbolos
  
- `evaluate_expression(expr, symbol_table)` - Evaluador de expresiones
  - Calcula valores de expresiones aritméticas y booleanas
  - Resuelve variables declaradas
  - Devuelve el valor evaluado

- `extract_symbols(ast, symbol_table)` - Extractor de símbolos
  - Recorre el AST buscando declaraciones
  - Guarda variable, tipo y valor evaluado
  - Alimenta la tabla de símbolos que se muestra en UI

- `infer_symbol_type(value, expression)` - Inferencia de tipos
  - Deduce el tipo (número, texto, booleano)
  - Facilita display correcto en tabla

### `src/lexer.py` - Análisis Léxico
**Propósito**: Divide el código en tokens.

**Palabras reservadas soportadas**:
- Control: GRANJA, CIERRE, SEMILLA, MOSTRAR
- Condicionales: SIEMBRA, ENTONCES, COSECHA, SINO, SI
- Bucles: MIENTRAS, DIA, INVERNADERO
- Operadores: Y, O, MAYOR, MENOR, MAYOR_O_IGUAL, MENOR_O_IGUAL, IGUAL
- Símbolos: :=, ;, (, ), +, -, *, /

**Tipos de token**:
- ID: identificadores (variables)
- NUM: números enteros o decimales
- STRING: texto entre comillas
- Operadores y palabras clave

**Ejemplo**:
```
Entrada:  SEMILLA x := 5;
Tokens:   SEMILLA, ID(x), UBICAR, NUM(5), CIERRE_FINAL
```

### `src/parser.py` - Análisis Sintáctico
**Propósito**: Valida estructura gramatical y genera AST.

**Estructura de la gramática**:
```
programa := GRANJA instrucciones CIERRE

instrucciones := instruccion | instrucciones instruccion

instruccion := declaracion | mostrar | condicional | bucle_mientras | bucle_dia

declaracion := SEMILLA ID := expresion ;

mostrar := MOSTRAR expresion ;

condicional := SIEMBRA expr ENTONCES instr COSECHA
             | SIEMBRA expr ENTONCES instr COSECHA SINO instr
             | SIEMBRA expr ENTONCES instr COSECHA SINO SI expr ENTONCES instr COSECHA
             | SIEMBRA expr ENTONCES instr COSECHA SINO SI expr ENTONCES instr COSECHA SINO instr
```

**Precedencia de operadores**:
1. O (OR) - más baja
2. Y (AND)
3. Comparaciones (>, <, >=, <=, ==)
4. Suma/Resta (+, -)
5. Multiplicación/División (*, /) - más alta

**Salida**: Árbol de Sintaxis Abstracta (AST) como tuplas anidadas.

### `src/error_table.py` - Gestión de Errores
**Propósito**: Centraliza detección y presentación de errores.

**Métodos principales**:
- `add_error(error_type, line, column, description)` - Registra error con contexto
- `get_column_from_lexpos(line_num, lexpos)` - Convierte posición absoluta a columna relativa
- `_get_context(line_num, column)` - Genera línea de código + caret visual

**Tipos de error**:
- Léxico: caracteres ilegales
- Sintáctico: estructura incorrecta
- Semántico: variable no declarada, duplicada, etc.

**Salida JSON**:
```json
{
  "type": "Sintáctico",
  "line": 3,
  "column": 8,
  "description": "Token inesperado: extra",
  "context": {
    "code": "CIERRE extra",
    "caret": "       ^"
  }
}
```

### `src/symbol_table.py` - Tabla de Símbolos
**Propósito**: Almacena información de variables.

**Información por variable**:
- Nombre
- Tipo (número, texto, booleano)
- Valor evaluado (calculado en tiempo de compilación)

**Métodos**:
- `add_symbol(name, var_type, value)` - Registra variable
- `get_symbol(name)` - Busca variable
- `symbol_exists(name)` - Verifica si existe
- `update_value(name, value)` - Actualiza valor

### `src/validator.py` - Validación Semántica
**Propósito**: Detecta errores de lógica y contexto.

**Validaciones**:
- Variables duplicadas: `SEMILLA x := 5; SEMILLA x := 10;` ✗
- Variables no declaradas: `MOSTRAR y;` (sin declarar y) ✗
- Ámbito correcto en cada bloque

**Método principal**:
- `validate(ast)` - Recorre AST y valida cada nodo
- `_validate_expression(expr)` - Valida que variables en expresiones estén declaradas

---

## 📂 Archivos Secundarios

### `static/` - Frontend y Estilos
**Propósito**: Interfaz web y lógica del cliente.

- **`templates/index.html`** - Estructura HTML
  - Editor de código, botones de compilación
  - Paneles de tokens, errores, símbolos, AST
  - Cuadro flotante de música

- **`style.css`** - Estilos Stardew Valley
  - Tema verde y dorado inspirado en el juego
  - Responsive design, paneles con blur
  - Estilos para errores, tokens, símbolos

- **`js/main.js`** - Punto de entrada
  - Inicializa aplicación
  - Conecta eventos de botones
  - Maneja resize del AST

- **`js/api.js`** - Cliente HTTP
  - `requestCompile(code)` - Envía código al servidor

- **`js/render.js`** - Renderización
  - Muestra tokens, errores, símbolos, AST
  - Formatea contexto de errores con visual

- **`js/ast.js`** - Visualización de AST
  - D3.js para dibujar árbol
  - Nodos rectangulares, colores personalizados

- **`js/audio.js`** - Reproductor de música
  - Carga canciones desde archivos
  - Persistencia en localStorage
  - Control de mute/unmute

- **`js/ui.js`** - Referencias a elementos DOM

- **`js/tests.js`** - Carga programas de ejemplo
  - Válidos e inválidos desde el servidor

### `tests/` - Suite de Pruebas
**Propósito**: Validación automática.

- **`test_compiler.py`**
  - `TestValidPrograms` - Verifica que programas válidos compilen
  - `TestInvalidPrograms` - Verifica que programas inválidos fallen

Ejecuta con:
```bash
python -m unittest discover -s tests
```

### `src/tests/` - Fixtures
**Propósito**: Programas de ejemplo para testing.

- **`valid_programs/`** - 7 programas correctos
  - `prog1.sdw` - Declaración básica
  - `prog_condicional.sdw` - Ejemplo SIEMBRA/COSECHA
  - `prog_bucle.sdw` - Ejemplo DIA

- **`invalid_programs/`** - 5 programas con errores
  - `error1.sdw` - Error léxico (@)
  - `error2.sdw` - Error sintáctico (sin :=)
  - Etc.

### `main.py` - Script Principal Alternativo
**Propósito**: Compilación desde línea de comandos (no usado en web).

Permite ejecutar compilador directamente:
```bash
python main.py
```

### `src/parsetab.py`, `src/parser.out` - Caché de PLY
**Propósito**: Archivos generados automáticamente por PLY (Lex/Yacc).

- `parsetab.py` - Tablas de parsing compiladas
- `parser.out` - Depuración del parser

---

## 🚀 Configuración y Ejecución

### Requisitos
- Python 3.13+
- Flask
- PLY (Python Lex-Yacc)

### Setup
```bash
# Crear entorno virtual
python -m venv .venv

# Activar (Windows)
.venv\Scripts\activate

# Instalar dependencias
pip install flask ply
```

### Ejecutar Servidor Web
```bash
python app.py
```
Accede a `http://localhost:5000` en tu navegador.

### Ejecutar Tests
```bash
python -m unittest discover -s tests -v
```

### Compilar desde línea de comandos
```bash
python main.py
```

---

## 🎨 Características Especiales

### 1. Evaluación en Tiempo de Compilación
La tabla de símbolos no solo guarda expresiones, sino que las evalúa:
```
Código: SEMILLA resultado := contador + 3;  (donde contador=5)
Salida: resultado = 8
```

### 2. Error Handling Multicapa
- **Léxico**: Detecta caracteres no válidos inmediatamente
- **Sintáctico**: Valida estructura gramatical
- **Semántico**: Verifica lógica (variables declaradas, no duplicadas)

### 3. Contexto Visual de Errores
Cada error muestra:
- Línea y columna exactas
- Código original
- Caret (^) alineado al error

### 4. AST Interactivo
Árbol SVG generado con D3.js que muestra la estructura del programa de forma visual.

### 5. Reproductor de Música Persistente
- Sube canciones que se guardan en el navegador
- Suena en bucle cada vez que abres la web
- Botón de mute/unmute en esquina inferior izquierda

---

## 📝 Resumen

**StardewScript** es un compilador educativo completo para un lenguaje inspirado en StardewValley. Incluye:

✅ Lexer (análisis léxico)  
✅ Parser (análisis sintáctico)  
✅ Validator (análisis semántico)  
✅ Evaluador de expresiones  
✅ Tabla de símbolos con valores calculados  
✅ Visualización de AST con D3.js  
✅ Interfaz web completa  
✅ Reproductor de música persistente  
✅ Suite de pruebas automáticas  
✅ Manejo de errores con contexto visual  

---

**Última actualización**: 29 de abril de 2026

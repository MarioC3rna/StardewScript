from flask import Flask, render_template, request, jsonify
from pathlib import Path
from src.lexer import lexer, set_error_table as set_lexer_error_table
from src.parser import parser, set_error_table as set_parser_error_table
from src.error_table import ErrorTable
from src.symbol_table import SymbolTable
from src.validator import SemanticValidator

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/compile', methods=['POST'])
def compile_code():
    data = request.json
    code = data.get('code', '')

    error_table = ErrorTable(source_code=code)
    symbol_table = SymbolTable()

    try:
        # Configurar captura de errores léxicos y sintácticos
        set_lexer_error_table(error_table)
        set_parser_error_table(error_table)

        # Reiniciar estado del lexer para que las líneas no se acumulen entre compilaciones
        lexer.lineno = 1
        
        result = parser.parse(code, lexer=lexer)

        lexer.input(code)
        tokens_list = []

        for tok in lexer:
            tokens_list.append({
                'type': tok.type,
                'value': str(tok.value)
            })

        if result is None:
            error_table.add_error(
                'Sintáctico',
                1,
                1,
                'No se pudo generar el AST por error de sintaxis.'
            )
            return jsonify({
                'success': False,
                'ast': None,
                'tokens': tokens_list,
                'errors': error_table.errors,
                'symbols': {}
            })

        # Validación semántica
        validator = SemanticValidator(error_table)
        validator.validate(result)

        extract_symbols(result, symbol_table)

        return jsonify({
            'success': len(error_table.errors) == 0,
            'ast': serialize_ast(result),
            'tokens': tokens_list,
            'errors': error_table.errors,
            'symbols': symbol_table.symbols
        })
    except Exception as e:
        error_table.add_error('Sintáctico', 1, 1, str(e))
        return jsonify({
            'success': False,
            'ast': None,
            'tokens': [],
            'errors': error_table.errors,
            'symbols': {}
        })


@app.route('/tests/<group>', methods=['GET'])
def get_tests(group):
    group_map = {
        'valid': 'valid_programs',
        'invalid': 'invalid_programs'
    }

    folder_name = group_map.get(group)
    if folder_name is None:
        return jsonify({'success': False, 'message': 'Grupo inválido'}), 400

    tests_dir = Path(__file__).resolve().parent / 'src' / 'tests' / folder_name
    if not tests_dir.exists():
        return jsonify({'success': False, 'tests': []})

    tests = []
    for file_path in sorted(tests_dir.glob('*.sdw')):
        tests.append({
            'name': file_path.name,
            'content': file_path.read_text(encoding='utf-8')
        })

    return jsonify({'success': True, 'tests': tests})


def serialize_ast(node):
    if isinstance(node, tuple):
        return [serialize_ast(item) for item in node]
    if isinstance(node, list):
        return [serialize_ast(item) for item in node]
    return node

#expresiones regulares	

def evaluate_expression(expr, symbol_table):
    if isinstance(expr, tuple):
        node_type = expr[0]

        if node_type == 'num':
            return expr[1]

        if node_type == 'string':
            return expr[1]

        if node_type == 'id':
            symbol = symbol_table.get_symbol(expr[1])
            return symbol['value'] if symbol else None

        if len(expr) == 3:
            operator = expr[0]
            left = evaluate_expression(expr[1], symbol_table)
            right = evaluate_expression(expr[2], symbol_table)

            if left is None or right is None:
                return None

            try:
                if operator == '+':
                    return left + right
                if operator == '-':
                    return left - right
                if operator == '*':
                    return left * right
                if operator == '/':
                    return left / right
                if operator == '>':
                    return left > right
                if operator == '<':
                    return left < right
                if operator == '>=':
                    return left >= right
                if operator == '<=':
                    return left <= right
                if operator == '==':
                    return left == right
                if operator == 'Y':
                    return bool(left) and bool(right)
                if operator == 'O':
                    return bool(left) or bool(right)
            except Exception:
                return None

    return None


def infer_symbol_type(value, expression):
    if isinstance(value, bool):
        return 'booleano'
    if isinstance(value, (int, float)):
        return 'numero'
    if isinstance(value, str):
        return 'texto'

    if isinstance(expression, tuple) and len(expression) > 0:
        if expression[0] == 'string':
            return 'texto'
        return 'numero'

    return 'numero'


def extract_symbols(ast, symbol_table):
    if isinstance(ast, tuple):
        if ast[0] == 'declaracion':
            var_name = ast[1]
            expression = ast[2]
            value = evaluate_expression(expression, symbol_table)
            var_type = infer_symbol_type(value, expression)
            symbol_table.add_symbol(var_name, var_type, value)

        elif ast[0] == 'dia':
            var_name = ast[1]
            expression = ast[2]
            value = evaluate_expression(expression, symbol_table)
            symbol_table.add_symbol(var_name, 'numero', value)

        for item in ast[1:]:
            extract_symbols(item, symbol_table)

    elif isinstance(ast, list):
        for item in ast:
            extract_symbols(item, symbol_table)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

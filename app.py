from flask import Flask, render_template, request, jsonify
from pathlib import Path
from src.lexer import lexer
from src.parser import parser
from src.error_table import ErrorTable
from src.symbol_table import SymbolTable

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/compile', methods=['POST'])
def compile_code():
    data = request.json
    code = data.get('code', '')

    error_table = ErrorTable()
    symbol_table = SymbolTable()

    try:
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

        extract_symbols(result, symbol_table)

        return jsonify({
            'success': True,
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


def extract_symbols(ast, symbol_table):
    if isinstance(ast, tuple):
        if ast[0] == 'declaracion':
            var_name = ast[1]
            value = ast[2]
            symbol_table.add_symbol(var_name, 'numero', value)

        for item in ast[1:]:
            extract_symbols(item, symbol_table)

    elif isinstance(ast, list):
        for item in ast:
            extract_symbols(item, symbol_table)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

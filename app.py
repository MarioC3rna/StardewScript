from flask import Flask, render_template, request, jsonify
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

        if result:
            extract_symbols(result, symbol_table)

        return jsonify({
            'success': True,
            'ast': str(result),
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
class ErrorTable:
    def __init__(self, source_code=None):
        self.errors = []
        self.source_code = source_code
        self.source_lines = source_code.split('\n') if source_code else []

    def set_source_code(self, source_code):
        """Establecer código fuente para contexto de errores"""
        self.source_code = source_code
        self.source_lines = source_code.split('\n') if source_code else []

    def add_error(self, error_type, line, column, description):
        """Agregar error con contexto"""
        error_obj = {
            'type': error_type,
            'line': line,
            'column': column,
            'description': description,
            'context': self._get_context(line, column)
        }
        self.errors.append(error_obj)

    def get_column_from_lexpos(self, line_num, lexpos):
        """Convertir una posición absoluta del lexer a columna dentro de la línea"""
        if line_num <= 0 or not self.source_lines:
            return max(1, lexpos + 1)

        line_start = 0
        for index in range(max(0, line_num - 1)):
            line_start += len(self.source_lines[index]) + 1

        return max(1, lexpos - line_start + 1)

    def _get_context(self, line_num, column):
        """Obtener línea de código y generar caret"""
        if line_num <= 0 or line_num > len(self.source_lines):
            return None
        
        code_line = self.source_lines[line_num - 1]
        caret_line = ' ' * max(0, column - 1) + '^'
        
        return {
            'code': code_line,
            'caret': caret_line
        }

    def add_parser_error(self, error_line, error_col, error_value):
        """Agregar error del parser"""
        self.add_error('Sintáctico', error_line, error_col, f"Token inesperado: {error_value}")

    def has_errors(self):
        """¿Hay errores?"""
        return len(self.errors) > 0

    def print_table(self):
        """Mostrar tabla"""
        if not self.has_errors():
            print("\n=== TABLA DE ERRORES ===")
            print("✓ Sin errores")
            return

        print("\n=== TABLA DE ERRORES ===")
        header = (
            f"{'Tipo':<12} | {'Línea':<6} | {'Columna':<8} | "
            f"{'Descripción':<30}"
        )
        print(header)
        print("-" * 70)
        for err in self.errors:
            line_num = err['line']
            col = err['column']
            err_type = err['type']
            desc = err['description']
            print(f"{err_type:<12} | {line_num:<6} | {col:<8} | {desc:<30}")
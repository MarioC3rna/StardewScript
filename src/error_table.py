class ErrorTable:
    def __init__(self):
        self.errors = []

    def add_error(self, error_type, line, column, description):
        """Agregar error"""
        self.errors.append({
            'type': error_type,
            'line': line,
            'column': column,
            'description': description
        })

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
class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, name, var_type, value=None):
        """Agregar una variable a la tabla"""
        self.symbols[name] = {
            'name': name,
            'type': var_type,
            'value': value
        }

    def get_symbol(self, name):
        """Obtener una variable"""
        return self.symbols.get(name)

    def symbol_exists(self, name):
        """¿Existe la variable?"""
        return name in self.symbols

    def update_value(self, name, value):
        """Actualizar valor de variable"""
        if self.symbol_exists(name):
            self.symbols[name]['value'] = value

    def print_table(self):
        """Mostrar tabla de símbolos"""
        if not self.symbols:
            print("\n=== TABLA DE SÍMBOLOS ===")
            print("Vacía")
            return

        print("\n=== TABLA DE SÍMBOLOS ===")
        header = (
            f"{'Variable':<15} | {'Tipo':<10} | {'Valor':<15}"
        )
        print(header)
        print("-" * 45)
        for name, symbol in self.symbols.items():
            val = symbol['value']
            value = val if val is not None else "indefinido"
            line = (
                f"{name:<15} | {symbol['type']:<10} | "
                f"{str(value):<15}"
            )
            print(line)
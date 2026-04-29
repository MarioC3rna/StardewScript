class SemanticValidator:
    """Validador semántico para detectar errores en el AST"""
    
    def __init__(self, error_table):
        self.error_table = error_table
        self.declared_vars = set()
        self.current_line = 1
    
    def validate(self, ast):
        """Validar el AST y registrar errores semánticos"""
        if ast is None:
            return
        
        self.declared_vars.clear()
        self._visit(ast)
    
    def _visit(self, node):
        """Recorrer el AST recursivamente"""
        if isinstance(node, tuple) and len(node) > 0:
            node_type = node[0]
            
            # Actualizar línea actual si está disponible
            if node_type in ['declaracion', 'mostrar', 'condicional', 'mientras', 'dia']:
                self.current_line = getattr(node, 'lineno', self.current_line)
            
            # Procesar cada tipo de nodo
            if node_type == 'declaracion':
                self._handle_declaracion(node)
            elif node_type == 'mostrar':
                self._handle_mostrar(node)
            elif node_type == 'condicional':
                self._handle_condicional(node)
            elif node_type == 'mientras':
                self._handle_mientras(node)
            elif node_type == 'dia':
                self._handle_dia(node)
            elif node_type == 'programa':
                self._handle_programa(node)
            else:
                # Para otros nodos, visitar recursivamente
                for item in node[1:]:
                    self._visit(item)
        
        elif isinstance(node, list):
            for item in node:
                self._visit(item)
    
    def _handle_declaracion(self, node):
        """SEMILLA x := expresion;"""
        var_name = node[1]
        expresion = node[2]
        
        # Verificar si ya está declarada
        if var_name in self.declared_vars:
            self.error_table.add_error(
                'Semántico',
                self.current_line,
                0,
                f"Variable '{var_name}' ya fue declarada anteriormente"
            )
        else:
            self.declared_vars.add(var_name)
        
        # Validar expresión
        self._validate_expression(expresion)
    
    def _handle_mostrar(self, node):
        """MOSTRAR expresion;"""
        expresion = node[1]
        self._validate_expression(expresion)
    
    def _handle_condicional(self, node):
        """SIEMBRA expresion ENTONCES ... COSECHA [SINO ...]"""
        expresion = node[1]
        bloque_true = node[2]
        bloque_false = node[3]
        
        # Validar condición
        self._validate_expression(expresion)
        
        # Validar bloques
        if bloque_true:
            self._visit(bloque_true)
        if bloque_false:
            self._visit(bloque_false)
    
    def _handle_mientras(self, node):
        """MIENTRAS expresion INVERNADERO ... CIERRE"""
        expresion = node[1]
        bloque = node[2]
        
        # Validar condición
        self._validate_expression(expresion)
        
        # Validar bloque
        self._visit(bloque)
    
    def _handle_dia(self, node):
        """DIA x := NUM INVERNADERO ... CIERRE"""
        var_name = node[1]
        num = node[2]
        bloque = node[3]
        
        # Verificar si ya está declarada
        if var_name in self.declared_vars:
            self.error_table.add_error(
                'Semántico',
                self.current_line,
                0,
                f"Variable '{var_name}' ya fue declarada anteriormente"
            )
        else:
            self.declared_vars.add(var_name)
        
        # Validar bloque
        self._visit(bloque)
    
    def _handle_programa(self, node):
        """programa : GRANJA instrucciones CIERRE"""
        instrucciones = node[1]
        self._visit(instrucciones)
    
    def _validate_expression(self, expresion):
        """Validar que todas las variables en la expresión estén declaradas"""
        if isinstance(expresion, tuple):
            if expresion[0] == 'id':
                var_name = expresion[1]
                if var_name not in self.declared_vars:
                    self.error_table.add_error(
                        'Semántico',
                        self.current_line,
                        0,
                        f"Variable '{var_name}' usada sin ser declarada"
                    )
            else:
                # Recorrer sub-expresiones
                for item in expresion[1:]:
                    self._validate_expression(item)
        
        elif isinstance(expresion, list):
            for item in expresion:
                self._validate_expression(item)

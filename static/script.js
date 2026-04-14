const codeEditor = document.getElementById('codeEditor');
const compileBtn = document.getElementById('compileBtn');
const tokensList = document.getElementById('tokensList');
const errorsList = document.getElementById('errorsList');
const astContainer = document.getElementById('astContainer');
const symbolsList = document.getElementById('symbolsList');

compileBtn.addEventListener('click', compileCode);

async function compileCode() {
    const code = codeEditor.value;
    
    if (!code.trim()) {
        alert('Escribe código para compilar');
        return;
    }

    try {
        const response = await fetch('/compile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: code })
        });

        const data = await response.json();
        
        displayResults(data);
    } catch (error) {
        console.error('Error:', error);
        errorsList.innerHTML = '<div class="error-item">Error de conexión con el servidor</div>';
    }
}

function displayResults(data) {
    if (!data.success) {
        displayErrors(data.errors);
        astContainer.innerHTML = '<p class="placeholder">Compila código válido para ver el árbol</p>';
        symbolsList.innerHTML = '<p class="placeholder">Sin variables</p>';
        return;
    }

    displayErrors(data.errors);
    displaySymbols(data.symbols);
    displayAST(data.ast);
}

function displayErrors(errors) {
    if (!errors || errors.length === 0) {
        errorsList.innerHTML = '<p class="placeholder">✓ Sin errores</p>';
        return;
    }

    errorsList.innerHTML = errors.map(err => 
        `<div class="error-item">
            <strong>${err.type}</strong> - Línea ${err.line}, Col ${err.column}<br>
            ${err.description}
        </div>`
    ).join('');
}

function displaySymbols(symbols) {
    if (!symbols || Object.keys(symbols).length === 0) {
        symbolsList.innerHTML = '<p class="placeholder">Sin variables declaradas</p>';
        return;
    }

    symbolsList.innerHTML = Object.entries(symbols).map(([name, sym]) =>
        `<div class="symbol-item">
            <strong>${name}</strong>: ${sym.type} = ${sym.value || 'indefinido'}
        </div>`
    ).join('');
}

function displayAST(astString) {
    if (!astString) {
        astContainer.innerHTML = '<p class="placeholder">Sin árbol disponible</p>';
        return;
    }

    try {
        const ast = eval(astString);
        drawAST(ast);
    } catch (error) {
        astContainer.innerHTML = `<div class="error-item">Error al procesar AST: ${error.message}</div>`;
    }
}

function drawAST(data) {
    astContainer.innerHTML = '';
    
    const width = astContainer.clientWidth;
    const height = 400;

    const svg = d3.select('#astContainer')
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', 'translate(50, 30)');

    const root = d3.hierarchy(buildHierarchy(data));
    const tree = d3.tree().size([width - 100, height - 60]);
    tree(root);

    svg.selectAll('.link')
        .data(root.links())
        .enter()
        .append('line')
        .attr('class', 'link')
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

    svg.selectAll('.node')
        .data(root.descendants())
        .enter()
        .append('g')
        .attr('class', 'node')
        .attr('transform', d => `translate(${d.x}, ${d.y})`)
        .append('rect')
        .attr('width', 80)
        .attr('height', 30)
        .attr('x', -40)
        .attr('y', -15)
        .attr('rx', 5);

    svg.selectAll('.node')
        .append('text')
        .attr('dy', 5)
        .text(d => d.data.name);
}

function buildHierarchy(ast) {
    if (typeof ast === 'string') {
        return { name: ast, children: [] };
    }

    if (Array.isArray(ast)) {
        return { 
            name: 'Instrucciones', 
            children: ast.map(item => buildHierarchy(item)) 
        };
    }

    if (typeof ast === 'object' && ast !== null) {
        if (ast[0]) {
            const type = ast[0];
            const children = ast.slice(1).map((item, idx) => 
                typeof item === 'string' ? 
                    { name: item, children: [] } : 
                    buildHierarchy(item)
            );
            return { name: type, children };
        }
    }

    return { name: String(ast), children: [] };
}
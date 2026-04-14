const codeEditor = document.getElementById('codeEditor');
const compileBtn = document.getElementById('compileBtn');
const tokensList = document.getElementById('tokensList');
const errorsList = document.getElementById('errorsList');
const astContainer = document.getElementById('astContainer');
const symbolsList = document.getElementById('symbolsList');
const validTestsBtn = document.getElementById('validTestsBtn');
const invalidTestsBtn = document.getElementById('invalidTestsBtn');
const currentTestLabel = document.getElementById('currentTestLabel');

const testCache = {
    valid: null,
    invalid: null
};

const testIndex = {
    valid: -1,
    invalid: -1
};

compileBtn.addEventListener('click', compileCode);
validTestsBtn.addEventListener('click', () => loadNextTest('valid'));
invalidTestsBtn.addEventListener('click', () => loadNextTest('invalid'));

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
        errorsList.innerHTML =
            '<div class="error-item">Error de conexión con el servidor</div>';
    }
}

function displayResults(data) {
    if (!data.success) {
        displayErrors(data.errors);
        astContainer.innerHTML =
            '<p class="placeholder">Compila código válido para ver el árbol</p>';
        displayTokens(data.tokens);
        symbolsList.innerHTML = '<p class="placeholder">Sin variables</p>';
        return;
    }

    displayTokens(data.tokens);
    displayErrors(data.errors);
    displaySymbols(data.symbols);
    displayAST(data.ast);
}

function displayTokens(tokens) {
    if (!tokens || tokens.length === 0) {
        tokensList.innerHTML =
            '<p class="placeholder">Compila código para ver los tokens</p>';
        return;
    }

    tokensList.innerHTML = tokens
        .map((tok) => `<div class="token-item">${tok.type}: ${tok.value}</div>`)
        .join('');
}

function displayErrors(errors) {
    if (!errors || errors.length === 0) {
        errorsList.innerHTML = '<p class="placeholder">✓ Sin errores</p>';
        return;
    }

    errorsList.innerHTML = errors
        .map(
            (err) =>
                `<div class="error-item">
            <strong>${err.type}</strong> - Línea ${err.line}, Col ${err.column}<br>
            ${err.description}
        </div>`
        )
        .join('');
}

function displaySymbols(symbols) {
    if (!symbols || Object.keys(symbols).length === 0) {
        symbolsList.innerHTML =
            '<p class="placeholder">Sin variables declaradas</p>';
        return;
    }

    symbolsList.innerHTML = Object.entries(symbols)
        .map(
            ([name, sym]) =>
                `<div class="symbol-item">
            <strong>${name}</strong>: ${sym.type} = ${sym.value || 'indefinido'}
        </div>`
        )
        .join('');
}

function displayAST(astData) {
    if (!astData) {
        astContainer.innerHTML =
            '<p class="placeholder">Sin árbol disponible</p>';
        return;
    }

    try {
        drawAST(astData);
    } catch (error) {
        console.error('Error:', error);
        astContainer.innerHTML = `<div class="error-item">Error al procesar AST: ${error.message}</div>`;
    }
}

async function loadNextTest(group) {
    try {
        if (!testCache[group]) {
            const response = await fetch(`/tests/${group}`);
            const data = await response.json();

            if (!data.success || !data.tests || data.tests.length === 0) {
                alert('No hay tests disponibles para este grupo.');
                return;
            }

            testCache[group] = data.tests;
        }

        const tests = testCache[group];
        testIndex[group] = (testIndex[group] + 1) % tests.length;
        const selected = tests[testIndex[group]];

        codeEditor.value = selected.content;

        if (group === 'invalid') {
            currentTestLabel.textContent = '';
            currentTestLabel.style.display = 'none';
        } else {
            const groupLabel = 'Válido';
            currentTestLabel.textContent =
                `Test ${groupLabel}: ${selected.name} (${testIndex[group] + 1}/${tests.length})`;
            currentTestLabel.style.display = 'block';
        }
    } catch (error) {
        console.error('Error cargando tests:', error);
        alert('No se pudieron cargar los tests.');
    }
}

function drawAST(data) {
    astContainer.innerHTML = '';

    const container = astContainer;
    const baseWidth = container.clientWidth || 1400;
    const nodeWidth = 110;
    const nodeHeight = 42;
    const horizontalGap = 220;
    const verticalGap = 120;
    const marginX = 90;
    const marginY = 60;

    const hierarchy = d3.hierarchy(buildHierarchy(data));
    const tree = d3.tree().nodeSize([horizontalGap, verticalGap]);
    const root = tree(hierarchy);

    const nodesData = root.descendants();
    const minX = d3.min(nodesData, d => d.x) || 0;
    const maxX = d3.max(nodesData, d => d.x) || 0;
    const maxY = d3.max(nodesData, d => d.y) || 0;

    const width = Math.max(baseWidth, (maxX - minX) + (marginX * 2) + nodeWidth);
    const height = maxY + (marginY * 2) + nodeHeight;

    const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .attr('style', 'background: #0a1428; border-radius: 5px;');

    const g = svg.append('g')
        .attr('transform', `translate(${marginX - minX}, ${marginY})`);

    // Dibujar líneas
    g.selectAll('line')
        .data(root.links())
        .enter()
        .append('line')
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y)
        .attr('stroke', '#7dd56f')
        .attr('stroke-width', 2)
        .attr('opacity', 0.8);

    // Dibujar nodos (rectángulos pequeños)
    const nodes = g.selectAll('g')
        .data(root.descendants())
        .enter()
        .append('g')
        .attr('transform', d => `translate(${d.x},${d.y})`);

    nodes.append('rect')
        .attr('width', nodeWidth)
        .attr('height', nodeHeight)
        .attr('x', -(nodeWidth / 2))
        .attr('y', -(nodeHeight / 2))
        .attr('rx', 4)
        .attr('fill', '#7dd56f')
        .attr('stroke', '#5ab547')
        .attr('stroke-width', 1.5);

    nodes.append('text')
        .attr('text-anchor', 'middle')
        .attr('dy', '0.35em')
        .attr('font-size', '11px')
        .attr('font-weight', 'bold')
        .attr('fill', '#0a1428')
        .text(d => {
            const name = String(d.data.name);
            return name;
        });
}

function buildHierarchy(data) {
    if (typeof data === 'string') {
        return { name: data, children: [] };
    }

    if (typeof data === 'number') {
        return { name: String(data), children: [] };
    }

    if (Array.isArray(data)) {
        return {
            name: '[]',
            children: data.map(item => buildHierarchy(item))
        };
    }

    if (typeof data === 'object' && data !== null && data[0]) {
        const name = String(data[0]);
        const children = data.slice(1)
            .filter(item => item !== null && item !== undefined)
            .map(item => buildHierarchy(item));

        return { name, children };
    }

    return { name: String(data), children: [] };
}

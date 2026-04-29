import { ui } from './ui.js';
import { renderAST } from './ast.js';

export function renderCompilationResult(data) {
    if (!data.success) {
        renderErrors(data.errors);
        renderTokens(data.tokens);
        ui.astContainer.innerHTML =
            '<p class="placeholder">Compila código válido para ver el árbol</p>';
        ui.symbolsList.innerHTML = '<p class="placeholder">Sin variables</p>';
        return;
    }

    renderTokens(data.tokens);
    renderErrors(data.errors);
    renderSymbols(data.symbols);
    renderAST(data.ast);
}

export function renderConnectionError() {
    ui.errorsList.innerHTML =
        '<div class="error-item">Error de conexión con el servidor</div>';
}

export function renderCurrentTestLabel(group, testName, currentIndex, total) {
    if (group === 'invalid') {
        ui.currentTestLabel.textContent = '';
        ui.currentTestLabel.style.display = 'none';
        return;
    }

    ui.currentTestLabel.textContent =
        `Test Válido: ${testName} (${currentIndex + 1}/${total})`;
    ui.currentTestLabel.style.display = 'block';
}

function renderTokens(tokens) {
    if (!tokens || tokens.length === 0) {
        ui.tokensList.innerHTML =
            '<p class="placeholder">Compila código para ver los tokens</p>';
        return;
    }

    ui.tokensList.innerHTML = tokens
        .map((tok) => `<div class="token-item">${tok.type}: ${tok.value}</div>`)
        .join('');
}

function renderErrors(errors) {
    if (!errors || errors.length === 0) {
        ui.errorsList.innerHTML = '<p class="placeholder">✓ Sin errores</p>';
        return;
    }

    ui.errorsList.innerHTML = errors
        .map(
            (err) => {
                let errorHTML = `<div class="error-item">
                    <strong>[${err.type}]</strong> Línea ${err.line}, Columna ${err.column}<br>
                    <span class="error-description">${err.description}</span>`;
                
                // Mostrar contexto si existe
                if (err.context && err.context.code) {
                    errorHTML += `<div class="error-context">
                        <span class="error-context-label">Contexto</span>
                        <code>${err.context.code}</code><br>
                        <code class="error-caret">${err.context.caret}</code>
                    </div>`;
                }
                
                errorHTML += '</div>';
                return errorHTML;
            }
        )
        .join('');
}

function renderSymbols(symbols) {
    if (!symbols || Object.keys(symbols).length === 0) {
        ui.symbolsList.innerHTML =
            '<p class="placeholder">Sin variables declaradas</p>';
        return;
    }

    ui.symbolsList.innerHTML = Object.entries(symbols)
        .map(
            ([name, sym]) =>
                `<div class="symbol-item">
            <strong>${name}</strong>: ${sym.type} = ${formatSymbolValue(sym.value)}
        </div>`
        )
        .join('');
}

function formatSymbolValue(value) {
    if (value === null || value === undefined) {
        return 'indefinido';
    }

    if (typeof value !== 'object') {
        return String(value);
    }

    if (!Array.isArray(value)) {
        return JSON.stringify(value);
    }

    if (value[0] === 'num') {
        return String(value[1]);
    }

    if (value[0] === 'id') {
        return String(value[1]);
    }

    if (value[0] === 'string') {
        return `"${value[1]}"`;
    }

    if (value.length === 3) {
        const left = formatSymbolValue(value[1]);
        const operator = String(value[0]);
        const right = formatSymbolValue(value[2]);
        return `${left} ${operator} ${right}`;
    }

    return value.map(formatSymbolValue).join(', ');
}

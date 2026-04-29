import { ui } from './ui.js';
import { requestCompile } from './api.js';
import { renderCompilationResult, renderConnectionError } from './render.js';
import { redrawLastAST } from './ast.js';
import { loadNextTest } from './tests.js';
import { initializeMusicPlayer } from './audio.js';

let resizeTimer = null;

export function initializeApp() {
    ui.compileBtn.addEventListener('click', handleCompileClick);
    ui.validTestsBtn.addEventListener('click', () => loadNextTest('valid'));
    ui.invalidTestsBtn.addEventListener('click', () => loadNextTest('invalid'));
    window.addEventListener('resize', handleResize);
    initializeMusicPlayer();
}

async function handleCompileClick() {
    const code = ui.codeEditor.value;
    if (!code.trim()) {
        alert('Escribe código para compilar');
        return;
    }

    try {
        const data = await requestCompile(code);
        renderCompilationResult(data);
    } catch (error) {
        console.error('Error:', error);
        renderConnectionError();
    }
}

function handleResize() {
    if (resizeTimer) {
        clearTimeout(resizeTimer);
    }

    resizeTimer = setTimeout(() => {
        redrawLastAST();
    }, 150);
}

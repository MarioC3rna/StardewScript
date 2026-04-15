import { ui } from './ui.js';
import { state } from './state.js';
import { fetchTests } from './api.js';
import { renderCurrentTestLabel } from './render.js';

export async function loadNextTest(group) {
    try {
        if (!state.testCache[group]) {
            state.testCache[group] = await fetchTests(group);
        }

        const tests = state.testCache[group];
        state.testIndex[group] = (state.testIndex[group] + 1) % tests.length;
        const selected = tests[state.testIndex[group]];

        ui.codeEditor.value = selected.content;
        renderCurrentTestLabel(group, selected.name, state.testIndex[group], tests.length);
    } catch (error) {
        console.error('Error cargando tests:', error);
        alert('No se pudieron cargar los tests.');
    }
}

import { ui } from './ui.js';
import { AST_LAYOUT, state } from './state.js';

export function renderAST(astData) {
    if (!astData) {
        ui.astContainer.innerHTML = '<p class="placeholder">Sin árbol disponible</p>';
        state.runtime.lastAstData = null;
        return;
    }

    try {
        drawAST(astData);
        state.runtime.lastAstData = astData;
    } catch (error) {
        console.error('Error:', error);
        ui.astContainer.innerHTML =
            `<div class="error-item">Error al procesar AST: ${error.message}</div>`;
    }
}

export function redrawLastAST() {
    if (state.runtime.lastAstData) {
        drawAST(state.runtime.lastAstData);
    }
}

function drawAST(data) {
    ui.astContainer.innerHTML = '';

    const hierarchy = d3.hierarchy(buildHierarchy(data));
    const tree = d3.tree().nodeSize([AST_LAYOUT.horizontalGap, AST_LAYOUT.verticalGap]);
    const root = tree(hierarchy);

    const nodes = root.descendants();
    const minX = d3.min(nodes, d => d.x) || 0;
    const maxX = d3.max(nodes, d => d.x) || 0;
    const maxY = d3.max(nodes, d => d.y) || 0;

    const baseWidth = ui.astContainer.clientWidth || AST_LAYOUT.minWidth;
    const width = Math.max(
        baseWidth,
        (maxX - minX) + (AST_LAYOUT.marginX * 2) + AST_LAYOUT.nodeWidth
    );
    const height = maxY + (AST_LAYOUT.marginY * 2) + AST_LAYOUT.nodeHeight;

    const svg = d3.select(ui.astContainer)
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .attr('style', 'background: #233a1f; border-radius: 5px;');

    const group = svg.append('g')
        .attr('transform', `translate(${AST_LAYOUT.marginX - minX}, ${AST_LAYOUT.marginY})`);

    drawLinks(group, root.links());
    drawNodes(group, nodes);
}

//aqui se dibuja  el arbol 
function drawLinks(group, links) {
    group.selectAll('line')
        .data(links)
        .enter()
        .append('line')
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y)
        .attr('stroke', '#d9e8b2')
        .attr('stroke-width', 2)
        .attr('opacity', 0.8);
}

function drawNodes(group, nodes) {
    const nodeGroups = group.selectAll('.ast-node')
        .data(nodes)
        .enter()
        .append('g')
        .attr('class', 'ast-node')
        .attr('transform', d => `translate(${d.x},${d.y})`);

    nodeGroups.append('rect')
        .attr('width', AST_LAYOUT.nodeWidth)
        .attr('height', AST_LAYOUT.nodeHeight)
        .attr('x', -(AST_LAYOUT.nodeWidth / 2))
        .attr('y', -(AST_LAYOUT.nodeHeight / 2))
        .attr('rx', 4)
        .attr('fill', '#f4d67f')
        .attr('stroke', '#c9ae63')
        .attr('stroke-width', 1.5);

    nodeGroups.append('text')
        .attr('text-anchor', 'middle')
        .attr('dy', '0.35em')
        .attr('font-size', '11px')
        .attr('font-weight', 'bold')
        .attr('fill', '#3b331f')
        .text((d) => String(d.data.name));
}

function buildHierarchy(data) {
    if (typeof data === 'string' || typeof data === 'number') {
        return { name: String(data), children: [] };
    }

    if (Array.isArray(data)) {
        return {
            name: '[]',
            children: data.map(item => buildHierarchy(item))
        };
    }

    if (typeof data === 'object' && data !== null && data[0]) {
        const children = data.slice(1)
            .filter(item => item !== null && item !== undefined)
            .map(item => buildHierarchy(item));

        return { name: String(data[0]), children };
    }

    return { name: String(data), children: [] };
}

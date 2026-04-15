export async function requestCompile(code) {
    const response = await fetch('/compile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: code })
    });

    return response.json();
}

export async function fetchTests(group) {
    const response = await fetch(`/tests/${group}`);
    const data = await response.json();

    if (!data.success || !data.tests || data.tests.length === 0) {
        throw new Error('No hay tests disponibles para este grupo.');
    }

    return data.tests;
}

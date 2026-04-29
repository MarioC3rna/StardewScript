const STORAGE_KEYS = {
    songData: 'stardewscript.music.songData',
    songName: 'stardewscript.music.songName',
    muted: 'stardewscript.music.muted'
};

let audioElement = null;
let uploadInput = null;
let statusLabel = null;
let muteButton = null;
let uploadButton = null;
let unlockHandlerAttached = false;

export function initializeMusicPlayer() {
    if (audioElement) {
        return;
    }

    const existingSong = localStorage.getItem(STORAGE_KEYS.songData);
    const existingName = localStorage.getItem(STORAGE_KEYS.songName);
    const storedMuted = localStorage.getItem(STORAGE_KEYS.muted);
    const isMuted = storedMuted === null ? true : storedMuted === 'true';

    audioElement = document.createElement('audio');
    audioElement.loop = true;
    audioElement.preload = 'auto';
    audioElement.muted = isMuted;
    audioElement.volume = 0.75;
    audioElement.style.display = 'none';
    document.body.appendChild(audioElement);

    const player = document.createElement('div');
    player.className = 'music-player';
    player.innerHTML = `
        <div class="music-player__title">Música</div>
        <div class="music-player__status">${existingName ? escapeHtml(existingName) : 'Sin canción cargada'}</div>
        <div class="music-player__actions">
            <button type="button" class="music-player__btn" data-action="upload">Subir canción</button>
            <button type="button" class="music-player__btn music-player__btn--mute" data-action="mute"></button>
        </div>
        <input type="file" accept="audio/*" class="music-player__file" hidden>
    `;
    document.body.appendChild(player);

    uploadInput = player.querySelector('.music-player__file');
    statusLabel = player.querySelector('.music-player__status');
    uploadButton = player.querySelector('[data-action="upload"]');
    muteButton = player.querySelector('[data-action="mute"]');

    uploadButton.addEventListener('click', () => uploadInput.click());
    uploadInput.addEventListener('change', handleSongUpload);
    muteButton.addEventListener('click', toggleMute);

    if (existingSong) {
        audioElement.src = existingSong;
        updateStatus(existingName || 'Canción cargada');
        syncMuteButton();
        tryStartPlayback();
    } else {
        updateStatus('Sube una canción para activarla');
        syncMuteButton();
    }
}

async function handleSongUpload(event) {
    const file = event.target.files && event.target.files[0];
    if (!file) {
        return;
    }

    const dataUrl = await readFileAsDataUrl(file);
    localStorage.setItem(STORAGE_KEYS.songData, dataUrl);
    localStorage.setItem(STORAGE_KEYS.songName, file.name);
    audioElement.src = dataUrl;
    updateStatus(file.name);
    tryStartPlayback();
}

function toggleMute() {
    const nextMuted = !audioElement.muted;
    audioElement.muted = nextMuted;
    localStorage.setItem(STORAGE_KEYS.muted, String(nextMuted));
    syncMuteButton();

    if (!nextMuted) {
        tryStartPlayback();
    }
}

function syncMuteButton() {
    if (!muteButton) {
        return;
    }

    muteButton.textContent = audioElement.muted ? 'Activar sonido' : 'Silenciar';
    muteButton.classList.toggle('is-muted', audioElement.muted);
}

function updateStatus(text) {
    if (statusLabel) {
        statusLabel.textContent = text;
    }
}

async function tryStartPlayback() {
    if (!audioElement.src) {
        return;
    }

    try {
        await audioElement.play();
        updateStatus(localStorage.getItem(STORAGE_KEYS.songName) || 'Reproduciendo en bucle');
    } catch (error) {
        updateStatus('Pulsa en la página para activar el sonido');
        attachUnlockHandler();
    }
}

function attachUnlockHandler() {
    if (unlockHandlerAttached) {
        return;
    }

    unlockHandlerAttached = true;
    const unlock = async () => {
        try {
            await audioElement.play();
            updateStatus(localStorage.getItem(STORAGE_KEYS.songName) || 'Reproduciendo en bucle');
            document.removeEventListener('pointerdown', unlock);
            document.removeEventListener('keydown', unlock);
            unlockHandlerAttached = false;
        } catch (error) {
            updateStatus('Pulsa en la página para activar el sonido');
        }
    };

    document.addEventListener('pointerdown', unlock, { once: true });
    document.addEventListener('keydown', unlock, { once: true });
}

function readFileAsDataUrl(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = () => reject(reader.error);
        reader.readAsDataURL(file);
    });
}

function escapeHtml(value) {
    return String(value)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}
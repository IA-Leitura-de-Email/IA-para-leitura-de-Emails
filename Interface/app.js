/* ─────────────────────────────────────────
   INTELBRAS · Agente de Suporte IA
   app.js
───────────────────────────────────────── */

// ── Relógio ──────────────────────────────
const $clock = document.getElementById('clock');
const tick = () => $clock.textContent = new Date().toLocaleTimeString('pt-BR');
tick();
setInterval(tick, 1000);

// ── Contador de caracteres ────────────────
document.getElementById('emailInput').addEventListener('input', function () {
    document.getElementById('charCount').textContent = this.value.length + ' caracteres';
});

// ── Tema claro / escuro ───────────────────
let dark = false;

function toggleTheme() {
    dark = !dark;
    document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
    document.getElementById('iconMoon').style.display = dark ? 'none'  : 'block';
    document.getElementById('iconSun').style.display  = dark ? 'block' : 'none';
}

// ── Estado global ─────────────────────────
let respostaAtual = '';

// ── Enviar para a API ─────────────────────
async function enviar() {
    const email = document.getElementById('emailInput').value.trim();
    if (!email) { showToast('Cole um e-mail antes!'); return; }

    const body = document.getElementById('respBody');
    const btn  = document.getElementById('btnGerar');
    const meta = document.getElementById('respMeta');

    btn.disabled = true;
    const t0 = Date.now();

    body.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <div class="steps">
                <div class="step active" id="s1"><div class="step-dot"></div>Lendo e-mail do cliente</div>
                <div class="step"        id="s2"><div class="step-dot"></div>Consultando base de conhecimento</div>
                <div class="step"        id="s3"><div class="step-dot"></div>Gerando resposta com IA</div>
            </div>
        </div>`;

    const advance = (n) => [1, 2, 3].forEach(i => {
        const el = document.getElementById('s' + i);
        if (el) el.className = 'step' + (i < n ? ' done' : i === n ? ' active' : '');
    });

    const t1 = setTimeout(() => advance(2), 700);
    const t2 = setTimeout(() => advance(3), 1600);

    try {
        const res  = await fetch('http://127.0.0.1:5000/perguntar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        const data = await res.json();
        const elapsed = ((Date.now() - t0) / 1000).toFixed(1);

        clearTimeout(t1);
        clearTimeout(t2);

        if (data.resposta) {
            respostaAtual = data.resposta;
            body.innerHTML = `<div class="resp-text" id="rtx"></div>`;
            typewrite(document.getElementById('rtx'), data.resposta);
            meta.textContent = `gerado em ${elapsed}s · ${data.resposta.length} chars`;
        } else {
            body.innerHTML = `<div class="empty"><p style="color:var(--err)">${data.erro || 'Resposta inválida'}</p></div>`;
            meta.textContent = 'erro na geração';
        }
    } catch {
        clearTimeout(t1);
        clearTimeout(t2);
        body.innerHTML = `
            <div class="empty">
                <p style="color:var(--err)">
                    ⚠ Servidor offline.<br>
                    Execute: <code>python Service/Mail-AgentGenerative.py</code>
                </p>
            </div>`;
        meta.textContent = 'erro de conexão';
    }

    btn.disabled = false;
}

// ── Efeito typewriter ─────────────────────
function typewrite(el, text) {
    let i = 0;
    const speed = Math.max(4, Math.min(18, 1800 / text.length));
    (function t() {
        if (i < text.length) {
            el.textContent += text[i++];
            setTimeout(t, speed);
        }
    })();
}

// ── Copiar resposta ───────────────────────
function copiar() {
    if (!respostaAtual) { showToast('Nada para copiar ainda.'); return; }
    navigator.clipboard.writeText(respostaAtual).then(() => showToast('Resposta copiada!'));
}

// ── Limpar tudo ───────────────────────────
function limpar() {
    document.getElementById('emailInput').value = '';
    document.getElementById('charCount').textContent = '0 caracteres';
    document.getElementById('respMeta').textContent = '—';
    respostaAtual = '';
    resetEmptyState();
}

function resetEmptyState() {
    document.getElementById('respBody').innerHTML = `
        <div class="empty">
            <div class="empty-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                    <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
                </svg>
            </div>
            <h3>Nenhuma resposta ainda</h3>
            <p>Cole o e-mail do cliente ao lado<br>e clique em <strong>Gerar Resposta</strong></p>
        </div>`;
}

// ── Toast ─────────────────────────────────
let toastTimer;

function showToast(msg) {
    document.getElementById('toastMsg').textContent = msg;
    const el = document.getElementById('toast');
    el.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove('show'), 2700);
}
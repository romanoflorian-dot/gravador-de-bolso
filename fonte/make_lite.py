import re, os, json, shutil
D = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(D, 'gravador-de-bolso-full.html'), encoding='utf-8').read()
def rep(a, b, count=1):
    global s
    assert a in s, 'faltou: ' + a[:70]
    s = s.replace(a, b, count)
rep('<title>Gravador de Bolso</title>', '<title>Gravador de Bolso Lite</title>')
rep('<div class="chips" id="diag" aria-live="polite"></div>', '<div class="chips" id="diag" hidden></div>')
rep('<div class="screen"><canvas id="wave" aria-label="Forma de onda; arraste para mover o início ou o fim do corte"></canvas></div>',
    '''<div class="screen"><canvas id="wave" aria-label="Forma de onda; arraste para mover o início ou o fim do corte"></canvas></div>
    <div class="wavefoot"><span class="summary" id="durLabel">Duração 0:00,0</span></div>
    <div class="ctl">
      <button class="btn primary tbtn" id="tpPlay" aria-label="Tocar"><span class="ic"></span><span class="tl">Tocar</span></button>
      <button class="btn tbtn" id="tpStop" aria-label="Parar"><svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><rect x="3" y="3" width="10" height="10" rx="1" fill="currentColor"/></svg><span>Parar</span></button>
      <button class="btn accent" id="autoTrim" disabled>Cortar</button>
      <button class="btn" id="resetTrim">Desfazer corte</button>
    </div>''')
rep('''      <div class="row">
        <button class="btn accent" id="autoTrim" disabled>Cortar manuseio sugerido</button>
        <button class="btn" id="resetTrim">Desfazer corte</button>
      </div>
''', '')
rep('Só as operações dos estúdios de música concreta da época dos gravadores de rolo (Schaeffer, Henry, GRM, anos 1950).', 'Operações tradicionais dos estúdios de música concreta da época dos gravadores de rolo.')
rep('<legend>Mixagem</legend>', '<legend>Overdub</legend>')
rep("  const box = $('#takes'); box.innerHTML = '';", "  const box = $('#takes'); box.innerHTML = '';\n  if (!takes.length) { const m = document.createElement('div'); m.className = 'sub'; m.textContent = 'Nenhuma tomada ainda. Grave ou abra um arquivo.'; box.appendChild(m); }")
rep('addTake(makeExample());', 'renderTakes(); drawWave();')
rep('<div class="row">\n      <button class="btn" id="playOrig">', '<div class="row" hidden>\n      <button class="btn" id="playOrig">')
s, n = re.subn(r'(<label class="preset">.*?<b>[^<]+</b>)<small>.*?</small>', r'\1', s); assert n == 3, n
rep('.studio-open{align-self:flex-start;', '.studio-open{align-self:center;')
rep('<button class="btn" id="exZip">', '<button class="btn" id="exZip" hidden>')
rep("$('#exShare').hidden = !shareSupported();", "$('#exShare').hidden = true;")
rep('App criado para o curso de Arte Sonora de LV/PPGAV/EBA/UFRJ por Floriano Romano',
    'App criado para a disciplina de Arte Sonora do curso de Linguagens Visuais do PPGAV/EBA/UFRJ por Floriano Romano')
rep('footer{font-size:12.5px;', '''.lite{color:var(--accent)}
.wavefoot{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}
.ctl{display:flex;flex-wrap:wrap;gap:8px}
@media (max-width:460px){.ctl{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px}.ctl .btn{padding:9px 6px;font-size:13px;justify-content:center;text-align:center;line-height:1.15}}
.tbtn svg{display:block}
.tbtn .ic{display:inline-flex}
footer{font-size:12.5px;''')
# JS: reprodução da tomada (tocar / pausar / parar) e duração
rep('const takes = []; let cur = null, idSeq = 0;', 'const takes = []; let cur = null, idSeq = 0;\nconst tp = { pos: null };')
rep('function stopPlay() { edStop();', 'function stopPlay() { edStop(); setPP(false);')
rep('cur.trimStart = a; cur.trimEnd = b; invalidate(); syncTrimInputs(); drawWave();',
    'cur.trimStart = a; cur.trimEnd = b; invalidate(); tp.pos = null; updDur(); syncTrimInputs(); drawWave();')
rep("  const box = $('#diag'); box.innerHTML = ''; if (!cur) return;", "  const box = $('#diag'); box.innerHTML = ''; if (!cur) return;\n  tp.pos = null; updDur();")
rep('/* ---------- estúdio de música concreta ---------- */', r'''/* ---------- tocar, pausar, parar ---------- */
function icPlay() { return '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M4 2.5v11l9-5.5z" fill="currentColor"/></svg>'; }
function icPause() { return '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><rect x="3.5" y="2.5" width="3" height="11" rx=".6" fill="currentColor"/><rect x="9.5" y="2.5" width="3" height="11" rx=".6" fill="currentColor"/></svg>'; }
function setPP(on) {
  const b = document.getElementById('tpPlay'); if (!b) return;
  b.querySelector('.ic').innerHTML = on ? icPause() : icPlay();
  b.querySelector('.tl').textContent = on ? 'Pausar' : 'Tocar';
  b.setAttribute('aria-label', on ? 'Pausar' : 'Tocar');
}
function updDur() {
  const el = document.getElementById('durLabel'); if (!el || !cur) return;
  const d = cur.trimEnd - cur.trimStart, full = cur.analysis.dur;
  el.textContent = 'Duração ' + fmtTime(d) + (d < full - 0.05 ? ' (de ' + fmtTime(full) + ')' : '');
}
function tpPlay() {
  const sr = cur.sr, a = cur.trimStart, b = cur.trimEnd;
  const from = (tp.pos !== null && tp.pos >= a && tp.pos < b - 0.05) ? tp.pos : a;
  playBuffer(cur.chs.map(c => c.slice(Math.floor(from * sr), Math.floor(b * sr))), sr, t => { tp.pos = from + t; return tp.pos; });
  setPP(true);
}
$('#tpPlay').onclick = () => {
  if (!cur) return;
  if (playSrc) { const keep = tp.pos; stopPlay(); tp.pos = keep; playhead = keep; drawWave(); return; }
  tpPlay();
};
$('#tpStop').onclick = () => { stopPlay(); tp.pos = null; };
setPP(false);

/* ---------- estúdio de música concreta ---------- */''')

# bloco de tratamento oculto: valores padrão aplicados automaticamente
a = s.index('    <div class="divider"></div>\n    <div class="presets"')
b = s.index('</div>\n', s.index('<label class="field" for="padPost">')) + len('</div>\n')
b = s.index('</div>\n', b) + len('</div>\n') if s[b:b+40].strip().startswith('</div>') else b
blk = s[a:b]
assert blk.count('<div class="grid2">') == 1 and 'padPost' in blk
s = s[:a] + '    <div hidden>\n' + blk + '    </div>\n' + s[b:]
rep(' Num gravador como o Zoom, desligue AUTO GAIN e COMP/LIMITER no menu.', '')

# ---------- visual preto e branco (desenho aprovado) ----------
EAR = open(os.path.join(D, 'ear_notas.svg'), encoding='utf-8').read()
rep('<span class="core"></span>', EAR)
rep("const acc = css('--accent');", "const acc = css('--screen-ink');")
s = s.replace("g.fillStyle = css('--accent');", "g.fillStyle = css('--screen-ink');")
rep('family=Archivo:wdth,wght@62..100,400..800&family=IBM+Plex+Mono:wght@400;500;600&display=swap',
    'family=Archivo:wdth,wght@62..100,400..800&family=IBM+Plex+Mono:wght@400;500;600&family=Special+Elite&family=Space+Mono:wght@400;700&display=swap')
THEME = """
/* visual preto e branco — sobrepõe os dois temas */
:root,:root:not([data-theme="light"]),:root[data-theme="dark"]{
  --bg:#ffffff; --panel:#ffffff; --ink:#000000; --ink-2:#000000; --ink-3:#000000; --line:#000000;
  --accent:#000000; --accent-ink:#ffffff; --rec:#000000; --ok:#000000; --warn:#000000; --bad:#d4281c;
  --screen:#000000; --screen-ink:#ffffff; --screen-dim:#ffffff; --screen-wave:#ffffff; --screen-off:#ffffff; --screen-cut:rgba(0,0,0,.6);
  --m-low:#6a6a6a; --m-target:#d0d0d0; --m-hot:#e5534b; --m-clip:#ff2d20;
  --f-display:"American Typewriter","Special Elite","Courier New",serif;
  --f-body:"Space Mono",ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace;
  --f-mono:"Space Mono",ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace;
  --r:16px; color-scheme:light;
}
header{align-items:center;text-align:center}
h1{font-stretch:normal;font-weight:400;font-size:clamp(30px,8vw,40px);letter-spacing:.01em;text-align:center}
.tag{text-align:center}
.mod{background:transparent;border:none;border-radius:0;padding:6px 0}
details.tips{background:transparent;border:1px solid #000;border-radius:16px}
.mod h2{font-family:var(--f-body);font-stretch:normal;font-size:12px;letter-spacing:.18em}
.btn{font:400 13px/1.2 var(--f-body);border-radius:12px;border:1px solid #000;background:#fff;color:#000;min-height:44px}
.btn:hover{border-color:#000}
.btn.primary{background:#000;color:#fff;border-color:#000;font-weight:700}
.btn.accent{background:#fff;color:#000;border-color:#000;font-weight:700}
.take{background:#fff;border:1px solid #000;border-radius:12px;min-height:46px;align-items:center}
.take[aria-current="true"]{background:#000;color:#fff;border-color:#000;box-shadow:none}
.take[aria-current="true"] .d{color:#fff}
.field input,.field select,.mini{border:1px solid #000;border-radius:12px;background:#fff;color:#000}
.screen{border-radius:12px}
.drop{border:1.5px dashed #000;border-radius:16px}
.seg{border-color:#000;border-radius:12px}
.preset span,.tool{border-color:#000;border-radius:12px;background:#fff}
.studio-open{border-radius:12px}
.recrow{justify-items:center}
.recbtn{width:112px;height:132px;border-radius:16px;border:2px solid #000;background:#fff;padding:4px;justify-self:center}
.recbtn .ear{display:block;width:98px;height:120px}
.recbtn.on::after{display:none}
.nota{opacity:0;transform-box:fill-box;transform-origin:center}
.recbtn.on .nota,#abertura .nota{animation:entra 1.6s ease-in infinite}
.recbtn.on .n2,#abertura .n2{animation-delay:.8s}
@keyframes entra{0%{opacity:0;transform:translate(0,0) scale(1) rotate(0)}15%{opacity:1}75%{opacity:1}100%{opacity:0;transform:translate(30px,52px) scale(.3) rotate(25deg)}}
@media (prefers-reduced-motion:reduce){.recbtn.on .nota,#abertura .nota{animation:none;opacity:1}}
.exrow{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.exrow .btn{justify-content:center;text-align:center;padding:10px 4px;line-height:1.15}
#abertura{position:fixed;inset:0;z-index:999;background:#fff;display:grid;place-items:center;transition:opacity .45s ease}
#abertura svg{width:150px;height:186px}
#abertura.sai{opacity:0;pointer-events:none}
footer{text-align:center;border-top:1px solid #000}
"""
rep('.hl{font-weight:600;color:var(--ink)}\n</style>', '.hl{font-weight:600;color:var(--ink)}\n' + THEME + '</style>')
s = s.replace('Os picos devem ficar na faixa laranja, entre −12 e −6 dB.', 'Os picos devem ficar entre −12 e −6 dB no medidor.')
s = s.replace(' A faixa laranja do medidor é o nível ideal.', ' O nível ideal fica entre −12 e −6 dB no medidor.')
s = s.replace('botão vermelho', 'botão da orelha')
rep('<div class="row">\n      <button class="btn primary" id="exWav24">', '<div class="row exrow">\n      <button class="btn primary" id="exWav24">')
SPL = EAR.replace('hachura', 'hachuraS').replace('tremido', 'tremidoS').replace('class="ear"', 'class="ear-ab"')
rep('<div class="wrap">', '<div class="wrap">\n<div id="abertura" aria-hidden="true">' + SPL + '</div>')
rep("$('#tpStop').onclick = () => { stopPlay(); tp.pos = null; };", "$('#tpStop').onclick = () => { stopPlay(); tp.pos = null; };\n(function () { const a = document.getElementById('abertura'); if (!a) return; setTimeout(() => a.classList.add('sai'), 1700); setTimeout(() => a.remove(), 2200); })();")
# estúdio reorganizado em grades + texto centralizado
_a = s.index('  <section class="mod" id="studio"')
_b = s.index('</section>', _a) + len('</section>')
s = s[:_a] + open(os.path.join(D, 'studio_lite.html'), encoding='utf-8').read().rstrip('\n') + s[_b:]
assert s.count('</style>') == 1
s = s.replace('</style>', open(os.path.join(D, 'lite_extra.css'), encoding='utf-8').read() + '</style>')
assert 'playOrig' in s
open(os.path.join(D, 'gravador-de-bolso-lite.html'), 'w', encoding='utf-8').write(s)
print('lite ok', len(s))

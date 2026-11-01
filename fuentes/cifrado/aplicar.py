import json,sys
D=json.load(open('/tmp/claude-0/-home-claude/e4a0f501-efa3-5cc0-b0b7-1fe68110612f/scratchpad/cifrado/teletipos.json'))
BLOCK='''/* =====================================================================
   TELETIPOS DE CLASE · cifrados. Cada uno solo se abre con la clave que
   reparte el profesor (AES-GCM; clave derivada con PBKDF2-SHA256).
   Para añadir uno: pásale a Claude el teletipo, las W y la solución, y
   te devolverá el bloque cifrado y su clave. Los textos en claro no están
   en este código.
   ===================================================================== */
const TELETIPOS_CLASE_CIFRADOS = '''+json.dumps(D['cifrados'],ensure_ascii=False)+''';
const b64bytes = s => Uint8Array.from(atob(s), c => c.charCodeAt(0));
async function abrirTeletipo(clave){
const k = String(clave||'').toUpperCase().replace(/[^A-Z0-9]/g,''); if(!k) return null;
if(!(window.crypto && crypto.subtle)) throw {code:'nocrypto'};
const base = await crypto.subtle.importKey('raw', new TextEncoder().encode(k), 'PBKDF2', false, ['deriveKey']);
for(const c of TELETIPOS_CLASE_CIFRADOS){
try{
const key = await crypto.subtle.deriveKey({name:'PBKDF2', salt:b64bytes(c.s), iterations:150000, hash:'SHA-256'}, base, {name:'AES-GCM', length:256}, false, ['decrypt']);
const pt = await crypto.subtle.decrypt({name:'AES-GCM', iv:b64bytes(c.i)}, key, b64bytes(c.d));
return JSON.parse(new TextDecoder().decode(pt));
}catch(e){}
}
return null;
}
'''
NEWFUNCS='''async function submitClassKey(){
const inp=$('classKey'), err=$('classErr'), btn=$('classGo'); if(!inp) return;
err.hidden=true; btn.disabled=true; btn.textContent='Comprobando…';
let t=null, fallo=null; try{ t = await abrirTeletipo(inp.value); }catch(e){ fallo=e; }
if(!t){
err.hidden=false; err.textContent = fallo && fallo.code==='nocrypto' ? 'Este navegador no permite abrir teletipos de clase. Prueba con Chrome o Edge actualizados.' : (inp.value.trim() ? 'Clave incorrecta. Revísala o pídesela a tu profesor.' : 'Escribe la clave que te ha dado tu profesor.');
btn.disabled=false; btn.textContent='Abrir teletipo'; inp.focus(); inp.select(); return;
}
loadStory(t, 'clase · '+t.id);
}
function toggleClassPick(){
const box=$('classPick'); if(!box) return;
box.hidden=!box.hidden; if(!box.hidden){ const i=$('classKey'); if(i) i.focus(); }
}
'''
CSS='''
/* v1.9 · Teletipo de clase con clave */
.class-pick{margin-top:12px;padding:12px 14px;background:var(--practice);border:1px solid var(--line);border-left:5px solid var(--yellow)}
.class-pick label{display:block;font-family:var(--font-slab);font-weight:850;font-size:.66rem;letter-spacing:.13em;text-transform:uppercase;color:var(--ink);margin:0 0 6px}
.key-row{display:flex;gap:8px;flex-wrap:wrap}
.key-row input{flex:1;min-width:170px;border:1.5px solid var(--line);border-radius:var(--r);padding:9px 12px;font:inherit;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--ink);background:#fff}
.key-row input::placeholder{font-weight:400;letter-spacing:.02em;text-transform:none;color:var(--muted)}
.key-row input:focus{outline:none;border-color:var(--ink)}
.class-pick .err{margin:8px 0 0}
'''
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    a=s.index('/* =====================================================================\n   TELETIPOS DE CLASE'); b=s.index('function loadStory(d, origen){')
    s=s[:a]+BLOCK+s[b:]
    a=s.index('function startClass(id){'); b=s.index('async function startStory(){')
    s=s[:a]+NEWFUNCS+s[b:]
    old=s[s.index('<div class="class-pick" id="classPick" hidden>'):s.index('<p class="err" id="startErr" hidden></p>')]
    s=s.replace(old,'<form class="class-pick" id="classPick" hidden autocomplete="off"><label for="classKey">Clave del profesor</label><div class="key-row"><input id="classKey" type="text" autocomplete="off" autocapitalize="characters" spellcheck="false" placeholder="Escribe la clave que te ha dado"><button class="btn" id="classGo" type="submit">Abrir teletipo</button></div><p class="err" id="classErr" hidden></p></form>\n',1)
    s=s.replace("box.querySelectorAll('[data-class]').forEach(b=>b.onclick=()=>startClass(b.dataset.class));","const cp = $('classPick'); if(cp) cp.onsubmit = e=>{ e.preventDefault(); submitClassKey(); };",1)
    s=s.replace('De clase: el mismo para todos, el que indique tu profesor.','De clase: el mismo para todos, con la clave que te dé tu profesor.',1)
    import re
    s=re.sub(r'<span class="ver">v1\.8( · pruebas| · L)?</span>', lambda m:'<span class="ver">v1.9'+(m.group(1) or '')+'</span>', s)
    i=s.index('</style>'); s=s[:i]+CSS+s[i:]
    for bad in ['startClass','TELETIPOS_CLASE =','Feijóo','hurones']:
        assert bad not in s, (f,bad)
    open(f,'w',encoding='utf-8').write(s); print('ok',f)

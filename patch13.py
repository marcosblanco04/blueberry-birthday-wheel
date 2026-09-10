import re

def sub(s, a, b, n=1):
    assert a in s, 'NOT FOUND: ' + a[:80].replace('\n', '\\n')
    return s.replace(a, b, n)

# ============================================================
# minigames.js
# ============================================================
f = 'minigames.js'
s = open(f, encoding='utf-8').read()
o = s

# BUG: cards only opened halfway. cos(f*PI/2) goes 1 -> 0, so a fully
# flipped card had zero width. It has to go 1 -> 0 -> 1 across the flip.
s = sub(s, "const f = c.face, sx = Math.abs(Math.cos(f*Math.PI/2));",
           "const f = c.face, sx = Math.abs(Math.cos(f*Math.PI));")

# swap in the new rhythm game (real song + sea lion interference)
start = s.index('function gameRhythm(env){')
end = s.index('/* ============================================================\n   GAME 3 - BERRY MEMORY')
s = s[:start] + open('rhythm.js', encoding='utf-8').read() + '\n' + s[end:]

# let the admin panel close the gauntlet
s = sub(s, "  inGame:function(){ return running; },",
"""  inGame:function(){ return running; },
  abort:function(){
    stopLoop(); activeFlag=false;
    ov.classList.remove('on');
    document.body.classList.remove('mg-open');
  },""")

assert s != o
open(f, 'w', encoding='utf-8').write(s)
print('minigames.js patched')

# ============================================================
# surprises.js - let the admin fire a specific event
# ============================================================
f = 'surprises.js'
s = open(f, encoding='utf-8').read()
o = s
s = sub(s, "function remaining(){ return queue.length; }",
"""function remaining(){ return queue.length; }

const NAMES = ['Upside down','Disco','Sea lions','Fake crash','Berry rain',
               'Gravity','Angry wheel','Tiny wheel','Fake chat','Delivery','Slots'];
function list(){ return NAMES.slice(); }
function play(i){
  const ev = EVENTS[i];
  if(!ev || busy) return false;
  if(typeof MG !== 'undefined' && MG.inGame && MG.inGame()) return false;
  const qi = queue.indexOf(ev); if(qi >= 0) queue.splice(qi,1);
  busy = true;
  try { ev(); } catch(e){ console.error('surprise failed', e); end(); }
  return true;
}""")
s = sub(s, """return {
  fire:fire, next:next, flush:flush, remaining:remaining,
  doubleOrNothing:doubleOrNothing,
  busy:function(){ return busy; }
};""",
"""return {
  fire:fire, next:next, flush:flush, remaining:remaining,
  list:list, play:play,
  busy:function(){ return busy; }
};""")
assert s != o
open(f, 'w', encoding='utf-8').write(s)
print('surprises.js patched')

# ============================================================
# template.html
# ============================================================
f = 'template.html'
s = open(f, encoding='utf-8').read()
o = s

# ---- prize pool: the four cheapest, Celsius is the separate final fight ----
s = sub(s, " {k:'wig',      n:'Zero Two Cosplay Wig',              s:'ZERO TWO\\nWIG',      win:1,",
           " {k:'wig',      n:'Zero Two Cosplay Wig',              s:'ZERO TWO\\nWIG',      win:1,")
s = sub(s, " {k:'celsius24',n:'24 x Celsius Peach Vibe',           s:'24x\\nCELSIUS',       win:1,",
           " {k:'celsius24',n:'24 x Celsius Peach Vibe',           s:'24x\\nCELSIUS',       final:1,")
s = sub(s, """const PRIZE_SPINS = 2;      /* spins earned back from the gauntlet */
const LOSS_SPINS  = 2;      /* spins she loses at the start */""",
"""const PRIZE_SPINS = 2;      /* spins earned back from the gauntlet */
const DON_SPINS   = 2;      /* spins from the double-or-nothing gamble */
const LOSS_SPINS  = 2;      /* spins she loses at the start */""")

# ---- five prize slots: 4 wheel prizes + the Celsius ----
s = sub(s, "  for(let i=0;i<PRIZE_SPINS;i++) h+='<div class=\"slot\"><div class=\"qm\">?</div>'+",
           "  for(let i=0;i<PRIZE_SPINS+DON_SPINS+1;i++) h+='<div class=\"slot\"><div class=\"qm\">?</div>'+")

# ---- the mega treatment belongs to the Celsius, not to spin 4 ----
s = sub(s, "  const isFinal = (spinsTaken+1 >= spinsAllowed);",
           "  const isFinal = !!item.final;")

# ---- counter ----
s = sub(s, """function updCounter(){
  if(phase==='done'){ counter.textContent='ALL DONE'; return; }
  if(phase==='gauntlet'){ counter.textContent='GAUNTLET'; return; }
  if(phase==='comeback'){
    const n = Math.min(PRIZE_SPINS, spinsTaken-comebackBase+1);
    counter.textContent = 'COMEBACK ' + n + ' / ' + PRIZE_SPINS;
    return;
  }
  counter.textContent = 'SPIN ' + (spinsTaken+1) + ' / ' + LOSS_SPINS;
}""",
"""function updCounter(){
  if(phase==='done'){ counter.textContent='ALL DONE'; return; }
  if(phase==='gauntlet'){ counter.textContent='GAUNTLET'; return; }
  if(phase==='double'){ counter.textContent='DOUBLE OR NOTHING'; return; }
  if(phase==='celsius'){ counter.textContent='FINAL PRIZE'; return; }
  if(phase==='comeback'){
    const cap = donDone ? DON_SPINS : PRIZE_SPINS;
    const n = Math.min(cap, spinsTaken-comebackBase+1);
    counter.textContent = (donDone ? 'BONUS ' : 'COMEBACK ') + n + ' / ' + cap;
    return;
  }
  counter.textContent = 'SPIN ' + (spinsTaken+1) + ' / ' + LOSS_SPINS;
}""")

# ---- phase machine ----
s = sub(s, """  if(spinsTaken>=spinsAllowed){
    phase='done'; updCounter();
    state='done';
    hub.disabled=true; hub.classList.remove('waiting','ready');
    hub.textContent='THE\\nEND';
    showFinale();
    return;
  }""",
"""  if(spinsTaken>=spinsAllowed){
    if(phase==='comeback' && !donDone){ startDoubleOrNothing(); return; }
    if(!celsiusDone){ startCelsiusIntro(); return; }
    phase='done'; updCounter();
    state='done';
    hub.disabled=true; hub.classList.remove('waiting','ready');
    hub.textContent='THE\\nEND';
    showFinale();
    return;
  }""")

# ---- markup ----
s = sub(s, '<div id="fakeWin">',
"""<div class="ov" id="donOv">
  <div id="donCard">
    <div id="donOffer">
      <div class="t">DOUBLE OR NOTHING</div>
      <div class="s">Two spins is all you get.<br>
        Unless you gamble them. <b>5%</b> chance of two more.
        <b>95%</b> chance you walk away with what you have.</div>
      <div class="oddsbar"><div class="r5"></div></div>
      <div class="row">
        <button class="btn" id="donYes">YES &mdash; RISK IT</button>
        <button class="btn pinky" id="donNo">NO, I'LL KEEP IT</button>
      </div>
    </div>
    <div id="donRoll">
      <div class="t">HIT THE 5%</div>
      <div class="s" id="donOdds">YOUR ODDS: 5%</div>
      <div id="donTrack">
        <div id="donGreen"></div>
        <div id="donNeedle"></div>
      </div>
      <div class="s" id="donResult"></div>
      <button class="btn" id="donStop">STOP IT</button>
      <div class="hintline">SPACE or click</div>
    </div>
  </div>
</div>

<div class="ov" id="celsiusOv">
  <div id="celsiusCard">
    <div class="peach">&#127825;</div>
    <div class="t" id="celsiusTag">ONE LAST THING</div>
    <div class="s" id="celsiusSub">There is a 24-pack of Peach Vibe still on that wheel.
      But the wheel has seized up. You are going to have to force it.</div>
    <button class="btn" id="celsiusBtn">GRAB THE WHEEL</button>
  </div>
</div>

<div id="mashOv">
  <div id="mashIn">
    <div class="t">BREAK IT LOOSE</div>
    <div class="s" id="mashNote"></div>
    <div id="mashBar"><div id="mashFill"></div><div id="mashMark"></div></div>
    <div id="mashTime">12.0s</div>
    <button class="btn" id="mashBtn">MASH  (or SPACE)</button>
  </div>
</div>

<div id="adminOv">
  <div id="adminIn">
    <div id="adminHead">ADMIN &mdash; hidden from stream &nbsp;<span id="adminState"></span></div>
    <div id="adminBody"></div>
  </div>
</div>

<div id="fakeWin">""")

# ---- styles ----
s = sub(s, "#help{position:fixed;left:16px;",
"""/* ---------- double or nothing ---------- */
#donCard{position:relative;text-align:center;max-width:min(760px,94vw);
  padding:clamp(20px,3vw,42px) clamp(24px,4vw,56px);border-radius:30px;border:5px solid transparent;
  transform:scale(.6);transition:.5s cubic-bezier(.15,1.7,.4,1);
  background:linear-gradient(160deg,#3a0512,#160207) padding-box,
             conic-gradient(from 0deg,#ff3355,#FFD447,#ff3355) border-box;
  animation:cardGlow .9s ease-in-out infinite}
.ov.on #donCard{transform:scale(1)}
#donCard .t{font-family:'Bungee',cursive;font-size:clamp(22px,4.4vw,58px);line-height:1;color:#ff5b7a;
  text-shadow:0 0 34px rgba(255,51,85,.9)}
#donCard .s{margin-top:12px;font-weight:800;font-size:clamp(11px,1.35vw,17px);line-height:1.6;
  color:rgba(255,255,255,.85)}
#donCard .s b{color:#FFD447}
#donCard .row{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:18px}
#donCard .hintline{margin-top:10px;font-size:11px;font-weight:800;letter-spacing:2px;
  text-transform:uppercase;color:rgba(255,255,255,.4)}
.oddsbar{margin:16px auto 0;width:min(520px,80vw);height:20px;border-radius:999px;overflow:hidden;
  background:#ff3355;border:2px solid rgba(255,255,255,.25);position:relative}
.oddsbar .r5{position:absolute;left:0;top:0;bottom:0;width:5%;background:#9DFF3C}
#donRoll{display:none}
#donTrack{position:relative;margin:18px auto;width:min(620px,86vw);height:46px;border-radius:12px;
  background:repeating-linear-gradient(90deg,#5c0d1e 0 18px,#4a0a18 18px 36px);
  border:3px solid rgba(255,255,255,.25);overflow:hidden}
#donGreen{position:absolute;top:0;bottom:0;background:linear-gradient(#c6ff6a,#4fbf00);
  box-shadow:0 0 24px rgba(157,255,60,.9)}
#donNeedle{position:absolute;top:-6px;bottom:-6px;width:6px;margin-left:-3px;border-radius:3px;
  background:#fff;box-shadow:0 0 18px #fff,0 0 40px #22E7FF}

/* ---------- the Celsius fight ---------- */
#celsiusCard{position:relative;text-align:center;max-width:min(720px,94vw);
  padding:clamp(20px,3vw,42px) clamp(24px,4vw,56px);border-radius:30px;border:5px solid transparent;
  transform:scale(.6);transition:.5s cubic-bezier(.15,1.7,.4,1);
  background:linear-gradient(160deg,#4a2410,#1c0c05) padding-box,
             conic-gradient(from 0deg,#ffb36b,#FFD447,#ff7a3d,#ffb36b) border-box;
  animation:cardGlow 1.3s ease-in-out infinite}
.ov.on #celsiusCard{transform:scale(1)}
#celsiusCard .peach{font-size:clamp(40px,7vw,86px);animation:pop 1.4s ease-in-out infinite}
#celsiusCard .t{font-family:'Bungee',cursive;font-size:clamp(20px,4vw,52px);line-height:1;color:#FFD447;
  text-shadow:0 0 30px rgba(255,212,71,.85);margin-top:4px}
#celsiusCard .s{margin-top:12px;font-weight:800;font-size:clamp(11px,1.35vw,17px);line-height:1.6;
  color:rgba(255,255,255,.85)}

#mashOv{position:fixed;inset:0;z-index:69;display:none;place-items:end center;padding-bottom:6vh;
  pointer-events:none;background:radial-gradient(circle at 50% 42%,transparent 34%,rgba(4,1,12,.72) 100%)}
#mashOv.on{display:grid}
#mashIn{pointer-events:auto;text-align:center;width:min(760px,94vw);padding:clamp(14px,2vw,26px);
  border-radius:26px;background:rgba(8,2,24,.92);border:4px solid #FFD447;
  box-shadow:0 0 60px rgba(255,212,71,.6)}
#mashIn .t{font-family:'Bungee',cursive;font-size:clamp(18px,3vw,40px);color:#FFD447;line-height:1}
#mashIn .s{margin-top:6px;font-weight:800;font-size:clamp(10px,1.2vw,15px);color:rgba(255,255,255,.75)}
#mashBar{position:relative;margin:14px auto 8px;width:100%;height:34px;border-radius:999px;
  background:rgba(255,255,255,.1);overflow:hidden;border:2px solid rgba(255,255,255,.2)}
#mashFill{position:absolute;inset:0;transform:scaleX(0);transform-origin:left center;
  background:linear-gradient(90deg,#22E7FF,#9DFF3C,#FFD447,#FF3FD0)}
#mashMark{position:absolute;top:-4px;bottom:-4px;width:5px;margin-left:-2px;background:#fff;
  box-shadow:0 0 16px #fff}
#mashTime{font-family:'Bungee',cursive;font-size:clamp(14px,2vw,26px);color:#fff}

/* ---------- admin ---------- */
#adminOv{position:fixed;inset:0;z-index:95;display:none;background:rgba(2,0,8,.9);padding:16px;
  overflow:auto}
#adminOv.on{display:block}
#adminIn{max-width:1100px;margin:0 auto;background:#0d0524;border:3px solid #8B3DFF;border-radius:18px;
  padding:16px 18px 22px}
#adminHead{font-family:'Bungee',cursive;font-size:15px;color:#FFD447;letter-spacing:1px;
  padding-bottom:10px;border-bottom:2px solid rgba(255,255,255,.12);margin-bottom:12px}
#adminHead span{font-family:'Outfit';font-weight:700;font-size:11.5px;color:rgba(255,255,255,.55);
  letter-spacing:0}
.adGroup h4{margin:14px 0 7px;font-size:11px;letter-spacing:2.5px;text-transform:uppercase;
  color:#22E7FF}
.adRow{display:flex;flex-wrap:wrap;gap:7px}
.adBtn{font-family:'Outfit';font-weight:800;font-size:12px;padding:8px 13px;border-radius:9px;
  border:2px solid rgba(255,255,255,.18);background:rgba(255,255,255,.07);color:#fff;cursor:pointer}
.adBtn:hover{background:rgba(255,212,71,.22);border-color:#FFD447}

#help{position:fixed;left:16px;""")

# ---- wiring ----
s = sub(s, "document.getElementById('lostBtn').addEventListener('click', enterGauntlet);",
"""document.getElementById('lostBtn').addEventListener('click', enterGauntlet);
document.getElementById('donYes').addEventListener('click', donAccept);
document.getElementById('donStop').onclick = donStop;
document.getElementById('celsiusBtn').addEventListener('click', function(){
  document.getElementById('celsiusOv').classList.remove('on');
  document.getElementById('dim').classList.remove('on');
  startMash();
});""")

# admin key must work even while a mini game is running, so it goes first
s = sub(s, "addEventListener('keydown', function(e){\n  if(MG.active()) return;\n  const k=e.key.toLowerCase();",
"""addEventListener('keydown', function(e){
  if(e.key === '`' || e.key === '\\u00a7' || e.key === '~' || e.key === '\\u00bd'){
    e.preventDefault(); ADMIN.toggle(); return;
  }
  if(document.getElementById('adminOv').classList.contains('on')){
    if(e.key === 'Escape'){ ADMIN.close(); }
    return;
  }
  if(MG.active()) return;
  if(state === 'don' || state === 'donRoll' || state === 'mash') return;
  const k=e.key.toLowerCase();""")

s = sub(s, "  if(k==='v'){ SUR.doubleOrNothing(); }",
           "  if(k==='v'){ startDoubleOrNothing(); }")

s = sub(s, """  <kbd>X</kbd> next surprise (<b id="surLeft">11</b> left) &nbsp; <kbd>V</kbd> double-or-nothing &nbsp;
  <kbd>B</kbd> fake-out: auto/always/never<br>""",
"""  <kbd>X</kbd> next surprise (<b id="surLeft">11</b> left) &nbsp; <kbd>V</kbd> double-or-nothing &nbsp;
  <kbd>B</kbd> fake-out: auto/always/never<br>
  <kbd>&sect;</kbd> or <kbd>`</kbd> ADMIN PANEL (jump anywhere, no replaying)<br>""")

s = sub(s, """  <span style="opacity:.6;font-size:11.5px">Flow: spin 1 FAIL &rarr; spin 2 FAIL &rarr; YOU LOST EVERYTHING
  &rarr; 5-game gauntlet (~10 min, unlimited retries, always winnable) &rarr; +2 spins,
  each a RANDOM pick from the 5 remaining prizes. Operator only &mdash; keep hidden on stream.</span>""",
"""  <span style="opacity:.6;font-size:11.5px">Flow: FAIL &rarr; FAIL &rarr; YOU LOST EVERYTHING &rarr; 5-game
  gauntlet &rarr; +2 spins &rarr; DOUBLE OR NOTHING (the NO button runs away) &rarr; she hits the 5%
  &rarr; +2 spins &rarr; Celsius mash fight &rarr; finale. Prizes are the 4 cheapest, drawn at random.
  Operator only &mdash; keep hidden on stream.</span>""")

assert s != o
open(f, 'w', encoding='utf-8').write(s)
print('template.html patched')

# ============================================================
# build.py - include endgame.js
# ============================================================
f = 'build.py'
s = open(f, encoding='utf-8').read()
o = s
s = sub(s, "      + open('surprises.js', encoding='utf-8').read())",
           "      + open('surprises.js', encoding='utf-8').read()\n"
           "      + '\\n'\n"
           "      + open('endgame.js', encoding='utf-8').read())")
assert s != o
open(f, 'w', encoding='utf-8').write(s)
print('build.py patched')

def sub(s, a, b):
    assert a in s, 'NOT FOUND: ' + a[:80].replace('\n', '\\n')
    return s.replace(a, b, 1)

# ---------------- template.html ----------------
f = 'template.html'
s = open(f, encoding='utf-8').read(); o = s

# a spin can be cut short
s = sub(s, "let spinsTaken=0, spinsAllowed=LOSS_SPINS,",
           "let FF = false;   /* fast-forward: set by the hidden 0 key */\nlet spinsTaken=0, spinsAllowed=LOSS_SPINS,")

s = sub(s, """  function frame(now){
    const e = now - t0;
    let p;
    if(HOLD_MS > 0){""",
"""  function frame(now){
    if(FF){ rot = from + dist; done(); return; }
    const e = now - t0;
    let p;
    if(HOLD_MS > 0){""")

s = sub(s, """function fakeCelebrate(item, done){
  const box = document.getElementById('fakeWin');""",
"""function fakeCelebrate(item, done){
  if(FF){ done(); return; }
  const box = document.getElementById('fakeWin');""")

s = sub(s, """function land(item){
  spinning=false; wrap.classList.remove('zoom');""",
"""function land(item){
  FF = false;
  spinning=false; wrap.classList.remove('zoom');""")

# the skip itself
s = sub(s, "/* ============================================================\n   7. WIRING",
"""/* ------------------------------------------------------------
   HIDDEN FAST-FORWARD (key 0) - one button that advances whatever
   is on screen, so the whole show can be tested in a minute.
   ------------------------------------------------------------ */
function fastForward(){
  try{
    if(MG.active()){
      if(MG.inGame()){ MG.skip(); return; }
      const card = document.getElementById('mgCard');
      if(card && card.style.display !== 'none'){ document.getElementById('mgCardBtn').click(); }
      return;
    }
    if(!started){ begin(); return; }
    switch(state){
      case 'ready':         spin(); return;
      case 'spinning':      FF = true; return;
      case 'awaitGift':     giftConfirmed(); return;
      case 'failed':        failAcknowledged(); return;
      case 'lost':          enterGauntlet(); return;
      case 'bonus':         extraAcknowledged(); return;
      case 'don':           donAccept(); return;
      case 'donRoll':       rollNeedle = greenPos; donStop(); return;
      case 'celsiusIntro':  document.getElementById('celsiusBtn').click(); return;
      case 'mash':          mashPower = 999; return;
      default: return;
    }
  }catch(e){ console.error('fast-forward', e); }
}

/* ============================================================
   7. WIRING""")

# rebind: 0 = skip, 9 = force a loss
s = sub(s, "  if(k==='0') override='FAIL';",
           "  if(k==='9') override='FAIL';")
s = sub(s, """  if(MG.active()) return;
  if(state === 'don' || state === 'donRoll' || state === 'mash') return;
  const k=e.key.toLowerCase();""",
"""  if(e.key === '0'){ e.preventDefault(); fastForward(); return; }
  if(MG.active()) return;
  if(state === 'don' || state === 'donRoll' || state === 'mash') return;
  const k=e.key.toLowerCase();""")

s = sub(s, "  <kbd>0</kbd> force FAILED &nbsp; <kbd>G</kbd> skip gauntlet",
           "  <kbd>9</kbd> force FAILED &nbsp; <kbd>G</kbd> skip gauntlet")
s = sub(s, """  <kbd>&sect;</kbd> or <kbd>`</kbd> ADMIN PANEL (jump anywhere, no replaying)<br>""",
"""  <kbd>&sect;</kbd> or <kbd>`</kbd> ADMIN PANEL &nbsp;&nbsp;
  <kbd>0</kbd> FAST-FORWARD &mdash; skips whatever is on screen<br>""")

assert s != o
open(f, 'w', encoding='utf-8').write(s)
print('template.html patched')

# ---------------- endgame.js: admin gets the same button ----------------
f = 'endgame.js'
s = open(f, encoding='utf-8').read(); o = s
s = sub(s, "    btn(r, 'Mute / unmute', function(){ Snd.muted = !Snd.muted; });",
"""    btn(r, 'Fast-forward (key 0)', function(){ closePanel(); fastForward(); });
    btn(r, 'Mute / unmute', function(){ Snd.muted = !Snd.muted; });""")
assert s != o
open(f, 'w', encoding='utf-8').write(s)
print('endgame.js patched')

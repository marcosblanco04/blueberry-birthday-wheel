# ============================================================
# Make every surprise actually happen during the show:
# shuffled queue + show-beat triggers + a finale flush.
# ============================================================

# ---------- surprises.js ----------
f = 'surprises.js'
s = open(f, encoding='utf-8').read()
o = s

old = """const EVENTS = [evUpsideDown, evDisco, evSeaLions, evFakeCrash, evBerryRain,
                evGravity, evAngryWheel, evTinyWheel, evChat, evDelivery, evSlots];
let bag = [];

function fire(){
  if(busy) return false;
  if(typeof MG !== 'undefined' && MG.active()) return false;
  if(!Snd.ctx) return false;
  if(!bag.length){ bag = EVENTS.slice(); }
  const i = (Math.random()*bag.length)|0;
  const ev = bag.splice(i,1)[0];
  busy = true;
  try { ev(); } catch(e){ console.error('surprise failed', e); end(); }
  return true;
}"""
new = """const EVENTS = [evUpsideDown, evDisco, evSeaLions, evFakeCrash, evBerryRain,
                evGravity, evAngryWheel, evTinyWheel, evChat, evDelivery, evSlots];

/* events that must never run while a mini game is on screen
   (they move or rotate things the games are drawn inside) */
const UNSAFE_IN_GAUNTLET = [evUpsideDown, evAngryWheel, evTinyWheel];

/* a shuffled queue, not a dice roll - she gets every single one */
let queue = [], lap = 0;
function reshuffle(){
  queue = EVENTS.slice();
  for(let i=queue.length-1;i>0;i--){
    const j=(Math.random()*(i+1))|0, t=queue[i]; queue[i]=queue[j]; queue[j]=t;
  }
  lap++;
}
reshuffle();

function inGauntlet(){
  return typeof MG !== 'undefined' && MG.active && MG.active();
}

function next(){
  if(busy) return false;
  if(!Snd.ctx) return false;
  if(typeof MG !== 'undefined' && MG.inGame && MG.inGame()) return false;  /* never mid-game */
  if(!queue.length) reshuffle();

  /* pick the first queued event that is safe right now */
  let idx = 0;
  if(inGauntlet()){
    idx = -1;
    for(let i=0;i<queue.length;i++){
      if(UNSAFE_IN_GAUNTLET.indexOf(queue[i]) < 0){ idx = i; break; }
    }
    if(idx < 0) return false;         /* only unsafe ones left - wait for the wheel */
  }
  const ev = queue.splice(idx,1)[0];
  busy = true;
  try { ev(); } catch(e){ console.error('surprise failed', e); end(); }
  return true;
}
const fire = next;

/* fire everything still unseen, one after another */
function flush(){
  if(!queue.length) return;
  (function step(){
    if(!queue.length) return;
    if(busy){ setTimeout(step, 700); return; }
    if(!next()){ setTimeout(step, 700); return; }
    setTimeout(step, 1400);
  })();
}
function remaining(){ return queue.length; }"""
assert old in s, 'events block not found'
s = s.replace(old, new, 1)

old2 = """function tick(){
  const now = performance.now();
  if(!nextAt){ nextAt = now + 55000 + Math.random()*45000; return; }
  if(now < nextAt) return;
  const ok = (typeof state !== 'undefined') && state === 'ready';
  if(ok && fire()) nextAt = now + 60000 + Math.random()*60000;
  else nextAt = now + 8000;
}
setInterval(tick, 1000);

return { fire:fire, doubleOrNothing:doubleOrNothing, busy:function(){ return busy; } };"""
new2 = """const OK_STATES = ['ready','awaitGift','failed','lost','gauntlet'];
function tick(){
  const now = performance.now();
  if(!nextAt){ nextAt = now + 22000; return; }
  if(now < nextAt) return;
  const ok = (typeof state !== 'undefined') && OK_STATES.indexOf(state) >= 0;
  if(ok && next()) nextAt = now + 34000 + Math.random()*22000;
  else nextAt = now + 5000;
}
setInterval(tick, 1000);

return {
  fire:fire, next:next, flush:flush, remaining:remaining,
  doubleOrNothing:doubleOrNothing,
  busy:function(){ return busy; }
};"""
assert old2 in s, 'scheduler not found'
s = s.replace(old2, new2, 1)

assert s != o
open(f, 'w', encoding='utf-8').write(s)
print('surprises.js patched')

# ---------- minigames.js ----------
f = 'minigames.js'
s = open(f, encoding='utf-8').read()
o = s

# expose whether a game loop is actually running
s = s.replace(
"""return {
  open:open,
  active:function(){ return activeFlag; },""",
"""return {
  open:open,
  active:function(){ return activeFlag; },
  inGame:function(){ return running; },""")

# a surprise must never survive into actual gameplay
s = s.replace(
"""function runStage(){
  const s = STAGES[stageIdx];
  hideCard(); fit();""",
"""function runStage(){
  const s = STAGES[stageIdx];
  document.body.classList.remove('sur-flip','sur-disco');
  try{ GRAV_MUL = 1; }catch(e){}
  hideCard(); fit();""")

# every card screen is a free slot for a surprise
s = s.replace(
"""  showCard(
    'STAGE ' + (stageIdx+1) + ' / ' + STAGES.length,""",
"""  setTimeout(function(){ try{ SUR.next(); }catch(e){} }, 900);
  showCard(
    'STAGE ' + (stageIdx+1) + ' / ' + STAGES.length,""")

s = s.replace(
"""  } else {
    showCard('STAGE CLEARED', '✔  ' + s.name,""",
"""  } else {
    setTimeout(function(){ try{ SUR.next(); }catch(e){} }, 1400);
    showCard('STAGE CLEARED', '✔  ' + s.name,""")

assert s != o
open(f, 'w', encoding='utf-8').write(s)
print('minigames.js patched')

# ---------- template.html ----------
f = 'template.html'
s = open(f, encoding='utf-8').read()
o = s

# a surprise between spins, once the wheel is armed again
s = s.replace(
"""  state='ready'; hub.disabled=false; hub.classList.remove('waiting');
  hub.classList.add('ready'); hub.textContent='SPIN';
}

/* ---------- rock bottom ---------- */""",
"""  state='ready'; hub.disabled=false; hub.classList.remove('waiting');
  hub.classList.add('ready'); hub.textContent='SPIN';
  setTimeout(function(){ try{ SUR.next(); }catch(e){} }, 1600);
}

/* ---------- rock bottom ---------- */""")

# nothing left unseen when the night ends
s = s.replace(
"  cannons(); rainConfetti(160); fireworks(8);",
"  cannons(); rainConfetti(160); fireworks(8);\n  setTimeout(function(){ try{ SUR.flush(); }catch(e){} }, 6000);")

# operator: show how many are left
s = s.replace(
"  if(k==='h') document.getElementById('help').classList.toggle('on');",
"""  if(k==='h'){
    const hp=document.getElementById('help');
    hp.classList.toggle('on');
    try{ document.getElementById('surLeft').textContent = SUR.remaining(); }catch(e){}
  }""")
s = s.replace(
"""  <kbd>X</kbd> random surprise &nbsp; <kbd>V</kbd> double-or-nothing troll &nbsp;
  <kbd>B</kbd> fake-out: auto/always/never<br>""",
"""  <kbd>X</kbd> next surprise (<b id="surLeft">11</b> left) &nbsp; <kbd>V</kbd> double-or-nothing &nbsp;
  <kbd>B</kbd> fake-out: auto/always/never<br>""")

assert s != o
open(f, 'w', encoding='utf-8').write(s)
print('template.html patched')

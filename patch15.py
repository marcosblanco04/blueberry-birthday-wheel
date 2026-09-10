def sub(s, a, b):
    assert a in s, 'NOT FOUND: ' + a[:70].replace('\n', '\\n')
    return s.replace(a, b, 1)

# 1. once the Celsius is won and paid for, the night is over - no matter
#    what the spin counters say.
f = 'template.html'
s = open(f, encoding='utf-8').read(); o = s
s = sub(s, """  if(spinsTaken>=spinsAllowed){
    if(phase==='comeback' && !donDone){ startDoubleOrNothing(); return; }
    if(!celsiusDone){ startCelsiusIntro(); return; }
    phase='done'; updCounter();
    state='done';
    hub.disabled=true; hub.classList.remove('waiting','ready');
    hub.textContent='THE\\nEND';
    showFinale();
    return;
  }""",
"""  if(celsiusDone){
    phase='done'; updCounter();
    state='done';
    hub.disabled=true; hub.classList.remove('waiting','ready');
    hub.textContent='THE\\nEND';
    showFinale();
    return;
  }
  if(spinsTaken>=spinsAllowed){
    if(phase==='comeback' && !donDone){ startDoubleOrNothing(); return; }
    startCelsiusIntro();
    return;
  }""")
assert s != o
open(f, 'w', encoding='utf-8').write(s)
print('template.html patched')

# 2 + 3. surprises must never touch a spin in progress
f = 'surprises.js'
s = open(f, encoding='utf-8').read(); o = s
s = sub(s, """function next(){
  if(busy) return false;
  if(!Snd.ctx) return false;""",
"""function next(){
  if(busy) return false;
  if(!Snd.ctx) return false;
  if(typeof spinning !== 'undefined' && spinning) return false;   /* never mid-spin */""")
s = sub(s, """function play(i){
  const ev = EVENTS[i];
  if(!ev || busy) return false;""",
"""function play(i){
  const ev = EVENTS[i];
  if(!ev || busy) return false;
  if(typeof spinning !== 'undefined' && spinning) return false;""")
s = sub(s, """  const iv = setInterval(function(){
    rot -= .09;
    if(Math.random()<.3) Snd.clack(.8);
    if(performance.now()-t0 > 5200){""",
"""  const iv = setInterval(function(){
    if(spinning){                       /* a spin started - get out of its way */
      clearInterval(iv);
      end(function(){ idleSpin = old; document.getElementById('redveil').style.opacity = 0; });
      return;
    }
    rot -= .09;
    if(Math.random()<.3) Snd.clack(.8);
    if(performance.now()-t0 > 5200){""")
assert s != o
open(f, 'w', encoding='utf-8').write(s)
print('surprises.js patched')

import io, re

p = 'template.html'
s = open(p, encoding='utf-8').read()
o = s

start = s.index("/* ============================================================\n   3. WHEEL RENDERING")
end = s.index("/* ============================================================\n   5. MAIN LOOP")

new = open('section34.js', encoding='utf-8').read()
s = s[:start] + new + s[end:]

# main loop: track fps for the quality budget
s = s.replace(
"""  const dt=Math.min((now-last)/1000,.05); last=now;
  if(!spinning && idleSpin) rot += dt*.16;""",
"""  const dt=Math.min((now-last)/1000,.05); last=now;
  if(dt>0) fpsAvg = fpsAvg*.94 + (1/dt)*.06;
  if(!spinning && idleSpin) rot += dt*.16;""")

# confetti volumes
for a, b in [
    ("  rainConfetti(220);\n", "  rainConfetti(110);\n"),
    ("setTimeout(function(){rainConfetti(240);},600);", "setTimeout(function(){rainConfetti(90);},600);"),
    ("setTimeout(function(){rainConfetti(240);},1400);", "setTimeout(function(){rainConfetti(90);},1400);"),
    ("fireworks(7);", "fireworks(5);"),
    ("burst(innerWidth/2,innerHeight*.98,150,", "burst(innerWidth/2,innerHeight*.98,90,"),
    ("burst(innerWidth*.5,innerHeight*.98,150,", "burst(innerWidth*.5,innerHeight*.98,80,"),
    ("rainConfetti(150); burst(innerWidth/2,120,120,", "rainConfetti(80); burst(innerWidth/2,120,70,"),
    ("setTimeout(function(){ rainConfetti(320); fireworks(5); Snd.jackpot(); },250);",
     "setTimeout(function(){ rainConfetti(150); fireworks(4); Snd.jackpot(); },250);"),
    ("rainConfetti(120);\n  setTimeout(function(){ startEl.remove(); },600);",
     "rainConfetti(70);\n  setTimeout(function(){ startEl.remove(); },600);"),
    ("if(k==='c'){ cannons(); rainConfetti(220); fireworks(3); }",
     "if(k==='c'){ cannons(); rainConfetti(120); fireworks(3); }"),
]:
    s = s.replace(a, b)

# reuse a single noise buffer instead of allocating one per sound
s = s.replace(
"""  noiseBuf(sec){
    const sr=this.ctx.sampleRate, b=this.ctx.createBuffer(1,Math.max(1,Math.floor(sr*sec)),sr), d=b.getChannelData(0);
    for(let i=0;i<d.length;i++) d[i]=Math.random()*2-1; return b;
  },""",
"""  _nb:null,
  noiseBuf(){
    if(this._nb) return this._nb;
    const sr=this.ctx.sampleRate, b=this.ctx.createBuffer(1,sr*2,sr), d=b.getChannelData(0);
    for(let i=0;i<d.length;i++) d[i]=Math.random()*2-1;
    this._nb=b; return b;
  },""")
s = s.replace(
    "const t=(when||this.t), s=this.ctx.createBufferSource(); s.buffer=this.noiseBuf(Math.max(dur,.05));",
    "const t=(when||this.t), s=this.ctx.createBufferSource(); s.buffer=this.noiseBuf();")
s = s.replace(
    "    s.start(t); s.stop(t+dur+.03);\n  },\n  tone(",
    "    s.start(t, Math.random()*(2-Math.min(dur,1.5))); s.stop(t+dur+.03);\n  },\n  tone(")
s = s.replace(
    "const t=this.t, s=this.ctx.createBufferSource(); s.buffer=this.noiseBuf(1.1);",
    "const t=this.t, s=this.ctx.createBufferSource(); s.buffer=this.noiseBuf();")
s = s.replace(
    "g.gain.exponentialRampToValueAtTime(.0001,t+1.1); s.start(t); s.stop(t+1.2);",
    "g.gain.exponentialRampToValueAtTime(.0001,t+1.1); s.start(t,Math.random()*.5); s.stop(t+1.2);")

# tracker: mystery slots, revealed only when won
s = s.replace(
"""function buildTracker(){
  document.getElementById('tracker').innerHTML = ['sealion','jersey','bangle'].map(function(k){
    const it=ITEMS[idxOf(k)];
    return '<div class="slot" data-k="'+k+'"><img src="'+(A[k]||'')+'" alt="">'+
      '<div><div class="nm">'+it.n+'</div><div class="st">LOCKED</div></div></div>';
  }).join('');
}
function markTracker(k){
  const el=document.querySelector('.slot[data-k="'+k+'"]');
  if(el){ el.classList.add('won'); el.querySelector('.st').textContent='WON!'; }
}""",
"""function buildTracker(){
  let h='';
  for(let i=0;i<3;i++) h+='<div class="slot"><div class="qm">?</div>'+
    '<div><div class="nm">MYSTERY PRIZE</div><div class="st">LOCKED</div></div></div>';
  document.getElementById('tracker').innerHTML=h;
}
function markTracker(k){
  const el=document.querySelector('#tracker .slot:not(.won)');
  if(!el) return;
  el.classList.add('won');
  el.innerHTML='<img src="'+(A[k]||'')+'" alt=""><div><div class="nm">'+
    ITEMS[idxOf(k)].n+'</div><div class="st">WON!</div></div>';
}""")

s = s.replace(
""".slot img{width:clamp(30px,3.4vw,46px);height:clamp(30px,3.4vw,46px);object-fit:contain;
  border-radius:9px;background:#fff;padding:3px;filter:grayscale(1) brightness(.55);transition:.45s}""",
""".slot img{width:clamp(30px,3.4vw,46px);height:clamp(30px,3.4vw,46px);object-fit:contain;
  border-radius:9px;background:#fff;padding:3px;transition:.45s}
.slot .qm{width:clamp(30px,3.4vw,46px);height:clamp(30px,3.4vw,46px);border-radius:9px;
  background:rgba(255,255,255,.07);display:grid;place-items:center;
  font-family:'Bungee',cursive;font-size:clamp(14px,1.6vw,22px);color:rgba(255,255,255,.35)}""")

assert s != o, 'nothing changed'
open(p, 'w', encoding='utf-8').write(s)
print('patched ok')

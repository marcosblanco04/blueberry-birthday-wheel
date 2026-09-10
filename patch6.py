p = 'template.html'
s = open(p, encoding='utf-8').read()
o = s

# ---------------- START SCREEN: "ARE YOU FEELING LUCKY?" ----------------
s = s.replace(
"""<div id="start">
  <div>
    <h2>HAPPY BIRTHDAY BLUE</h2>
    <p>Click anywhere to arm the wheel</p>
    <div class="tapdot">&#127914;</div>
  </div>
</div>""",
"""<div id="start">
  <div>
    <div class="preline">BLUEBERRY BIRTHDAY SPECIAL</div>
    <h2>ARE YOU<br>FEELING LUCKY?</h2>
    <p>Click anywhere to find out, Blue</p>
    <div class="tapdot">&#127920;</div>
  </div>
</div>

<div id="intro"><div id="introText"></div></div>""")

s = s.replace(
"""#start h2{font-family:'Bungee',cursive;font-size:clamp(24px,5vw,66px);margin:0 0 10px;""",
"""#start .preline{font-family:'Bungee',cursive;letter-spacing:6px;font-size:clamp(9px,1.2vw,15px);
  color:#FFD447;margin-bottom:14px;opacity:.85;animation:pop 2.4s ease-in-out infinite}
#start h2{font-family:'Bungee',cursive;font-size:clamp(28px,6.4vw,86px);line-height:1;margin:0 0 14px;""")

s = s.replace(
"""#help{position:fixed;left:16px;""",
"""#intro{position:fixed;inset:0;z-index:88;display:none;place-items:center;text-align:center;
  background:radial-gradient(circle at 50% 45%,#180546,#05010f 72%)}
#intro.on{display:grid}
#introText{font-family:'Bungee',cursive;font-size:clamp(30px,7vw,104px);line-height:1;padding:0 6vw;
  background:linear-gradient(92deg,var(--pink),var(--gold),var(--cyan),var(--purple),var(--pink));
  background-size:300% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;
  animation:flow 2.4s linear infinite;filter:drop-shadow(0 0 30px rgba(255,63,208,.65))}
#introText.hit{animation:flow 2.4s linear infinite, slam .42s cubic-bezier(.2,1.8,.35,1)}
@keyframes slam{0%{transform:scale(2.4) rotate(-6deg);opacity:0}60%{transform:scale(.93) rotate(1.5deg);opacity:1}100%{transform:scale(1) rotate(0)}}

#sumCard{position:relative;text-align:center;max-width:min(1100px,95vw);max-height:94vh;overflow:auto;
  padding:clamp(18px,2.6vw,34px);border-radius:32px;border:5px solid transparent;
  transform:scale(.6);transition:.6s cubic-bezier(.15,1.7,.4,1);
  background:linear-gradient(160deg,#2b0a5e,#12032e) padding-box,
             conic-gradient(from 0deg,#FFD447,#FF3FD0,#22E7FF,#8B3DFF,#9DFF3C,#FFD447) border-box;
  animation:cardGlow 1.4s ease-in-out infinite}
.ov.on #sumCard{transform:scale(1)}
#sumTag{font-family:'Bungee',cursive;font-size:clamp(22px,4.6vw,64px);line-height:1;
  background:linear-gradient(92deg,var(--gold),#fff,var(--pink),var(--cyan),var(--gold));
  background-size:300% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;
  animation:flow 2s linear infinite;filter:drop-shadow(0 0 26px rgba(255,212,71,.8))}
#sumLove{font-family:'Bungee',cursive;font-size:clamp(16px,3vw,40px);color:#FF6FDD;margin-top:6px;
  text-shadow:0 0 30px rgba(255,63,208,.9);animation:pop 1.2s ease-in-out infinite}
#sumSub{margin:14px 0 12px;font-weight:800;letter-spacing:3px;text-transform:uppercase;
  font-size:clamp(9px,1.1vw,13px);color:var(--cyan)}
#sumGrid{display:flex;flex-wrap:wrap;justify-content:center;gap:clamp(8px,1.4vw,18px)}
.sumItem{width:clamp(118px,15vw,180px);background:rgba(255,255,255,.06);border:2px solid rgba(255,212,71,.5);
  border-radius:18px;padding:10px 8px;box-shadow:0 0 22px rgba(255,212,71,.25)}
.sumItem img{width:100%;height:clamp(80px,10vh,110px);object-fit:contain;background:#fff;
  border-radius:12px;padding:5px}
.sumItem .t{margin-top:7px;font-weight:900;font-size:clamp(9px,.95vw,12.5px);line-height:1.2}
#sumFoot{margin-top:16px;font-weight:800;font-size:clamp(11px,1.3vw,17px);color:#ffe9a8}

#help{position:fixed;left:16px;""")

# ---------------- markup: summary overlay ----------------
s = s.replace(
"""<div id="giftBanner">""",
"""<div class="ov" id="sumOv">
  <div id="sumCard">
    <div id="sumTag">HAPPY BIRTHDAY BLUE</div>
    <div id="sumLove">I LOVE YOU &#10084;&#65039;</div>
    <div id="sumSub">Everything you won tonight</div>
    <div id="sumGrid"></div>
    <div id="sumFoot">Every single one of them is getting bought. Happy birthday, my love. &#129744;</div>
  </div>
</div>

<div id="giftBanner">""")

# ---------------- intro sequence on first click ----------------
s = s.replace(
"""function begin(){
  if(started) return; started=true;
  Snd.init(); Snd.ctx.resume();
  startEl.classList.add('gone');
  Snd.ding(660,undefined,.8); Snd.ding(990,Snd.t+.12,.8);
  rainConfetti(70);
  setTimeout(function(){ startEl.remove(); },600);
}""",
"""const INTRO_BEATS = ['TONIGHT...', 'ONE WHEEL.', 'REAL PRIZES.', 'GOOD LUCK, BLUE'];
function runIntro(){
  const box=document.getElementById('intro'), txt=document.getElementById('introText');
  box.classList.add('on');
  INTRO_BEATS.forEach(function(line,i){
    setTimeout(function(){
      txt.textContent=line;
      txt.classList.remove('hit'); void txt.offsetWidth; txt.classList.add('hit');
      Snd.tone(70+i*22,.5,.42,'sine',undefined,32);
      Snd.noise(.35,500+i*260,.9,.2,'lowpass');
      flashScreen(.22);
      if(i===INTRO_BEATS.length-1){ Snd.ding(880,undefined,1); burst(innerWidth/2,innerHeight/2,90,{speed:16,g:.2}); }
    }, 260+i*900);
  });
  setTimeout(function(){
    box.style.transition='opacity .5s'; box.style.opacity=0;
    Snd.whoosh(); rainConfetti(70);
    setTimeout(function(){ box.remove(); },550);
  }, 260+INTRO_BEATS.length*900+520);
}
function begin(){
  if(started) return; started=true;
  Snd.init(); Snd.ctx.resume();
  startEl.classList.add('gone');
  Snd.ding(660,undefined,.8); Snd.ding(990,Snd.t+.12,.8);
  setTimeout(function(){ startEl.remove(); },600);
  runIntro();
}""")

# ---------------- remember what was won ----------------
s = s.replace(
"""function markTracker(k){
  const el=document.querySelector('#tracker .slot:not(.won)');""",
"""const WON=[];
function markTracker(k){
  if(WON.indexOf(k)<0) WON.push(k);
  const el=document.querySelector('#tracker .slot:not(.won)');""")

# ---------------- final card button wording ----------------
s = s.replace(
"""  document.getElementById('winCard').classList.toggle('mega', isFinal);""",
"""  document.getElementById('winCard').classList.toggle('mega', isFinal);
  document.getElementById('winBtn').textContent = isFinal
    ? 'GIFT BOUGHT - SHOW THE FINALE'
    : 'GIFT BOUGHT - NEXT SPIN';""")

# ---------------- the finale ----------------
s = s.replace(
"""  if(step>=SEQUENCE.length){
    state='done';
    hub.disabled=true; hub.classList.remove('waiting','ready');
    hub.textContent='THE\\nEND';
    setTimeout(function(){ rainConfetti(150); fireworks(4); Snd.jackpot(); },250);
    return;
  }""",
"""  if(step>=SEQUENCE.length){
    state='done';
    hub.disabled=true; hub.classList.remove('waiting','ready');
    hub.textContent='THE\\nEND';
    showFinale();
    return;
  }""")

s = s.replace(
"""function giftConfirmed(){""",
"""function showFinale(){
  let g='';
  WON.forEach(function(k){
    const it=ITEMS[idxOf(k)];
    g+='<div class="sumItem"><img src="'+(A[k]||'')+'" alt=""><div class="t">'+it.n+'</div></div>';
  });
  document.getElementById('sumGrid').innerHTML=g;
  document.getElementById('dim').classList.add('on');
  document.getElementById('rays').classList.add('on');
  winMode=true;
  chaos(16);
  Snd.fanfare(); Snd.jackpot(); Snd.yippee();
  setTimeout(function(){ Snd.yippee(); },2200);
  cannons(); rainConfetti(160); fireworks(8);
  setTimeout(function(){ document.getElementById('sumOv').classList.add('on'); },500);
}

function giftConfirmed(){""")

assert s != o, 'nothing changed'
open(p, 'w', encoding='utf-8').write(s)
print('patched ok')

p = 'template.html'
s = open(p, encoding='utf-8').read()
o = s

# ---------- 1. sequence + items ----------
s = s.replace(
"const SEQUENCE = ['sealion', 'FAIL', 'jersey', 'bangle'];",
"const SEQUENCE = ['sealion', 'FAIL', 'jersey', 'EXTRA', 'cowboy', 'bangle'];")

s = s.replace(
" {k:'cowboy',   n:'Cowboy Hat (Brown)',                s:'COWBOY\\nHAT'},",
" {k:'cowboy',   n:'Cowboy Hat - Brown',                s:'COWBOY\\nHAT',      win:1, url:'https://throne.com/blueberryvibezz/item/7d355302-b8a2-423b-896f-b2d9bd3c9b4c'},")

# the secret bonus slice
s = s.replace(
" {k:'wig',      n:'Zero Two Cosplay Wig',              s:'ZERO TWO\\nWIG'},",
" {k:'EXTRA',    n:'SECRET EXTRA SPIN',                 s:'EXTRA\\nSPIN', extra:1},\n"
" {k:'wig',      n:'Zero Two Cosplay Wig',              s:'ZERO TWO\\nWIG'},")

# ---------- 2. the bonus slice looks like gold ----------
s = s.replace(
"""    if(it.fail){ grad.addColorStop(0,'#2b0008'); grad.addColorStop(.6,'#7a001c'); grad.addColorStop(1,'#12000a'); }
    else { const c=PAL[i%PAL.length];""",
"""    if(it.fail){ grad.addColorStop(0,'#2b0008'); grad.addColorStop(.6,'#7a001c'); grad.addColorStop(1,'#12000a'); }
    else if(it.extra){ grad.addColorStop(0,'#fffbe6'); grad.addColorStop(.35,'#FFD447'); grad.addColorStop(1,'#a35c00'); }
    else { const c=PAL[i%PAL.length];""")
s = s.replace(
"""    } else if(it.fail){
      ctx.save(); ctx.translate(ix,0); ctx.rotate(Math.PI/2);
      ctx.font=(R*.15)+'px serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
      ctx.fillText('💀',0,0); ctx.restore();
    }""",
"""    } else if(it.fail || it.extra){
      ctx.save(); ctx.translate(ix,0); ctx.rotate(Math.PI/2);
      ctx.font=(R*.15)+'px serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
      ctx.fillText(it.fail?'💀':'⭐',0,0); ctx.restore();
    }""")
s = s.replace(
"    ctx.fillStyle= it.fail?'#ffd2da' : '#ffffff';",
"    ctx.fillStyle= it.fail?'#ffd2da' : (it.extra?'#3a1f00':'#ffffff');")
s = s.replace(
"    ctx.strokeStyle='rgba(0,0,0,.62)';\n    ctx.fillStyle= it.fail",
"    ctx.strokeStyle= it.extra?'rgba(255,255,255,.85)':'rgba(0,0,0,.62)';\n    ctx.fillStyle= it.fail")

# ---------- 3. routing: extra spin is its own outcome ----------
s = s.replace(
"""  if(item.fail) doFail(); else doWin(item);""",
"""  if(item.fail) doFail();
  else if(item.extra) doExtra();
  else doWin(item);""")

# ---------- 4. final win = total chaos ----------
s = s.replace(
"""function doWin(item){
  winMode=true; state='awaitGift';
  shake(); flashScreen(1);""",
"""let chaosTimer=null, chaosEnd=0;
function chaos(sec){
  chaosEnd=performance.now()+sec*1000;
  document.body.classList.add('chaos');
  winMode=true;
  if(chaosTimer) return;
  chaosTimer=setInterval(function(){
    if(performance.now()>chaosEnd){
      clearInterval(chaosTimer); chaosTimer=null;
      document.body.classList.remove('chaos'); return;
    }
    if(Math.random()<.5) burst(Math.random()*innerWidth, innerHeight*(.15+Math.random()*.75), 40,
        {speed:16,g:.22,coin:.3,emoji:.22});
    else cannons();
    rainConfetti(45);
    shake();
    flashScreen(.18+Math.random()*.28, Math.random()<.5?'#ffffff':'#FF3FD0');
    Snd.ding(500+Math.random()*1200,undefined,.85);
    if(Math.random()<.4) Snd.coins(8);
    if(Math.random()<.22) Snd.fanfare();
  }, 330);
}

function doWin(item){
  const isFinal = (step === SEQUENCE.length-1);
  winMode=true; state='awaitGift';
  shake(); flashScreen(1);""")

s = s.replace(
"""  } else {
    document.getElementById('winTag').textContent='YOU WON!!!';
  }
  document.getElementById('dim').classList.add('on');
  setTimeout(function(){ document.getElementById('winOv').classList.add('on'); }, 520);""",
"""  } else if(isFinal){
    document.getElementById('winTag').textContent='MEGA JACKPOT!!!';
  } else {
    document.getElementById('winTag').textContent='YOU WON!!!';
  }
  document.getElementById('winCard').classList.toggle('mega', isFinal);
  document.getElementById('winSub').textContent = isFinal
    ? 'THE BIG ONE - THE DREAM ITEM - IT IS YOURS'
    : 'Real prize - getting bought right now';
  if(isFinal){
    chaos(20);
    Snd.jackpot(); setTimeout(function(){Snd.fanfare();},1500);
    setTimeout(function(){Snd.jackpot();},3000);
    fireworks(10);
  }
  document.getElementById('dim').classList.add('on');
  setTimeout(function(){ document.getElementById('winOv').classList.add('on'); }, isFinal?1300:520);""")

# ---------- 5. the secret extra spin screen ----------
s = s.replace(
"""function buildTracker(){""",
"""function doExtra(){
  state='bonus'; winMode=true;
  shake(); flashScreen(1,'#FFD447');
  document.getElementById('rays').classList.add('on');
  Snd.jackpot(); Snd.coins(22);
  cannons(); setTimeout(cannons,300);
  rainConfetti(120,45);
  setTimeout(function(){ burst(innerWidth/2,innerHeight*.98,110,
    {dir:-Math.PI/2,spread:2.1,speed:24,g:.34,lift:5,coin:.75,emoji:.1,hue:45}); },120);
  fireworks(4);
  for(let i=0;i<4;i++) setTimeout(function(){ shake(); flashScreen(.3,'#FFD447'); }, 350+i*400);
  document.getElementById('dim').classList.add('on');
  setTimeout(function(){ document.getElementById('extraOv').classList.add('on'); },500);
  hub.disabled=true; hub.textContent='...';
}
function extraAcknowledged(){
  if(state!=='bonus') return;
  document.getElementById('extraOv').classList.remove('on');
  document.getElementById('dim').classList.remove('on');
  armNext();
}

function buildTracker(){""")

# 4 prize slots now (sea lion, jersey, cowboy hat, bangles)
s = s.replace("  for(let i=0;i<3;i++) h+='<div class=\"slot\"><div class=\"qm\">?</div>'+",
              "  for(let i=0;i<4;i++) h+='<div class=\"slot\"><div class=\"qm\">?</div>'+")

# ---------- 6. wiring ----------
s = s.replace(
"document.getElementById('failBtn').addEventListener('click', failAcknowledged);",
"document.getElementById('failBtn').addEventListener('click', failAcknowledged);\ndocument.getElementById('extraBtn').addEventListener('click', extraAcknowledged);")
s = s.replace(
"""    if(state==='ready') spin();
    else if(state==='awaitGift') giftConfirmed();
    else if(state==='failed') failAcknowledged();
    return;""",
"""    if(state==='ready') spin();
    else if(state==='awaitGift') giftConfirmed();
    else if(state==='failed') failAcknowledged();
    else if(state==='bonus') extraAcknowledged();
    return;""")
s = s.replace(
"""    if(state==='awaitGift') giftConfirmed();
    else if(state==='failed') failAcknowledged();
    else if(!started) begin();
    return;""",
"""    if(state==='awaitGift') giftConfirmed();
    else if(state==='failed') failAcknowledged();
    else if(state==='bonus') extraAcknowledged();
    else if(!started) begin();
    return;""")
s = s.replace("  if(k==='3') override='bangle';",
              "  if(k==='3') override='cowboy';\n  if(k==='4') override='bangle';\n  if(k==='5') override='EXTRA';")

# ---------- 7. markup ----------
s = s.replace(
"""<div id="giftBanner">""",
"""<div class="ov" id="extraOv">
  <div id="extraCard">
    <div class="starz">&#11088;</div>
    <div id="extraTag">SECRET<br>EXTRA SPIN!</div>
    <div id="extraSub">The wheel likes you &mdash; you get one more, free</div>
    <button class="btn" id="extraBtn">SPIN AGAIN!</button>
  </div>
</div>

<div id="giftBanner">""")

s = s.replace(
'<div class="sub">Happy Birthday Blue &nbsp;&bull;&nbsp; 3 Real Prizes &nbsp;&bull;&nbsp; Winners Get Bought Live</div>',
'<div class="sub">Happy Birthday Blue &nbsp;&bull;&nbsp; Mystery Prizes &nbsp;&bull;&nbsp; Winners Get Bought Live</div>')

s = s.replace(
"""  <kbd>1</kbd> force Sea Lion &nbsp; <kbd>2</kbd> force Jersey &nbsp; <kbd>3</kbd> force Bangles<br>
  <kbd>0</kbd> force FAILED &nbsp; <kbd>R</kbd> full reset &nbsp; <kbd>M</kbd> mute<br>
  <kbd>F</kbd> fullscreen &nbsp; <kbd>C</kbd> confetti test &nbsp; <kbd>H</kbd> hide this<br>
  <span style="opacity:.6;font-size:11.5px">Scripted order: Sea Lion &rarr; FAILED &rarr; Jersey &rarr; Bangles.
  Only those 3 can ever be won &mdash; every other slice is decoration.</span>""",
"""  <kbd>1</kbd> Sea Lion &nbsp; <kbd>2</kbd> Jersey &nbsp; <kbd>3</kbd> Cowboy Hat &nbsp; <kbd>4</kbd> Bangles<br>
  <kbd>5</kbd> Extra Spin &nbsp; <kbd>0</kbd> FAILED &nbsp; <kbd>R</kbd> full reset &nbsp; <kbd>M</kbd> mute<br>
  <kbd>F</kbd> fullscreen &nbsp; <kbd>C</kbd> confetti test &nbsp; <kbd>H</kbd> hide this<br>
  <span style="opacity:.6;font-size:11.5px">Order: Sea Lion &rarr; FAILED &rarr; Jersey &rarr; SECRET EXTRA SPIN
  &rarr; Cowboy Hat &rarr; Bangles (total chaos). Nothing else can ever be won.
  Operator only &mdash; keep this hidden on stream.</span>""")

# ---------- 8. styles ----------
s = s.replace(
"""#failCard{position:relative;text-align:center;transform:scale(.6);transition:.45s cubic-bezier(.15,1.7,.4,1)}""",
"""#failCard{position:relative;text-align:center;transform:scale(.6);transition:.45s cubic-bezier(.15,1.7,.4,1);
  padding:clamp(30px,6vw,80px);border-radius:50%;
  background:radial-gradient(circle,rgba(12,0,7,.9) 0%,rgba(12,0,7,.72) 45%,rgba(12,0,7,0) 72%)}

#extraCard{position:relative;text-align:center;transform:scale(.6) rotate(6deg);
  transition:.55s cubic-bezier(.15,1.7,.4,1);max-width:min(820px,94vw);
  padding:clamp(20px,3vw,44px) clamp(24px,4vw,60px);border-radius:32px;border:5px solid transparent;
  background:linear-gradient(160deg,#3a2400,#170c00) padding-box,
             conic-gradient(from 0deg,#fff6c2,#FFD447,#ff9d2e,#FFD447,#fff6c2) border-box;
  animation:cardGlow 1.1s ease-in-out infinite}
.ov.on #extraCard{transform:scale(1) rotate(0)}
.starz{font-size:clamp(38px,6vw,80px);animation:pop .5s ease-in-out infinite}
#extraTag{font-family:'Bungee',cursive;font-size:clamp(26px,5.4vw,74px);line-height:1;margin-top:4px;
  background:linear-gradient(92deg,#fff,#FFD447,#fff,#ff9d2e,#fff);background-size:300% 100%;
  -webkit-background-clip:text;background-clip:text;color:transparent;
  animation:flow 1.6s linear infinite;filter:drop-shadow(0 0 30px rgba(255,212,71,.95))}
#extraSub{margin-top:10px;font-weight:800;letter-spacing:2.4px;text-transform:uppercase;
  font-size:clamp(9px,1.1vw,14px);color:#ffe9a8}

#winCard.mega{animation:cardGlow .55s ease-in-out infinite, megaPulse .5s ease-in-out infinite}
@keyframes megaPulse{0%,100%{transform:scale(1) rotate(-.9deg)}50%{transform:scale(1.045) rotate(.9deg)}}
#winCard.mega #winTag{font-size:clamp(28px,5.6vw,80px);animation:flow .9s linear infinite}
body.chaos .bg{animation:chaosHue .9s linear infinite}
@keyframes chaosHue{to{filter:hue-rotate(360deg) saturate(1.7) brightness(1.15)}}
body.chaos #dim{animation:chaosDim .35s steps(2) infinite}
@keyframes chaosDim{0%{opacity:.95}100%{opacity:.6}}""")

assert s != o, 'nothing changed'
open(p, 'w', encoding='utf-8').write(s)
print('patched ok')

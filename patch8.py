import io

# ---------- small fixes in minigames.js ----------
mg = open('minigames.js', encoding='utf-8').read()
mg0 = mg
mg = mg.replace(
    "    stopLoop(); showResult(true, 'GLITCH IN THE MATRIX - free pass!');",
    "    stopLoop(); stageWin();")
mg = mg.replace(
    "        Snd.seaLionLaugh(undefined,.5) || Snd.bark();\n        Snd.ding(900+Math.random()*400,undefined,.5);",
    "        if(hits%5===0){ Snd.seaLionLaugh(undefined,.35); } else { Snd.bark(); }\n"
    "        Snd.ding(900+Math.random()*400,undefined,.5);")
assert mg != mg0
open('minigames.js', 'w', encoding='utf-8').write(mg)

# ---------- main template ----------
p = 'template.html'
s = open(p, encoding='utf-8').read()
o = s

# ============ 1. CONFIG: what can be won ============
old_cfg_start = s.index("const SEQUENCE = ")
old_cfg_end = s.index("const N = ITEMS.length")
new_cfg = '''/* ------------------------------------------------------------
   WHAT CAN BE WON
   alreadyWon:1  -> shown on the wheel stamped ALREADY WON, never winnable
   win:1         -> in the random prize pool
   Everything else is decoration: it is on the wheel but can never land.
   ------------------------------------------------------------ */
const ITEMS = [
 {k:'sealion',  n:'Sea Lion Sound Plush Toy',          s:'SEA LION\\nPLUSH',    alreadyWon:1},
 {k:'ps5',      n:'Blueberryvibezz PS5 Controller',    s:'PS5\\nCONTROLLER'},
 {k:'jersey',   n:'Silent Hill Is Broken Mesh Jersey', s:'SILENT HILL\\nJERSEY', alreadyWon:1},
 {k:'cowboy',   n:'Cowboy Hat - Brown',                s:'COWBOY\\nHAT',        alreadyWon:1},
 {k:'monitor',  n:'ASUS ROG Swift OLED 27"',           s:'OLED\\nMONITOR'},
 {k:'untildawn',n:'Until Dawn',                        s:'UNTIL\\nDAWN'},
 {k:'bangle',   n:"Everything's Romantic Bangle Set",  s:'ROMANTIC\\nBANGLES',  alreadyWon:1},
 {k:'axolotl',  n:'The Axolotl Ushanka',               s:'AXOLOTL\\nUSHANKA'},
 {k:'neon',     n:'Govee RGBIC Neon Lights',           s:'NEON\\nLIGHTS'},
 {k:'pyramid',  n:'Red Pyramid Head Figure',           s:'PYRAMID\\nHEAD'},
 {k:'celsius48',n:'48 x Celsius Peachy Vibe',          s:'48x\\nCELSIUS'},
 {k:'FAIL',     n:'TRY AGAIN',                         s:'TRY\\nAGAIN', fail:1},
 {k:'wig',      n:'Zero Two Cosplay Wig',              s:'ZERO TWO\\nWIG',      win:1, url:'https://throne.com/blueberryvibezz/item/6c1ffb36-3808-48f5-abfe-f7f42c8afcb0'},
 {k:'EXTRA',    n:'SECRET EXTRA SPIN',                 s:'EXTRA\\nSPIN', extra:1},
 {k:'gow',      n:'God of War',                        s:'GOD OF\\nWAR'},
 {k:'rabbit',   n:'Goth Rabbit Spa Headband',          s:'SPA\\nHEADBAND',      win:1, url:'https://throne.com/blueberryvibezz/item/20bf1901-a99f-467a-bf4a-ef874132cefa'},
 {k:'tender',   n:'Tender Hearted Bangle Set',         s:'TENDER\\nBANGLES'},
 {k:'hexa',     n:'Govee Glide Hexa Panels',           s:'HEXA\\nPANELS'},
 {k:'enderman', n:'The Enderman Ushanka',              s:'ENDERMAN\\nUSHANKA'},
 {k:'leon',     n:'Leon S. Kennedy Figure',            s:'LEON\\nFIGURE'},
 {k:'horns',    n:'3D Printed Headset Horns',          s:'HEADSET\\nHORNS',     win:1, url:'https://throne.com/blueberryvibezz/item/c3966aea-c58b-44ab-9d06-c77cbf720e1d'},
 {k:'dispatch', n:'Dispatch',                          s:'DISPATCH',           win:1, url:'https://throne.com/blueberryvibezz/item/86e34c64-16ea-4d2a-b1b8-15004a46c52f'},
 {k:'nurse',    n:'Bubble Head Nurse Figure',          s:'BUBBLE\\nNURSE'},
 {k:'celsius24',n:'24 x Celsius Peach Vibe',           s:'24x\\nCELSIUS',       win:1, url:'https://throne.com/blueberryvibezz/item/8716d1b1-08cf-4462-bf81-f1d5a1b53df6'},
];
const PRIZE_SPINS = 2;      /* spins earned back from the gauntlet */
const LOSS_SPINS  = 2;      /* spins she loses at the start */
'''
s = s[:old_cfg_start] + new_cfg + s[old_cfg_end:]

# ============ 2. WHEEL: already-won stamp, no winnable tell ============
s = s.replace(
"""    else { const c=PAL[i%PAL.length];
      if(it.win){ grad.addColorStop(0,'#ffffff'); grad.addColorStop(.14,c[0]); grad.addColorStop(1,c[1]); }
      else { grad.addColorStop(0,c[0]); grad.addColorStop(1,c[1]); } }
    ctx.beginPath(); ctx.moveTo(0,0); ctx.arc(0,0,R-6,a0,a1); ctx.closePath();
    ctx.fillStyle=grad; ctx.fill();
""",
"""    else { const c=PAL[i%PAL.length];
      grad.addColorStop(0,c[0]); grad.addColorStop(1,c[1]); }
    ctx.beginPath(); ctx.moveTo(0,0); ctx.arc(0,0,R-6,a0,a1); ctx.closePath();
    ctx.fillStyle=grad; ctx.fill();
    const owned = it.alreadyWon || WON.indexOf(it.k)>=0;
    if(owned){ ctx.fillStyle='rgba(4,0,14,.66)'; ctx.fill(); }
""")

s = s.replace(
"""    ctx.fillStyle= it.fail?'#ffd2da' : (it.extra?'#3a1f00':'#ffffff');
    const lx=R*.63;
    lines.forEach(function(ln,li){
      const y=(li-(lines.length-1)/2)*fs*1.02;
      ctx.strokeText(ln,lx,y); ctx.fillText(ln,lx,y);
    });
    ctx.restore();""",
"""    ctx.fillStyle= it.fail?'#ffd2da' : (it.extra?'#3a1f00':(owned?'rgba(255,255,255,.45)':'#ffffff'));
    const lx=R*.63;
    lines.forEach(function(ln,li){
      const y=(li-(lines.length-1)/2)*fs*1.02;
      ctx.strokeText(ln,lx,y); ctx.fillText(ln,lx,y);
    });
    if(owned){
      const fs2=R*.036;
      ctx.font='900 '+fs2+'px Outfit, system-ui, sans-serif';
      ctx.lineWidth=fs2*.5; ctx.strokeStyle='rgba(0,0,0,.85)';
      ctx.fillStyle='#ff5b7a';
      ctx.strokeText('ALREADY WON', R*.365, 0);
      ctx.fillText('ALREADY WON', R*.365, 0);
    }
    ctx.restore();""")

# WON must exist before the sprite is first built
s = s.replace("const wheelC = document.getElementById('wheel')",
              "const WON=[];\nconst wheelC = document.getElementById('wheel')")
s = s.replace("const WON=[];\nfunction markTracker(k){", "function markTracker(k){")

# ============ 3. MAIN LOOP: skip the wheel while a mini game runs ============
s = s.replace(
"""  if(!spinning && idleSpin) rot += dt*.16;
  drawWheel(rot); drawBulbs(dt); drawP(dt); drawRays(dt);""",
"""  if(!spinning && idleSpin) rot += dt*.16;
  if(!document.body.classList.contains('mg-open')){ drawWheel(rot); drawBulbs(dt); }
  drawP(dt); drawRays(dt);""")

# ============ 4. FLOW ============
s = s.replace(
"let step=0, override=null, state='ready';   /* ready | spinning | awaitGift | failed | done */",
"""let spinsTaken=0, spinsAllowed=LOSS_SPINS, phase='losses', override=null, state='ready';
/* phase: losses -> gauntlet -> comeback -> done
   state: ready | spinning | awaitGift | failed | bonus | lost | done */

function prizePool(){
  return ITEMS.filter(function(it){
    return it.win && !it.alreadyWon && WON.indexOf(it.k)<0;
  });
}
function pickOutcome(){
  if(override){ const k=override; override=null; return k; }
  if(phase==='losses') return 'FAIL';
  const pool = prizePool();
  if(!pool.length) return 'FAIL';
  return pool[(Math.random()*pool.length)|0].k;
}""")

s = s.replace(
"""  const key = override || SEQUENCE[Math.min(step, SEQUENCE.length-1)];
  override = null;
  let targetIdx = idxOf(key); if(targetIdx<0) targetIdx = idxOf('FAIL');""",
"""  const key = pickOutcome();
  let targetIdx = idxOf(key); if(targetIdx<0) targetIdx = idxOf('FAIL');""")

s = s.replace("  const isFinal = (step === SEQUENCE.length-1);",
              "  const isFinal = (spinsTaken+1 >= spinsAllowed);")

# counter + tracker
s = s.replace(
"""function updCounter(){
  counter.textContent = step>=SEQUENCE.length ? 'ALL DONE' : ('SPIN '+(step+1)+' / '+SEQUENCE.length);
}""",
"""function updCounter(){
  if(phase==='done'){ counter.textContent='ALL DONE'; return; }
  if(phase==='gauntlet'){ counter.textContent='GAUNTLET'; return; }
  if(phase==='comeback'){
    counter.textContent = 'COMEBACK ' + (spinsTaken-LOSS_SPINS+1) + ' / ' + PRIZE_SPINS;
    return;
  }
  counter.textContent = 'SPIN ' + (spinsTaken+1) + ' / ' + LOSS_SPINS;
}""")

s = s.replace("  for(let i=0;i<4;i++) h+='<div class=\"slot\"><div class=\"qm\">?</div>'+",
              "  for(let i=0;i<PRIZE_SPINS;i++) h+='<div class=\"slot\"><div class=\"qm\">?</div>'+")

# armNext -> phase machine
s = s.replace(
"""function armNext(){
  step++;
  document.getElementById('redveil').style.opacity=0;
  document.getElementById('rays').classList.remove('on');
  winMode=false; idleSpin=true;
  updCounter();
  if(step>=SEQUENCE.length){
    state='done';
    hub.disabled=true; hub.classList.remove('waiting','ready');
    hub.textContent='THE\\nEND';
    showFinale();
    return;
  }
  state='ready'; hub.disabled=false; hub.classList.remove('waiting');
  hub.classList.add('ready'); hub.textContent='SPIN';
}""",
"""function armNext(){
  spinsTaken++;
  document.getElementById('redveil').style.opacity=0;
  document.getElementById('rays').classList.remove('on');
  winMode=false; idleSpin=true;

  if(phase==='losses' && spinsTaken>=LOSS_SPINS){
    phase='gauntlet'; updCounter();
    state='lost';
    hub.disabled=true; hub.classList.remove('waiting','ready');
    hub.textContent='...';
    showLostEverything();
    return;
  }
  if(spinsTaken>=spinsAllowed){
    phase='done'; updCounter();
    state='done';
    hub.disabled=true; hub.classList.remove('waiting','ready');
    hub.textContent='THE\\nEND';
    showFinale();
    return;
  }
  updCounter();
  state='ready'; hub.disabled=false; hub.classList.remove('waiting');
  hub.classList.add('ready'); hub.textContent='SPIN';
}

/* ---------- rock bottom ---------- */
function showLostEverything(){
  document.getElementById('redveil').style.opacity=1;
  document.getElementById('dim').classList.add('on');
  Snd.buzzer(); setTimeout(function(){ Snd.sadTrombone(); },300);
  setTimeout(function(){ Snd.sadTrombone(); },1700);
  for(let i=0;i<5;i++) setTimeout(function(){ shake(); flashScreen(.3,'#ff0033'); }, i*380);
  setTimeout(function(){ document.getElementById('lostOv').classList.add('on'); },700);
}
function enterGauntlet(){
  if(state!=='lost') return;
  document.getElementById('lostOv').classList.remove('on');
  document.getElementById('dim').classList.remove('on');
  document.getElementById('redveil').style.opacity=0;
  state='gauntlet';
  MG.open();
}
/* called by the gauntlet when all 5 games are cleared */
function gauntletCleared(){
  phase='comeback';
  spinsAllowed = LOSS_SPINS + PRIZE_SPINS;
  updCounter();
  winMode=true;
  document.getElementById('rays').classList.add('on');
  chaos(10);
  Snd.fanfare(); Snd.jackpot(); Snd.yippee();
  cannons(); rainConfetti(140); fireworks(7);
  const b=document.getElementById('giftBanner');
  document.getElementById('giftText').textContent='+2 SPINS WON BACK!';
  b.classList.add('on');
  setTimeout(function(){ b.classList.remove('on');
    document.getElementById('giftText').textContent='GIFT PURCHASED!'; },5200);
  state='ready'; hub.disabled=false; hub.classList.remove('waiting');
  hub.classList.add('ready'); hub.textContent='SPIN';
}""")

# the two opening spins must always read as total loss
s = s.replace(
"""function doFail(){
  state='failed';""",
"""function doFail(){
  state='failed';
  document.getElementById('failSub').textContent =
    (phase==='losses' && spinsTaken===0) ? 'One spin left. Do not waste it.'
                                         : 'Nothing for you... this time';""")

# ============ 5. MARKUP ============
s = s.replace('<div id="giftBanner">',
"""<div class="ov" id="lostOv">
  <div id="lostCard">
    <div class="skull">&#128128;</div>
    <div id="lostTag">YOU LOST<br>EVERYTHING</div>
    <div id="lostSub">Two spins. Two losses. The wheel is closed.</div>
    <div id="lostHope">...but there is one way back in.</div>
    <button class="btn pinky" id="lostBtn">ENTER THE COMEBACK GAUNTLET</button>
  </div>
</div>

<div id="mgOv">
  <div id="mgPills"></div>
  <canvas id="mgCanvas"></canvas>
  <div id="mgHud"></div>
  <div class="mgCard" id="mgCard">
    <div id="mgCardTag"></div>
    <div id="mgCardSub"></div>
    <div id="mgCardRule"></div>
    <button class="btn" id="mgCardBtn">START</button>
  </div>
</div>

<div id="giftBanner">""")

s = s.replace(
'<div class="sub">Happy Birthday Blue &nbsp;&bull;&nbsp; Mystery Prizes &nbsp;&bull;&nbsp; Winners Get Bought Live</div>',
'<div class="sub">Happy Birthday Blue &nbsp;&bull;&nbsp; Random Mystery Prizes &nbsp;&bull;&nbsp; Winners Get Bought Live</div>')

# ============ 6. STYLES ============
s = s.replace("#help{position:fixed;left:16px;",
"""#lostCard{position:relative;text-align:center;transform:scale(.6);transition:.5s cubic-bezier(.15,1.7,.4,1);
  padding:clamp(26px,4vw,54px) clamp(30px,5vw,70px);border-radius:34px;
  background:radial-gradient(circle,rgba(30,0,10,.95) 0%,rgba(10,0,6,.9) 70%);
  border:4px solid rgba(255,51,85,.7);box-shadow:0 0 90px rgba(255,0,60,.5)}
.ov.on #lostCard{transform:scale(1)}
#lostTag{font-family:'Bungee',cursive;font-size:clamp(30px,6.6vw,96px);line-height:.95;color:#ff3355;
  text-shadow:0 0 40px rgba(255,51,85,.9),0 0 110px rgba(255,0,60,.6);animation:glitch .16s infinite}
#lostSub{margin-top:14px;font-weight:900;letter-spacing:3px;text-transform:uppercase;
  font-size:clamp(10px,1.4vw,18px);color:#ff9db0}
#lostHope{margin-top:18px;font-weight:800;font-size:clamp(12px,1.7vw,22px);color:#FFD447;
  animation:pop 1.8s ease-in-out infinite}

#mgOv{position:fixed;inset:0;z-index:86;display:none;align-content:center;justify-items:center;
  gap:12px;padding:16px;background:radial-gradient(circle at 50% 40%,#180b3d,#050110 75%)}
#mgOv.on{display:grid}
#mgCanvas{border-radius:18px;background:#0d0326;max-width:94vw;
  box-shadow:0 0 0 3px rgba(255,212,71,.55),0 0 70px rgba(139,61,255,.55),0 24px 70px rgba(0,0,0,.7)}
#mgHud{font-family:'Bungee',cursive;font-size:clamp(11px,1.4vw,19px);letter-spacing:1px;color:#FFD447;
  text-shadow:0 0 22px rgba(255,212,71,.6);min-height:1.2em;text-align:center}
#mgPills{display:flex;flex-wrap:wrap;gap:7px;justify-content:center}
.mgPill{font-weight:900;font-size:clamp(8px,.95vw,12px);letter-spacing:1.2px;padding:6px 12px;
  border-radius:999px;background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.14);
  color:rgba(255,255,255,.45)}
.mgPill.now{border-color:var(--gold);color:var(--gold);box-shadow:0 0 20px rgba(255,212,71,.45)}
.mgPill.done{border-color:#9DFF3C;color:#9DFF3C;background:rgba(157,255,60,.12)}
.mgCard{display:none;position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
  width:min(660px,92vw);text-align:center;padding:clamp(20px,3vw,40px);border-radius:28px;
  border:5px solid transparent;
  background:linear-gradient(160deg,#2b0a5e,#12032e) padding-box,
             conic-gradient(from 0deg,#FFD447,#FF3FD0,#22E7FF,#8B3DFF,#9DFF3C,#FFD447) border-box;
  animation:cardGlow 1.6s ease-in-out infinite}
.mgCard.win{background:linear-gradient(160deg,#0d3a1c,#04170c) padding-box,
             conic-gradient(from 0deg,#9DFF3C,#22E7FF,#FFD447,#9DFF3C) border-box}
.mgCard.lose{background:linear-gradient(160deg,#3a0512,#160207) padding-box,
             conic-gradient(from 0deg,#ff3355,#8B3DFF,#ff3355) border-box}
#mgCardTag{font-family:'Bungee',cursive;font-size:clamp(11px,1.5vw,18px);letter-spacing:4px;color:var(--gold)}
#mgCardSub{font-family:'Bungee',cursive;font-size:clamp(20px,3.4vw,44px);line-height:1.05;margin:8px 0 12px;
  background:linear-gradient(92deg,#fff,var(--cyan),#fff,var(--pink),#fff);background-size:300% 100%;
  -webkit-background-clip:text;background-clip:text;color:transparent;animation:flow 3s linear infinite}
#mgCardRule{white-space:pre-line;font-weight:700;font-size:clamp(11px,1.25vw,15.5px);line-height:1.6;
  color:rgba(255,255,255,.82)}
body.mg-open #stage,body.mg-open #counter,body.mg-open #hint{display:none}

#help{position:fixed;left:16px;""")

# ============ 7. WIRING ============
s = s.replace(
"document.getElementById('extraBtn').addEventListener('click', extraAcknowledged);",
"document.getElementById('extraBtn').addEventListener('click', extraAcknowledged);\n"
"document.getElementById('lostBtn').addEventListener('click', enterGauntlet);")

s = s.replace("addEventListener('keydown', function(e){\n  const k=e.key.toLowerCase();",
              "addEventListener('keydown', function(e){\n  if(MG.active()) return;\n  const k=e.key.toLowerCase();")

s = s.replace("""    if(state==='ready') spin();
    else if(state==='awaitGift') giftConfirmed();
    else if(state==='failed') failAcknowledged();
    else if(state==='bonus') extraAcknowledged();
    return;""",
"""    if(state==='ready') spin();
    else if(state==='awaitGift') giftConfirmed();
    else if(state==='failed') failAcknowledged();
    else if(state==='bonus') extraAcknowledged();
    else if(state==='lost') enterGauntlet();
    return;""")

s = s.replace("""    if(state==='awaitGift') giftConfirmed();
    else if(state==='failed') failAcknowledged();
    else if(state==='bonus') extraAcknowledged();
    else if(!started) begin();
    return;""",
"""    if(state==='awaitGift') giftConfirmed();
    else if(state==='failed') failAcknowledged();
    else if(state==='bonus') extraAcknowledged();
    else if(state==='lost') enterGauntlet();
    else if(!started) begin();
    return;""")

s = s.replace("  if(k==='1') override='sealion';\n  if(k==='2') override='jersey';\n"
              "  if(k==='3') override='cowboy';\n  if(k==='4') override='bangle';\n  if(k==='5') override='EXTRA';",
              "  if(k==='1') override='rabbit';\n  if(k==='2') override='wig';\n"
              "  if(k==='3') override='horns';\n  if(k==='4') override='dispatch';\n"
              "  if(k==='5') override='celsius24';\n  if(k==='g'){ phase='comeback'; spinsAllowed=LOSS_SPINS+PRIZE_SPINS; state='ready'; hub.disabled=false; hub.classList.add('ready'); hub.textContent='SPIN'; updCounter(); }")

# rebuild the wheel sprite whenever something becomes ALREADY WON
s = s.replace("""  el.classList.add('won');
  el.innerHTML='<img src="'+(A[k]||'')+'" alt=""><div><div class="nm">'+""",
"""  buildWheelSprite();
  el.classList.add('won');
  el.innerHTML='<img src="'+(A[k]||'')+'" alt=""><div><div class="nm">'+""")

# help panel
s = s.replace(
"""  <kbd>1</kbd> Sea Lion &nbsp; <kbd>2</kbd> Jersey &nbsp; <kbd>3</kbd> Cowboy Hat &nbsp; <kbd>4</kbd> Bangles<br>
  <kbd>5</kbd> Extra Spin &nbsp; <kbd>0</kbd> FAILED &nbsp; <kbd>R</kbd> full reset &nbsp; <kbd>M</kbd> mute<br>
  <kbd>F</kbd> fullscreen &nbsp; <kbd>C</kbd> confetti test &nbsp; <kbd>H</kbd> hide this<br>
  <span style="opacity:.6;font-size:11.5px">Order: Sea Lion &rarr; FAILED &rarr; Jersey &rarr; SECRET EXTRA SPIN
  &rarr; Cowboy Hat &rarr; Bangles (total chaos). Nothing else can ever be won.
  Operator only &mdash; keep this hidden on stream.</span>""",
"""  <kbd>1</kbd> Headband &nbsp; <kbd>2</kbd> Wig &nbsp; <kbd>3</kbd> Horns &nbsp; <kbd>4</kbd> Dispatch &nbsp; <kbd>5</kbd> Celsius<br>
  <kbd>0</kbd> force FAILED &nbsp; <kbd>G</kbd> skip gauntlet &nbsp; <kbd>R</kbd> full reset &nbsp; <kbd>M</kbd> mute<br>
  <kbd>F</kbd> fullscreen &nbsp; <kbd>C</kbd> confetti test &nbsp; <kbd>H</kbd> hide this<br>
  <span style="opacity:.6;font-size:11.5px">Flow: spin 1 FAIL &rarr; spin 2 FAIL &rarr; YOU LOST EVERYTHING
  &rarr; 5-game gauntlet (~10 min, unlimited retries, always winnable) &rarr; +2 spins,
  each a RANDOM pick from the 5 remaining prizes. Operator only &mdash; keep hidden on stream.</span>""")

assert s != o, 'template unchanged'
open(p, 'w', encoding='utf-8').write(s)
print('template patched')

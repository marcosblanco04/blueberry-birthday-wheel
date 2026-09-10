def sub(s, a, b):
    assert a in s, 'NOT FOUND: ' + a[:80].replace('\n', '\\n')
    return s.replace(a, b, 1)

f = 'template.html'
s = open(f, encoding='utf-8').read()
o = s

# ---- headset horns out of the prize pool ----
s = sub(s,
 " {k:'horns',    n:'3D Printed Headset Horns',          s:'HEADSET\\nHORNS',     win:1, url:'https://throne.com/blueberryvibezz/item/c3966aea-c58b-44ab-9d06-c77cbf720e1d'},",
 " {k:'horns',    n:'3D Printed Headset Horns',          s:'HEADSET\\nHORNS'},")

# ---- when the pool runs dry, the secret prize is what is left to win ----
s = sub(s, """function pickOutcome(){
  if(override){ const k=override; override=null; return k; }
  if(phase==='losses') return 'FAIL';
  const pool = prizePool();
  if(!pool.length) return 'FAIL';
  return pool[(Math.random()*pool.length)|0].k;
}""",
"""function pickOutcome(){
  if(override){ const k=override; override=null; return k; }
  if(phase==='losses') return 'FAIL';
  const pool = prizePool();
  if(pool.length) return pool[(Math.random()*pool.length)|0].k;
  if(WON.indexOf('SECRET') < 0) return 'SECRET';   /* the last thing on the wheel */
  return 'FAIL';
}""")

# ---- it is a win now, not a dud slice ----
s = sub(s, """  if(item.fail || item.secret) doFail();
  else doWin(item);""",
"""  if(item.fail) doFail();
  else doWin(item);""")

# ---- never fake-land on the secret slice ----
s = sub(s, "    if(it.fail || it.extra || it.alreadyWon) return;",
           "    if(it.fail || it.secret || it.alreadyWon) return;")

# ---- and always fake-out on the way to it ----
s = sub(s, """  const lastLoss  = (phase==='losses'   && spinsTaken === LOSS_SPINS-1);
  const lastPrize = (phase==='comeback' && spinsTaken+1 >= spinsAllowed);
  const force = (fakeOutForced === true) || lastLoss || lastPrize;""",
"""  const lastLoss  = (phase==='losses'   && spinsTaken === LOSS_SPINS-1);
  const lastPrize = (phase==='comeback' && spinsTaken+1 >= spinsAllowed);
  const secret    = !!(ITEMS[targetIdx] && ITEMS[targetIdx].secret);
  const force = (fakeOutForced === true) || lastLoss || lastPrize || secret;""")

# ---- the sealed win card ----
s = sub(s, """      <div id="seaLionBox"><img id="seaLionGif" alt="sea lion"><div id="orkText">ORK ORK ORK!</div></div>""",
"""      <div id="seaLionBox"><img id="seaLionGif" alt="sea lion"><div id="orkText">ORK ORK ORK!</div></div>
      <div id="winSecretBox">
        <div class="lock">&#128274;</div>
        <div class="sr">REVEALED ON THE 12TH</div>
        <div class="sh">Hint: it normally comes by the dozen &mdash; this is not a dozen.<br>
          You will smell it before you see it, and it will not last the week.<br>
          That is exactly the point.</div>
        <div class="sc" id="winSecretCd"></div>
      </div>""")

s = sub(s, "#seaLionBox,#yippeeBox{display:none;flex:0 0 auto}",
"""#seaLionBox,#yippeeBox,#winSecretBox{display:none;flex:0 0 auto}
#winSecretBox{max-width:min(560px,88vw);padding:14px 18px;border-radius:20px;
  border:3px dashed rgba(255,212,71,.8);background:rgba(255,212,71,.09);text-align:center}
#winSecretBox .lock{font-size:clamp(34px,5vw,60px);animation:pop 1.6s ease-in-out infinite}
#winSecretBox .sr{font-family:'Bungee',cursive;font-size:clamp(14px,2.4vw,30px);line-height:1.05;margin-top:6px;
  background:linear-gradient(92deg,#FFD447,#fff,#FF3FD0,#FFD447);background-size:300% 100%;
  -webkit-background-clip:text;background-clip:text;color:transparent;animation:flow 3s linear infinite}
#winSecretBox .sh{margin-top:9px;font-weight:700;font-size:clamp(10px,1.1vw,13.5px);line-height:1.6;
  color:rgba(255,255,255,.75);font-style:italic}
#winSecretBox .sc{margin-top:8px;font-family:'Bungee',cursive;font-size:clamp(12px,1.6vw,20px);color:#22E7FF}""")

# ---- doWin: sealed presentation for the secret prize ----
s = sub(s, """  const isSeaLion = item.k==='sealion';
  document.getElementById('winImg').src = A[item.k]||'';
  document.getElementById('winName').textContent = item.n;
  const lk=document.getElementById('winLink');
  lk.href = item.url||'#'; lk.textContent = item.url||'';""",
"""  const isSeaLion = item.k==='sealion';
  const isSecret  = !!item.secret;
  document.getElementById('winImgWrap').style.display = isSecret ? 'none' : 'grid';
  document.getElementById('winSecretBox').style.display = isSecret ? 'block' : 'none';
  document.querySelector('#winCard .linkline').style.display = isSecret ? 'none' : 'block';
  if(isSecret) startSecretCountdown('winSecretCd');
  document.getElementById('winImg').src = A[item.k]||'';
  document.getElementById('winName').textContent = isSecret ? '? ? ? ? ?' : item.n;
  const lk=document.getElementById('winLink');
  lk.href = item.url||'#'; lk.textContent = item.url||'';""")

s = sub(s, """  } else if(isFinal){
    document.getElementById('winTag').textContent='MEGA JACKPOT!!!';
  } else {""",
"""  } else if(isSecret){
    document.getElementById('winTag').textContent='THE SECRET PRIZE!!';
  } else if(isFinal){
    document.getElementById('winTag').textContent='MEGA JACKPOT!!!';
  } else {""")

s = sub(s, """  document.getElementById('winSub').textContent = isFinal
    ? 'SUPER PRIZE - THE BIGGEST DREAM ITEM ON THE WHOLE LIST'
    : 'Real prize - getting bought right now';""",
"""  document.getElementById('winSub').textContent = isSecret
    ? 'YOU WON SOMETHING YOU ARE NOT ALLOWED TO SEE YET'
    : (isFinal ? 'SUPER PRIZE - THE BIGGEST DREAM ITEM ON THE WHOLE LIST'
               : 'Real prize - getting bought right now');""")

s = sub(s, """  document.getElementById('winBtn').textContent = isFinal
    ? 'GIFT BOUGHT - SHOW THE FINALE'
    : 'GIFT BOUGHT - NEXT SPIN';""",
"""  document.getElementById('winBtn').textContent = isFinal
    ? 'GIFT BOUGHT - SHOW THE FINALE'
    : (isSecret ? 'SEALED - KEEP GOING' : 'GIFT BOUGHT - NEXT SPIN');""")

# ---- countdown helper takes a target element now ----
s = sub(s, """function startSecretCountdown(){
  const el = document.getElementById('secretCountdown');
  if(!el) return;""",
"""const secretTimers = {};
function startSecretCountdown(id){
  const el = document.getElementById(id || 'secretCountdown');
  if(!el) return;""")
s = sub(s, """  tick();
  if(secretTimer) clearInterval(secretTimer);
  secretTimer = setInterval(tick, 1000);
}""",
"""  tick();
  const key = id || 'secretCountdown';
  if(secretTimers[key]) clearInterval(secretTimers[key]);
  secretTimers[key] = setInterval(tick, 1000);
}""")
s = sub(s, "let secretTimer = null;\n", "")

# ---- the finale grid needs a padlock tile for the secret ----
s = sub(s, """  WON.forEach(function(k){
    const it=ITEMS[idxOf(k)];
    g+='<div class="sumItem"><img src="'+(A[k]||'')+'" alt=""><div class="t">'+it.n+'</div></div>';
  });""",
"""  WON.forEach(function(k){
    const it=ITEMS[idxOf(k)];
    if(!it) return;
    if(it.secret){
      g+='<div class="sumItem secret"><div class="pad">&#128274;</div>'+
         '<div class="t">SECRET PRIZE<br><span>revealed on the 12th</span></div></div>';
    } else {
      g+='<div class="sumItem"><img src="'+(A[k]||'')+'" alt=""><div class="t">'+it.n+'</div></div>';
    }
  });""")
s = sub(s, ".sumItem .t{margin-top:7px;",
""".sumItem.secret{border-style:dashed;background:rgba(255,212,71,.12)}
.sumItem .pad{height:clamp(80px,10vh,110px);display:grid;place-items:center;
  font-size:clamp(34px,5vw,54px);background:rgba(255,255,255,.06);border-radius:12px}
.sumItem .t span{font-weight:700;font-size:.85em;opacity:.7;font-style:italic}
.sumItem .t{margin-top:7px;""")

# ---- tracker: padlock instead of a photo ----
s = sub(s, """  el.innerHTML='<img src="'+(A[k]||'')+'" alt=""><div><div class="nm">'+
    ITEMS[idxOf(k)].n+'</div><div class="st">WON!</div></div>';""",
"""  const it = ITEMS[idxOf(k)];
  const thumb = (it && it.secret) ? '<div class="qm">&#128274;</div>'
                                  : '<img src="'+(A[k]||'')+'" alt="">';
  el.innerHTML = thumb + '<div><div class="nm">' +
    ((it && it.secret) ? 'SECRET PRIZE' : it.n) + '</div><div class="st">WON!</div></div>';""")

# ---- admin: let it force / mark the secret prize too ----
s = sub(s, """  <span style="opacity:.6;font-size:11.5px">Flow: FAIL &rarr; FAIL &rarr; YOU LOST EVERYTHING &rarr; 5-game
  gauntlet &rarr; +2 spins &rarr; DOUBLE OR NOTHING (the NO button runs away) &rarr; she hits the 5%
  &rarr; +2 spins &rarr; Celsius mash fight &rarr; finale. Prizes are the 4 cheapest, drawn at random.
  Operator only &mdash; keep hidden on stream.</span>""",
"""  <span style="opacity:.6;font-size:11.5px">Flow: FAIL &rarr; FAIL &rarr; YOU LOST EVERYTHING &rarr; 5-game
  gauntlet &rarr; +2 spins (random prize each) &rarr; DOUBLE OR NOTHING (the NO button runs away)
  &rarr; she hits the 5% &rarr; +2 spins: the last prize, then the SECRET PRIZE
  &rarr; Celsius mash fight &rarr; finale. Pool: Headband, Wig, Dispatch.
  Operator only &mdash; keep hidden on stream.</span>""")

assert s != o
open(f, 'w', encoding='utf-8').write(s)
print('template.html patched')

f = 'endgame.js'
s = open(f, encoding='utf-8').read(); o = s
s = sub(s, """    ITEMS.filter(function(it){ return it.win || it.final; }).forEach(function(it){
      btn(r, it.n, function(){ override = it.k; armWheel(); closePanel(); });
    });""",
"""    ITEMS.filter(function(it){ return it.win || it.final || it.secret; }).forEach(function(it){
      btn(r, it.n, function(){ override = it.k; armWheel(); closePanel(); });
    });""")
s = sub(s, """    ITEMS.filter(function(it){ return it.win || it.final; }).forEach(function(it){
      btn(r, 'Mark won: ' + it.n, function(){ markTracker(it.k); });
    });""",
"""    ITEMS.filter(function(it){ return it.win || it.final || it.secret; }).forEach(function(it){
      btn(r, 'Mark won: ' + it.n, function(){ markTracker(it.k); });
    });""")
assert s != o
open(f, 'w', encoding='utf-8').write(s)
print('endgame.js patched')

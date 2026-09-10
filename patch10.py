p = 'template.html'
s = open(p, encoding='utf-8').read()
o = s

def rep(a, b, n=1):
    global s
    assert a in s, 'NOT FOUND: ' + a[:70]
    s = s.replace(a, b, n)

# ============================================================
# 1. gravity multiplier for the "gravity is broken" event
# ============================================================
rep("let P=[];", "let P=[];\nlet GRAV_MUL = 1;")
rep("    p.vy+=p.g; p.vx*=p.drag; p.vy*=p.drag; p.sw+=.12;",
    "    p.vy+=p.g*GRAV_MUL; p.vx*=p.drag; p.vy*=p.drag; p.sw+=.12;")
rep("    if(p.life<=0||p.y>innerHeight+90||p.x<-160||p.x>innerWidth+160){ P.splice(i,1); continue; }",
    "    if(p.life<=0||p.y>innerHeight+90||p.y<-320||p.x<-160||p.x>innerWidth+160){ P.splice(i,1); continue; }")

# ============================================================
# 2. record scratch sound
# ============================================================
rep("""  buzzer(){ if(this.muted||!this.ctx)return;""",
"""  scratch(){ if(this.muted||!this.ctx)return;
    const t=this.t;
    this.tone(1400,.55,.3,'sawtooth',t,90);
    this.tone(700,.55,.22,'square',t,60);
    const s2=this.ctx.createBufferSource(); s2.buffer=this.noiseBuf();
    const bp=this.ctx.createBiquadFilter(); bp.type='bandpass'; bp.Q.value=2.5;
    bp.frequency.setValueAtTime(4200,t); bp.frequency.exponentialRampToValueAtTime(160,t+.5);
    const g=this.gain(0); s2.connect(bp); bp.connect(g);
    g.gain.setValueAtTime(.0001,t); g.gain.linearRampToValueAtTime(.3,t+.03);
    g.gain.exponentialRampToValueAtTime(.0001,t+.55);
    s2.start(t,Math.random()*.5); s2.stop(t+.6);
  },
  buzzer(){ if(this.muted||!this.ctx)return;""")

# ============================================================
# 3. spin engine: reusable phases + fake-out landing
# ============================================================
rep("""function targetRotationFor(index){
  const centre = index*SEG;
  const need = (-centre) % (Math.PI*2);
  const cur = rot % (Math.PI*2);
  let delta = need - cur; while(delta<0) delta += Math.PI*2;
  const turns = 7 + Math.floor(Math.random()*3);
  const jitter = (Math.random()-.5)*SEG*.42;
  return rot + turns*Math.PI*2 + delta + jitter;
}""",
"""function targetRotationFor(index, turns, jitterScale){
  const centre = index*SEG;
  const need = (-centre) % (Math.PI*2);
  const cur = rot % (Math.PI*2);
  let delta = need - cur; while(delta<0) delta += Math.PI*2;
  const t = (turns===undefined) ? (7 + Math.floor(Math.random()*3)) : turns;
  const jitter = (Math.random()-.5)*SEG*(jitterScale===undefined ? .42 : jitterScale);
  return rot + t*Math.PI*2 + delta + jitter;
}

/* one spin phase: eases into `targetIdx`, then calls done() */
function runSpin(targetIdx, opts, done){
  const from = rot;
  const to = targetRotationFor(targetIdx, opts.turns, opts.jitter);
  const dist = to - from;
  const DUR = opts.dur, HOLD_AT = opts.holdAt, HOLD_MS = opts.holdMs || 0, CREEP = .06;
  const t0 = performance.now();
  let tensionDone = false;

  function frame(now){
    const e = now - t0;
    let p;
    if(HOLD_MS > 0){
      if(e < DUR*HOLD_AT) p = e/DUR;
      else if(e < DUR*HOLD_AT + HOLD_MS) p = HOLD_AT + (e - DUR*HOLD_AT)/DUR*CREEP;
      else p = Math.min(1, (e - HOLD_MS*(1-CREEP))/DUR);
    } else {
      p = Math.min(1, e/DUR);
    }
    rot = from + dist*(1 - Math.pow(1-p, opts.pow || 3));

    const seg = Math.floor(rot/SEG);
    if(seg !== lastTickSeg){
      Snd.clack(.35 + Math.max(0,1-p)*1.1);
      lastTickSeg = seg;
      pointerEl.animate(
        [{transform:'translateX(-50%) rotate(0deg)'},
         {transform:'translateX(-50%) rotate(-16deg)'},
         {transform:'translateX(-50%) rotate(0deg)'}],
        {duration:170,easing:'ease-out'});
    }
    if(opts.tension && !tensionDone && p > HOLD_AT-.004){
      tensionDone = true; Snd.heartbeat();
      setTimeout(function(){ Snd.heartbeat(); },560);
      setTimeout(function(){ Snd.heartbeat(); },1120);
    }
    if(p < 1) requestAnimationFrame(frame); else done();
  }
  requestAnimationFrame(frame);
}

/* ---------- the fake-out ---------- */
const BIG_LOOKING = ['monitor','ps5','neon','hexa','pyramid','nurse','leon','tender','gow','untildawn'];
const FAKEOUT_CHANCE = .55;
let fakeOutForced = null;          /* null = auto, true = always, false = never */

function pickDecoy(targetIdx){
  if(fakeOutForced === false) return null;
  const lastLoss  = (phase==='losses'   && spinsTaken === LOSS_SPINS-1);
  const lastPrize = (phase==='comeback' && spinsTaken+1 >= spinsAllowed);
  const force = (fakeOutForced === true) || lastLoss || lastPrize;
  if(!force && Math.random() > FAKEOUT_CHANCE) return null;

  let pick = null;
  [2,3,4].forEach(function(k){
    const i = (targetIdx + k) % N, it = ITEMS[i];
    if(it.fail || it.extra || it.alreadyWon) return;
    if(!pick) pick = {idx:i, item:it};
    else if(BIG_LOOKING.indexOf(it.k) >= 0 && BIG_LOOKING.indexOf(pick.item.k) < 0) pick = {idx:i, item:it};
  });
  return pick;
}

function fakeCelebrate(item, done){
  const box = document.getElementById('fakeWin');
  document.getElementById('fakeWinName').textContent = item.n;
  document.getElementById('fakeWinImg').src = A[item.k] || '';
  box.classList.remove('wait'); box.classList.add('on');
  winMode = true;
  Snd.jackpot(); Snd.fanfare();
  cannons(); rainConfetti(130); shake(); flashScreen(.9);
  document.getElementById('rays').classList.add('on');
  setTimeout(function(){ cannons(); shake(); }, 500);
  setTimeout(function(){
    box.classList.add('wait');
    Snd.scratch(); shake();
    P.length = 0;
    document.getElementById('rays').classList.remove('on');
    winMode = false;
  }, 2300);
  setTimeout(function(){
    box.classList.remove('on','wait');
    done();
  }, 3400);
}""")

rep("""  const from=rot, to=targetRotationFor(targetIdx), dist=to-from;
  const DUR=8000, HOLD_AT=.80, HOLD_MS=900, CREEP=.06;
  const t0=performance.now();
  let tensionDone=false;

  function frame(now){
    const e=now-t0;
    let p;
    if(e < DUR*HOLD_AT) p = e/DUR;
    else if(e < DUR*HOLD_AT+HOLD_MS) p = HOLD_AT + (e-DUR*HOLD_AT)/DUR*CREEP;
    else p = Math.min(1,(e-HOLD_MS*(1-CREEP))/DUR);

    rot = from + dist*(1-Math.pow(1-p, 3));

    const seg = Math.floor(rot/SEG);
    if(seg!==lastTickSeg){
      Snd.clack(.35+Math.max(0,1-p)*1.1);
      lastTickSeg=seg;
      pointerEl.animate(
        [{transform:'translateX(-50%) rotate(0deg)'},
         {transform:'translateX(-50%) rotate(-16deg)'},
         {transform:'translateX(-50%) rotate(0deg)'}],
        {duration:170,easing:'ease-out'});
    }
    if(!tensionDone && p>HOLD_AT-.004){
      tensionDone=true; Snd.heartbeat();
      setTimeout(function(){ Snd.heartbeat(); },560);
      setTimeout(function(){ Snd.heartbeat(); },1120);
    }
    if(p<1) requestAnimationFrame(frame); else land(item);
  }
  requestAnimationFrame(frame);
}""",
"""  const decoy = pickDecoy(targetIdx);
  runSpin(decoy ? decoy.idx : targetIdx,
          {dur:8000, holdAt:.80, holdMs:900, tension:true},
          function(){
    if(!decoy){ land(item); return; }
    fakeCelebrate(decoy.item, function(){
      runSpin(targetIdx, {dur:3200, holdAt:1, holdMs:0, turns:0, jitter:.3, pow:3.6},
              function(){ land(item); });
    });
  });
}""")

# ============================================================
# 4. markup
# ============================================================
rep('<div id="giftBanner">',
"""<div id="fakeWin">
  <div id="fakeWinIn">
    <div class="ft">WINNER!!!</div>
    <div class="fimg"><img id="fakeWinImg" alt=""></div>
    <div class="fn" id="fakeWinName"></div>
    <div class="fw">...wait</div>
  </div>
</div>

<div id="surLayer"></div>

<div id="giftBanner">""")

# ============================================================
# 5. styles
# ============================================================
rep("#help{position:fixed;left:16px;",
"""/* ---------- fake-out winner ---------- */
#fakeWin{position:fixed;inset:0;z-index:67;display:grid;place-items:center;pointer-events:none;
  opacity:0;visibility:hidden;transition:.25s}
#fakeWin.on{opacity:1;visibility:visible}
#fakeWinIn{text-align:center;padding:clamp(18px,2.6vw,36px) clamp(26px,4vw,64px);border-radius:30px;
  border:5px solid transparent;transform:scale(.6);transition:.45s cubic-bezier(.15,1.7,.4,1);
  background:linear-gradient(160deg,#4a3200,#1c1000) padding-box,
             conic-gradient(from 0deg,#fff6c2,#FFD447,#ff9d2e,#FFD447,#fff6c2) border-box;
  animation:cardGlow .9s ease-in-out infinite}
#fakeWin.on #fakeWinIn{transform:scale(1)}
#fakeWinIn .ft{font-family:'Bungee',cursive;font-size:clamp(28px,6vw,84px);line-height:1;
  background:linear-gradient(92deg,#fff,#FFD447,#fff,#ff9d2e,#fff);background-size:300% 100%;
  -webkit-background-clip:text;background-clip:text;color:transparent;animation:flow 1.2s linear infinite;
  filter:drop-shadow(0 0 32px rgba(255,212,71,.95))}
#fakeWinIn .fimg{width:clamp(96px,14vh,150px);height:clamp(96px,14vh,150px);margin:12px auto 8px;
  background:#fff;border-radius:20px;display:grid;place-items:center;padding:8px;overflow:hidden}
#fakeWinIn .fimg img{max-width:100%;max-height:100%;object-fit:contain}
#fakeWinIn .fn{font-weight:900;font-size:clamp(14px,2vw,28px)}
#fakeWinIn .fw{display:none;font-family:'Bungee',cursive;font-size:clamp(20px,3.6vw,52px);
  color:#ff3355;margin-top:8px;animation:glitch .16s infinite}
#fakeWin.wait #fakeWinIn{background:linear-gradient(160deg,#3a0512,#160207) padding-box,
  conic-gradient(from 0deg,#ff3355,#8B3DFF,#ff3355) border-box;animation:none;
  transform:scale(.94) rotate(-1.5deg)}
#fakeWin.wait #fakeWinIn .ft,#fakeWin.wait #fakeWinIn .fn,#fakeWin.wait #fakeWinIn .fimg{opacity:.25}
#fakeWin.wait #fakeWinIn .fw{display:block}

/* ---------- surprises ---------- */
#surLayer{position:fixed;inset:0;z-index:76;pointer-events:none;overflow:hidden}
.surBanner{position:absolute;top:12%;left:50%;transform:translateX(-50%);text-align:center;
  padding:12px 30px;border-radius:999px;background:rgba(6,1,18,.86);border:3px solid var(--c);
  box-shadow:0 0 44px var(--c);animation:surIn .45s cubic-bezier(.2,1.7,.4,1)}
.surBanner b{display:block;font-family:'Bungee',cursive;font-size:clamp(14px,2.4vw,32px);color:var(--c);
  letter-spacing:1px}
.surBanner span{display:block;font-weight:800;font-size:clamp(9px,1.05vw,13px);letter-spacing:2px;
  text-transform:uppercase;color:rgba(255,255,255,.6);margin-top:3px}
@keyframes surIn{from{transform:translateX(-50%) scale(.4);opacity:0}to{transform:translateX(-50%) scale(1);opacity:1}}

body.sur-flip{transform:rotate(180deg);transition:transform .8s cubic-bezier(.6,-0.3,.3,1.3)}
body.sur-disco{animation:surDisco .55s steps(3) infinite}
@keyframes surDisco{0%{filter:hue-rotate(0) saturate(1.6)}100%{filter:hue-rotate(360deg) saturate(2.2)}}

.surLion{position:absolute;width:clamp(90px,13vw,190px);border-radius:16px;
  box-shadow:0 0 40px rgba(34,231,255,.8);animation:surLion 2.4s ease-in-out infinite alternate}
@keyframes surLion{from{transform:translate(0,0) rotate(-8deg) scale(1)}
                   to{transform:translate(var(--dx),var(--dy)) rotate(8deg) scale(1.15)}}

.surCrash{position:absolute;inset:0;background:#0a0a14;display:grid;place-items:center;text-align:center}
.surCrashIn b{display:block;font-family:'Bungee',cursive;font-size:clamp(20px,4vw,56px);color:#ff3355;
  letter-spacing:2px}
.surCrashIn span{display:block;margin-top:10px;font-weight:700;font-size:clamp(11px,1.3vw,16px);
  color:rgba(255,255,255,.5);letter-spacing:1px}
.surCrashIn .sp{width:54px;height:54px;margin:0 auto 22px;border-radius:50%;
  border:5px solid rgba(255,255,255,.15);border-top-color:#ff3355;animation:surSpin .8s linear infinite}
@keyframes surSpin{to{transform:rotate(360deg)}}

.surChat{position:absolute;right:-60vw;white-space:nowrap;font-weight:800;
  font-size:clamp(12px,1.5vw,20px);color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.9);
  animation:surChat linear forwards}
.surChat i{color:#9DFF3C;font-style:normal}
@keyframes surChat{from{transform:translateX(0)}to{transform:translateX(-190vw)}}

.surBox{position:absolute;left:50%;top:-14vh;transform:translateX(-50%);font-size:clamp(60px,11vw,150px);
  animation:surDrop 1.5s cubic-bezier(.5,1.6,.4,1) forwards}
.surBox.pop{animation:surPop .5s ease-out infinite alternate}
@keyframes surDrop{to{top:34vh}}
@keyframes surPop{from{transform:translateX(-50%) scale(1) rotate(-6deg)}
                  to{transform:translateX(-50%) scale(1.2) rotate(6deg)}}

.surSlots{position:absolute;left:50%;top:34%;transform:translate(-50%,-50%);display:flex;gap:12px;
  padding:18px 24px;border-radius:24px;background:rgba(6,1,18,.9);
  border:5px solid #FFD447;box-shadow:0 0 60px rgba(255,212,71,.7)}
.surSlots .r{width:clamp(58px,8vw,104px);height:clamp(58px,8vw,104px);border-radius:16px;background:#fff;
  display:grid;place-items:center;font-size:clamp(34px,5vw,64px)}

.surDon{position:absolute;inset:0;display:grid;place-items:center;pointer-events:auto;
  background:rgba(5,1,16,.82)}
.surDonIn{text-align:center;max-width:min(680px,92vw);padding:clamp(22px,3vw,44px);border-radius:30px;
  border:5px solid transparent;
  background:linear-gradient(160deg,#3a0512,#160207) padding-box,
             conic-gradient(from 0deg,#ff3355,#FFD447,#ff3355) border-box;
  animation:cardGlow .8s ease-in-out infinite}
.surDonIn .t{font-family:'Bungee',cursive;font-size:clamp(22px,4.4vw,58px);line-height:1;color:#ff5b7a;
  text-shadow:0 0 34px rgba(255,51,85,.9)}
.surDonIn .s{margin-top:10px;font-weight:800;font-size:clamp(11px,1.35vw,17px);color:rgba(255,255,255,.8)}
.surDonIn .clock{font-family:'Bungee',cursive;font-size:clamp(38px,7vw,92px);color:#FFD447;margin:8px 0;
  animation:pop .5s ease-in-out infinite}
.surDonIn .row{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}

#help{position:fixed;left:16px;""")

# ============================================================
# 6. hotkeys + help
# ============================================================
rep("  if(k==='c'){ cannons(); rainConfetti(120); fireworks(3); }",
"""  if(k==='c'){ cannons(); rainConfetti(120); fireworks(3); }
  if(k==='x'){ SUR.fire(); }
  if(k==='v'){ SUR.doubleOrNothing(); }
  if(k==='b'){ fakeOutForced = (fakeOutForced===null) ? true : (fakeOutForced===true ? false : null); }""")

rep("""  <kbd>F</kbd> fullscreen &nbsp; <kbd>C</kbd> confetti test &nbsp; <kbd>H</kbd> hide this<br>""",
"""  <kbd>F</kbd> fullscreen &nbsp; <kbd>C</kbd> confetti test &nbsp; <kbd>H</kbd> hide this<br>
  <kbd>X</kbd> random surprise &nbsp; <kbd>V</kbd> double-or-nothing troll &nbsp;
  <kbd>B</kbd> fake-out: auto/always/never<br>""")

assert s != o
open(p, 'w', encoding='utf-8').write(s)
print('patched')

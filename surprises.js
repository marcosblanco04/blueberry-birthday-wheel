/* ============================================================
   9. SURPRISES - random chaos events + the double-or-nothing troll
   Nothing in here can change an outcome. It is pure theatre.
   ============================================================ */
const SUR = (function(){

let busy = false, timers = [], nextAt = 0;
const layer = document.getElementById('surLayer');

function later(fn, ms){ timers.push(setTimeout(fn, ms)); }
function clearAll(){ timers.forEach(clearTimeout); timers = []; }

function end(cleanup){
  if(cleanup) cleanup();
  busy = false;
  layer.innerHTML = '';
  clearAll();
}
function banner(text, sub, col){
  const d = document.createElement('div');
  d.className = 'surBanner';
  d.style.setProperty('--c', col || '#FFD447');
  d.innerHTML = '<b>' + text + '</b>' + (sub ? '<span>' + sub + '</span>' : '');
  layer.appendChild(d);
  return d;
}

/* ---------- the events ---------- */

function evUpsideDown(){
  document.body.classList.add('sur-flip');
  banner('THE WORLD FLIPPED', 'blame the wheel', '#22E7FF');
  Snd.whoosh(); Snd.tone(420,1.2,.3,'sawtooth',undefined,90);
  later(function(){ end(function(){ document.body.classList.remove('sur-flip'); }); }, 9000);
}

function evDisco(){
  document.body.classList.add('sur-disco');
  banner('DISCO BREAK', 'nobody asked for this', '#FF3FD0');
  const beat = setInterval(function(){
    Snd.tone(55,.16,.5,'sine',undefined,35);
    Snd.noise(.09,7000,2,.1,'highpass');
    flashScreen(.16, Math.random()<.5 ? '#FF3FD0' : '#22E7FF');
  }, 260);
  timers.push(beat);
  later(function(){ clearInterval(beat); end(function(){ document.body.classList.remove('sur-disco'); }); }, 8500);
}

function evSeaLions(){
  banner('SEA LION INVASION', 'ork ork ork ork ork', '#22E7FF');
  const lions = [];
  for(let i=0;i<7;i++){
    const im = document.createElement('img');
    im.className = 'surLion';
    im.src = A.sealiongif || '';
    im.style.left = (Math.random()*80+5) + 'vw';
    im.style.top  = (Math.random()*70+8) + 'vh';
    im.style.setProperty('--dx', ((Math.random()-.5)*60) + 'vw');
    im.style.setProperty('--dy', ((Math.random()-.5)*45) + 'vh');
    im.style.animationDelay = (Math.random()*.6) + 's';
    layer.appendChild(im); lions.push(im);
  }
  Snd.seaLionSong();
  later(function(){ Snd.seaLionSong(); }, 2600);
  later(function(){ Snd.seaLionSong(); }, 5200);
  later(function(){ end(); }, 8000);
}

function evFakeCrash(){
  const d = document.createElement('div');
  d.className = 'surCrash';
  d.innerHTML = '<div class="surCrashIn"><div class="sp"></div>' +
                '<b>STREAM CRASHED</b><span>reconnecting to blueberry servers...</span></div>';
  layer.appendChild(d);
  Snd.buzzer(); Snd.noise(1.6, 300, .6, .2, 'lowpass');
  later(function(){
    d.querySelector('.surCrashIn').innerHTML =
      '<b style="color:#9DFF3C">just kidding</b><span>go back to your birthday 💜</span>';
    Snd.ding(880,undefined,1); Snd.ding(1320,Snd.t+.12,1);
    rainConfetti(80);
  }, 2600);
  later(function(){ end(); }, 4600);
}

function evBerryRain(){
  banner('IT IS RAINING BERRIES', 'someone tipped the basket', '#8B3DFF');
  const iv = setInterval(function(){ rainConfetti(26, 268); }, 260);
  timers.push(iv);
  Snd.coins(16);
  later(function(){ clearInterval(iv); end(); }, 6500);
}

function evGravity(){
  GRAV_MUL = -1;
  banner('GRAVITY IS BROKEN', 'up is the new down', '#9DFF3C');
  burst(innerWidth/2, innerHeight*.9, 220, {speed:6, g:.05, emoji:.3});
  Snd.tone(90,1.6,.4,'sine',undefined,900);
  later(function(){ end(function(){ GRAV_MUL = 1; }); }, 7000);
}

function evAngryWheel(){
  banner('THE WHEEL IS ANGRY', 'you have upset it', '#ff3355');
  document.getElementById('redveil').style.opacity = .85;
  const old = idleSpin;
  idleSpin = false;
  const t0 = performance.now();
  const iv = setInterval(function(){
    rot -= .09;
    if(Math.random()<.3) Snd.clack(.8);
    if(performance.now()-t0 > 5200){
      clearInterval(iv);
      end(function(){
        idleSpin = old;
        document.getElementById('redveil').style.opacity = 0;
      });
    }
  }, 16);
  timers.push(iv);
  Snd.tone(48,2.4,.5,'sawtooth',undefined,30);
  Snd.noise(2.4, 180, .8, .22, 'lowpass');
  for(let i=0;i<6;i++) later(function(){ shake(); }, i*420);
}

function evTinyWheel(){
  const w = document.getElementById('wheelWrap');
  w.classList.add('sur-tiny');
  banner('OOPS', 'the wheel got shy', '#FFD447');
  Snd.tone(900,.5,.35,'sine',undefined,180);
  later(function(){
    w.classList.remove('sur-tiny');
    Snd.tone(180,.4,.35,'sine',undefined,1100);
    cannons();
    end();
  }, 4200);
}

const CHAT = [
  'blue what are you DOING', 'CHAT SAW NOTHING', 'this wheel is rigged (it is)',
  'ORK ORK ORK', 'not the sea lion again', 'she is going to cry',
  'MODS.', 'i would have quit by now', 'BIRTHDAY GIRL BEHAVIOUR',
  'the bombs got me too', 'first try btw', 'copium', 'SHE IS SO BACK',
  'my blood pressure', 'happy birthday blue 💜', 'W stream'
];
const CHATTER = ['berrylover','pyramid_head_69','not_a_mod','xX_axolotl_Xx','sealionfan',
                 'blueberrypie','chatgpt_irl','yeehaw_enjoyer','silenthillgirl'];
function evChat(){
  let n = 0;
  const iv = setInterval(function(){
    const d = document.createElement('div');
    d.className = 'surChat';
    d.style.top = (8 + Math.random()*80) + 'vh';
    d.style.animationDuration = (5 + Math.random()*3) + 's';
    d.innerHTML = '<i>' + CHATTER[(Math.random()*CHATTER.length)|0] + ':</i> ' +
                  CHAT[(Math.random()*CHAT.length)|0];
    layer.appendChild(d);
    Snd.clack(.4);
    if(++n > 22){ clearInterval(iv); later(function(){ end(); }, 4000); }
  }, 260);
  timers.push(iv);
}

function evDelivery(){
  const d = document.createElement('div');
  d.className = 'surBox'; d.textContent = '📦';
  layer.appendChild(d);
  Snd.tone(300,.9,.35,'sine',undefined,120);
  later(function(){
    d.textContent = '🎁';
    d.classList.add('pop');
    cannons(); rainConfetti(120); Snd.fanfare(); shake();
    banner('MYSTERY DELIVERY', 'it was empty. sorry.', '#FFD447');
  }, 1600);
  later(function(){ end(); }, 5200);
}

function evSlots(){
  const d = document.createElement('div');
  d.className = 'surSlots';
  d.innerHTML = '<div class="r">🫐</div><div class="r">🫐</div><div class="r">🫐</div>';
  layer.appendChild(d);
  const faces = ['🫐','🦭','💎','🤠','⭐','💀','🎂'];
  const reels = d.querySelectorAll('.r');
  let spins = 0;
  const iv = setInterval(function(){
    reels.forEach(function(r){ r.textContent = faces[(Math.random()*faces.length)|0]; });
    Snd.clack(.6);
    if(++spins > 26){
      clearInterval(iv);
      reels.forEach(function(r){ r.textContent = '🦭'; });
      Snd.jackpot(); cannons(); rainConfetti(140);
      banner('THREE SEA LIONS', 'this wins you absolutely nothing', '#22E7FF');
      Snd.seaLionSong();
      later(function(){ end(); }, 4200);
    }
  }, 90);
  timers.push(iv);
}

const EVENTS = [evUpsideDown, evDisco, evSeaLions, evFakeCrash, evBerryRain,
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
function remaining(){ return queue.length; }

/* ---------- DOUBLE OR NOTHING (operator troll, key V) ---------- */
function doubleOrNothing(){
  if(busy) return;
  busy = true;
  const d = document.createElement('div');
  d.className = 'surDon';
  d.innerHTML =
    '<div class="surDonIn">' +
      '<div class="t">DOUBLE OR NOTHING?</div>' +
      '<div class="s">Risk the prize you just won for two of them.</div>' +
      '<div class="clock" id="donClock">5</div>' +
      '<div class="row">' +
        '<button class="btn pinky" data-a="1">RISK IT</button>' +
        '<button class="btn" data-a="0">KEEP IT</button>' +
      '</div>' +
    '</div>';
  layer.appendChild(d);
  Snd.riser(2.4);
  let n = 5;
  const clock = d.querySelector('#donClock');
  const iv = setInterval(function(){
    n--; clock.textContent = Math.max(0,n);
    Snd.heartbeat();
    if(n<=0){ clearInterval(iv); resolve(); }
  }, 1000);
  timers.push(iv);
  function resolve(){
    clearInterval(iv);
    d.querySelector('.surDonIn').innerHTML =
      '<div class="t" style="color:#9DFF3C">JUST KIDDING</div>' +
      '<div class="s">There was never a risk. It is your birthday. You keep it. 💜</div>';
    Snd.fanfare(); cannons(); rainConfetti(140); shake(); flashScreen(.5);
    later(function(){ end(); }, 3800);
  }
  d.querySelectorAll('button').forEach(function(b){ b.onclick = resolve; });
}

/* ---------- auto scheduler ---------- */
const OK_STATES = ['ready','awaitGift','failed','lost','gauntlet'];
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
};
})();

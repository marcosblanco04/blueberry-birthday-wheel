/* ============================================================
   10. ENDGAME - double or nothing, the Celsius fight, admin panel
   ============================================================ */

/* ------------------------------------------------------------
   DOUBLE OR NOTHING
   The NO button physically cannot be clicked. She has to say yes.
   Then she actually has to hit the 5% herself - unlimited tries,
   and the green zone quietly grows every time she misses.
   ------------------------------------------------------------ */
let donDone = false, donTries = 0;
let donRaf = null, donMoveHandler = null, donKeyHandler = null;

function donCleanup(){
  const no = document.getElementById('donNo');
  if(no){ no.onpointerdown = null; no.onclick = null; no.style.display = 'none'; }
  if(donRaf){ cancelAnimationFrame(donRaf); donRaf = null; }
  if(donMoveHandler){ window.removeEventListener('pointermove', donMoveHandler); donMoveHandler = null; }
  if(donKeyHandler){ window.removeEventListener('keydown', donKeyHandler, true); donKeyHandler = null; }
}

function startDoubleOrNothing(){
  phase = 'double'; state = 'don';
  donTries = 0;
  hub.disabled = true; hub.classList.remove('ready','waiting'); hub.textContent = '...';
  updCounter();
  document.getElementById('dim').classList.add('on');
  document.getElementById('donOffer').style.display = 'block';
  document.getElementById('donNo').style.display = 'block';
  document.getElementById('donRoll').style.display = 'none';
  document.getElementById('donOv').classList.add('on');
  Snd.riser(2.6);
  setTimeout(armDodgeButton, 500);
}

function armDodgeButton(){
  const no = document.getElementById('donNo');
  /* the card is transformed, which would make position:fixed resolve against
     the card instead of the viewport - so the button has to live on <body> */
  const r = no.getBoundingClientRect();
  document.body.appendChild(no);
  no.style.position = 'fixed';
  no.style.zIndex = '120';
  no.style.margin = '0';
  no.style.display = 'block';
  no.style.left = Math.max(10, Math.min(innerWidth  - r.width  - 10, r.left)) + 'px';
  no.style.top  = Math.max(10, Math.min(innerHeight - r.height - 10, r.top))  + 'px';

  function jump(){
    const w = no.offsetWidth || 200, h = no.offsetHeight || 56;
    const nx = 16 + Math.random()*Math.max(30, innerWidth  - w - 32);
    const ny = 16 + Math.random()*Math.max(30, innerHeight - h - 32);
    no.style.left = nx + 'px';
    no.style.top  = ny + 'px';
    no.style.transform = 'rotate(' + ((Math.random()-.5)*24) + 'deg)';
    Snd.tone(560 + Math.random()*500, .1, .18, 'square', undefined, 220);
  }
  donMoveHandler = function(e){
    const b = no.getBoundingClientRect();
    const cx = b.left + b.width/2, cy = b.top + b.height/2;
    if(Math.hypot(e.clientX - cx, e.clientY - cy) < 165) jump();
  };
  window.addEventListener('pointermove', donMoveHandler);
  no.onpointerdown = function(e){ e.preventDefault(); jump(); };
  no.onclick = function(e){ e.preventDefault(); jump(); };
  no.tabIndex = -1;
  no.onfocus = function(){ no.blur(); };
}

/* ---- the 5% roll: a needle she has to stop in the green ---- */
let rollNeedle = 0, rollDir = 1, rollSpeed = 1.55, rollActive = false;
let greenPos = 0, greenW = 0.05;

function donAccept(){
  if(state !== 'don') return;
  donCleanup();
  const no = document.getElementById('donNo');
  no.onpointerdown = no.onclick = null;
  no.style.display = 'none';
  state = 'donRoll';
  document.getElementById('donOffer').style.display = 'none';
  document.getElementById('donRoll').style.display = 'block';
  Snd.jackpot();
  newRoll();
}

function newRoll(){
  rollActive = true;
  rollSpeed = Math.max(.85, 1.55 - donTries*.12);
  greenW = Math.min(.30, .05 + donTries*.028);
  greenPos = .12 + Math.random()*.76;
  rollNeedle = 0; rollDir = 1;

  const g = document.getElementById('donGreen');
  g.style.left  = ((greenPos - greenW/2)*100) + '%';
  g.style.width = (greenW*100) + '%';
  document.getElementById('donResult').textContent = '';
  document.getElementById('donStop').textContent = 'STOP IT';
  document.getElementById('donStop').disabled = false;
  document.getElementById('donOdds').textContent =
    donTries === 0 ? 'YOUR ODDS: 5%' : ('THE WHEEL FEELS BAD FOR YOU: ' + Math.round(greenW*100) + '%');

  const needle = document.getElementById('donNeedle');
  let last = performance.now();
  function frame(now){
    if(!rollActive){ donRaf = null; return; }
    const dt = Math.min(.05, (now - last)/1000); last = now;
    rollNeedle += rollDir*rollSpeed*dt;
    if(rollNeedle >= 1){ rollNeedle = 1; rollDir = -1; Snd.clack(.5); }
    if(rollNeedle <= 0){ rollNeedle = 0; rollDir = 1; Snd.clack(.5); }
    needle.style.left = (rollNeedle*100) + '%';
    donRaf = requestAnimationFrame(frame);
  }
  donRaf = requestAnimationFrame(frame);

  donKeyHandler = function(e){
    if(e.code === 'Space' || e.key === ' '){ e.preventDefault(); e.stopPropagation(); donStop(); }
  };
  window.addEventListener('keydown', donKeyHandler, true);
}

function donStop(){
  if(!rollActive || state !== 'donRoll') return;
  rollActive = false;
  if(donRaf){ cancelAnimationFrame(donRaf); donRaf = null; }
  if(donKeyHandler){ window.removeEventListener('keydown', donKeyHandler, true); donKeyHandler = null; }
  document.getElementById('donStop').disabled = true;

  const rolled = Math.max(1, Math.round(rollNeedle*100));
  const dist = Math.abs(rollNeedle - greenPos);
  const forgiving = (greenW/2) * 1.35;          /* quiet help so it never feels brutal */
  const won = dist <= forgiving;

  document.getElementById('donResult').textContent = 'YOU ROLLED ' + rolled;

  if(won){
    Snd.fanfare(); Snd.jackpot();
    cannons(); rainConfetti(180); fireworks(7); shake(); flashScreen(1);
    document.getElementById('donStop').textContent = 'YOU HIT IT';
    document.getElementById('donOdds').textContent = 'YOU HIT THE 5%';
    setTimeout(donWin, 1500);
  } else {
    donTries++;
    Snd.buzzer(); shake(); flashScreen(.5, '#ff0033');
    document.getElementById('donOdds').textContent = 'SO CLOSE. GO AGAIN.';
    document.getElementById('donStop').textContent = 'AGAIN';
    document.getElementById('donStop').disabled = false;
    document.getElementById('donStop').onclick = function(){
      document.getElementById('donStop').onclick = donStop;
      newRoll();
    };
  }
}

function donWin(){
  donDone = true;
  donCleanup();
  document.getElementById('donOv').classList.remove('on');
  document.getElementById('dim').classList.remove('on');
  document.getElementById('donStop').onclick = donStop;

  phase = 'comeback';
  comebackBase = spinsTaken;
  spinsAllowed = spinsTaken + DON_SPINS;
  updCounter();

  winMode = true;
  document.getElementById('rays').classList.add('on');
  chaos(12);
  Snd.yippee(); cannons(); rainConfetti(160); fireworks(6);
  const b = document.getElementById('giftBanner');
  document.getElementById('giftText').textContent = '+2 BONUS SPINS!';
  b.classList.add('on');
  setTimeout(function(){
    b.classList.remove('on');
    document.getElementById('giftText').textContent = 'GIFT PURCHASED!';
  }, 5200);

  state = 'ready';
  hub.disabled = false; hub.classList.remove('waiting'); hub.classList.add('ready');
  hub.textContent = 'SPIN';
}

/* ------------------------------------------------------------
   THE CELSIUS FIGHT - the wheel is stuck, mash to break it free
   ------------------------------------------------------------ */
let celsiusDone = false, mashTries = 0;
let mashRaf = null, mashKey = null, mashPower = 0, mashActive = false;

function startCelsiusIntro(){
  phase = 'celsius'; state = 'celsiusIntro';
  updCounter();
  hub.disabled = true; hub.classList.remove('ready','waiting'); hub.textContent = '...';
  document.getElementById('dim').classList.add('on');
  document.getElementById('celsiusOv').classList.add('on');
  Snd.riser(2.4);
}

function mashCleanup(){
  mashActive = false;
  if(mashRaf){ cancelAnimationFrame(mashRaf); mashRaf = null; }
  if(mashKey){ window.removeEventListener('keydown', mashKey, true); mashKey = null; }
}

function startMash(){
  document.getElementById('celsiusOv').classList.remove('on');
  document.getElementById('dim').classList.remove('on');
  state = 'mash';
  mashPower = 0; mashActive = true; idleSpin = false;

  const need = Math.max(45, 100 - mashTries*15);
  const DUR = 12;
  let left = DUR, last = performance.now();

  const ov   = document.getElementById('mashOv');
  const fill = document.getElementById('mashFill');
  const mark = document.getElementById('mashMark');
  const time = document.getElementById('mashTime');
  const note = document.getElementById('mashNote');
  ov.classList.add('on');
  mark.style.left = Math.min(96, need/130*100) + '%';
  note.textContent = mashTries === 0
    ? 'The wheel will not budge. Break it loose.'
    : 'It is loosening. Attempt ' + (mashTries+1) + '.';

  function hit(){
    if(!mashActive) return;
    mashPower = Math.min(130, mashPower + 3);
    rot += 0.055;
    Snd.clack(1.1);
    if(Math.random() < .3) Snd.tone(90 + mashPower, .07, .2, 'square');
    fill.style.transform = 'scaleX(' + (mashPower/130) + ')';
  }
  mashKey = function(e){
    if(e.code === 'Space' || e.key === ' '){ e.preventDefault(); e.stopPropagation(); hit(); }
  };
  window.addEventListener('keydown', mashKey, true);
  document.getElementById('mashBtn').onpointerdown = function(e){ e.preventDefault(); hit(); };

  function frame(now){
    if(!mashActive){ mashRaf = null; return; }
    const dt = Math.min(.05, (now - last)/1000); last = now;
    left -= dt;
    mashPower = Math.max(0, mashPower - 6*dt);
    fill.style.transform = 'scaleX(' + (mashPower/130) + ')';
    time.textContent = Math.max(0, left).toFixed(1) + 's';
    if(mashPower >= need){ mashCleanup(); ov.classList.remove('on'); celsiusBreakFree(); return; }
    if(left <= 0){ mashCleanup(); ov.classList.remove('on'); celsiusFail(); return; }
    mashRaf = requestAnimationFrame(frame);
  }
  mashRaf = requestAnimationFrame(frame);
}

function celsiusFail(){
  mashTries++;
  state = 'celsiusIntro';
  Snd.buzzer(); setTimeout(function(){ Snd.sadTrombone(); }, 300);
  shake(); flashScreen(.5, '#ff0033');
  document.getElementById('celsiusTag').textContent = 'IT BARELY MOVED';
  document.getElementById('celsiusSub').textContent =
    'The wheel is heavy. It gave a little though - go again, it is easier now.';
  document.getElementById('celsiusBtn').textContent = 'AGAIN';
  document.getElementById('dim').classList.add('on');
  document.getElementById('celsiusOv').classList.add('on');
}

function celsiusBreakFree(){
  celsiusDone = true;
  state = 'spinning'; spinning = true;
  wrap.classList.add('zoom');
  shake(); flashScreen(1);
  Snd.whoosh(); Snd.riser(6.2); Snd.jackpot();
  cannons(); rainConfetti(120);
  const idx = idxOf('celsius24');
  runSpin(idx, {dur:6200, holdAt:.80, holdMs:1100, tension:true}, function(){
    land(ITEMS[idx]);
  });
}

/* ------------------------------------------------------------
   ADMIN PANEL - hidden. Backtick or paragraph key toggles it.
   ------------------------------------------------------------ */
const ADMIN = (function(){
  const ov = document.getElementById('adminOv');
  const body = document.getElementById('adminBody');
  let built = false;

  function group(title){
    const d = document.createElement('div');
    d.className = 'adGroup';
    d.innerHTML = '<h4>' + title + '</h4><div class="adRow"></div>';
    body.appendChild(d);
    return d.querySelector('.adRow');
  }
  function btn(row, label, fn){
    const b = document.createElement('button');
    b.className = 'adBtn'; b.textContent = label;
    b.onclick = function(e){ e.preventDefault(); try{ fn(); }catch(err){ console.error(err); } };
    row.appendChild(b);
    return b;
  }
  function closePanel(){ ov.classList.remove('on'); }
  function hideAllOverlays(){
    ['winOv','failOv','extraOv','lostOv','sumOv','donOv','celsiusOv','mashOv']
      .forEach(function(id){ const e=document.getElementById(id); if(e) e.classList.remove('on'); });
    document.getElementById('dim').classList.remove('on');
    document.getElementById('rays').classList.remove('on');
    document.getElementById('redveil').style.opacity = 0;
    document.getElementById('fakeWin').classList.remove('on','wait');
    document.body.classList.remove('chaos','sur-flip','sur-disco','mg-open');
    donCleanup(); mashCleanup();
    winMode = false; idleSpin = true; spinning = false; GRAV_MUL = 1;
    P.length = 0;
  }
  function armWheel(){
    hideAllOverlays();
    state = 'ready'; hub.disabled = false;
    hub.classList.remove('waiting'); hub.classList.add('ready'); hub.textContent = 'SPIN';
    updCounter();
  }

  function build(){
    if(built) return; built = true;

    let r = group('JUMP TO');
    btn(r, 'Losses (start)', function(){ phase='losses'; spinsTaken=0; spinsAllowed=LOSS_SPINS; armWheel(); });
    btn(r, 'You lost everything', function(){ hideAllOverlays(); phase='gauntlet'; spinsTaken=LOSS_SPINS; state='lost'; showLostEverything(); closePanel(); });
    btn(r, 'Open gauntlet', function(){ hideAllOverlays(); state='gauntlet'; MG.open(); closePanel(); });
    btn(r, 'Skip gauntlet (+2)', function(){ hideAllOverlays(); spinsTaken=LOSS_SPINS; gauntletCleared(); closePanel(); });
    btn(r, 'Double or nothing', function(){ hideAllOverlays(); phase='comeback'; donDone=false; startDoubleOrNothing(); closePanel(); });
    btn(r, 'Celsius fight', function(){ hideAllOverlays(); mashTries=0; celsiusDone=false; startCelsiusIntro(); closePanel(); });
    btn(r, 'Finale', function(){ hideAllOverlays(); phase='done'; state='done'; showFinale(); closePanel(); });
    btn(r, 'Full reset', function(){ location.reload(); });

    r = group('MINI GAMES  (opens the gauntlet at that stage)');
    ['1 Berry Catcher','2 Ork Rhythm','3 Berry Memory','4 Pyramid Dodge','5 Sea Lion Smack']
      .forEach(function(name, i){
        btn(r, name, function(){
          hideAllOverlays();
          state = 'gauntlet';
          if(!MG.active()) MG.open();
          setTimeout(function(){ MG.goto(i); }, 60);
          closePanel();
        });
      });
    btn(r, 'Win current stage', function(){ MG.skip(); closePanel(); });
    btn(r, 'Close gauntlet', function(){ MG.abort(); hideAllOverlays(); armWheel(); });

    r = group('FORCE NEXT SPIN');
    ITEMS.filter(function(it){ return it.win || it.final || it.secret; }).forEach(function(it){
      btn(r, it.n, function(){ override = it.k; armWheel(); closePanel(); });
    });
    btn(r, 'FAILED', function(){ override='FAIL'; armWheel(); closePanel(); });
    btn(r, 'Clear forced', function(){ override=null; });

    r = group('FAKE-OUT');
    btn(r, 'Auto (55%)', function(){ fakeOutForced=null; });
    btn(r, 'Always', function(){ fakeOutForced=true; });
    btn(r, 'Never', function(){ fakeOutForced=false; });

    r = group('SURPRISES');
    SUR.list().forEach(function(name, i){ btn(r, name, function(){ closePanel(); SUR.play(i); }); });
    btn(r, 'Next in queue', function(){ closePanel(); SUR.next(); });
    btn(r, 'Fire all remaining', function(){ closePanel(); SUR.flush(); });

    r = group('PRIZES');
    btn(r, 'Clear won list', function(){ WON.length = 0; buildTracker(); buildWheelSprite(); });
    ITEMS.filter(function(it){ return it.win || it.final || it.secret; }).forEach(function(it){
      btn(r, 'Mark won: ' + it.n, function(){ markTracker(it.k); });
    });

    r = group('MISC');
    btn(r, 'Show secret prize card', function(){
      closePanel();
      document.getElementById('dim').classList.add('on');
      startSecretCountdown();
      document.getElementById('sumOv').classList.add('on');
    });
    btn(r, 'Mute / unmute', function(){ Snd.muted = !Snd.muted; });
    btn(r, 'Confetti', function(){ cannons(); rainConfetti(160); fireworks(3); });
    btn(r, 'Close panel', closePanel);
  }

  function toggle(){
    build();
    ov.classList.toggle('on');
    const s = document.getElementById('adminState');
    if(s) s.textContent = 'phase=' + phase + '  state=' + state +
      '  spins=' + spinsTaken + '/' + spinsAllowed +
      '  won=' + WON.length + '  surprises left=' + SUR.remaining();
  }
  return { toggle:toggle, close:closePanel };
})();

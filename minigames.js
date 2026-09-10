/* ============================================================
   8. THE COMEBACK GAUNTLET - 5 mini games, ~10 minutes
   Rules: hard, but unlimited retries and every retry gets
   easier, so it is always winnable. Clear all 5 => +2 spins.
   ============================================================ */
const MG = (function(){

const LW = 960, LH = 540;                 /* logical play field */
const ov   = document.getElementById('mgOv');
const cv   = document.getElementById('mgCanvas');
const ctx  = cv.getContext('2d');
const hud  = document.getElementById('mgHud');
const card = document.getElementById('mgCard');
const cTag = document.getElementById('mgCardTag');
const cSub = document.getElementById('mgCardSub');
const cRule= document.getElementById('mgCardRule');
const cBtn = document.getElementById('mgCardBtn');
const pills= document.getElementById('mgPills');

let SC = 1;
let raf = null, running = false, lastT = 0;
let game = null, stageIdx = 0, fails = {}, activeFlag = false;
const held = {};
let bound = [];

function on(t,e,f){ t.addEventListener(e,f); bound.push([t,e,f]); }
function unbindAll(){ bound.forEach(function(b){ b[0].removeEventListener(b[1],b[2]); }); bound=[]; }

function fit(){
  const w = Math.min(innerWidth*0.94, (innerHeight*0.72)*LW/LH);
  const h = w*LH/LW;
  cv.style.width = w+'px'; cv.style.height = h+'px';
  cv.width  = Math.max(2,Math.round(w*DPR));
  cv.height = Math.max(2,Math.round(h*DPR));
  SC = (w/LW)*DPR;
}
addEventListener('resize', function(){ if(activeFlag) fit(); });

function pt(e){
  const r = cv.getBoundingClientRect();
  const cx = (e.touches ? e.touches[0].clientX : e.clientX);
  const cy = (e.touches ? e.touches[0].clientY : e.clientY);
  return { x:(cx-r.left)/r.width*LW, y:(cy-r.top)/r.height*LH };
}

/* ---------- shared drawing helpers ---------- */
function bgGrid(t){
  ctx.fillStyle='#0d0326'; ctx.fillRect(0,0,LW,LH);
  const g=ctx.createRadialGradient(LW/2,LH*.42,40,LW/2,LH*.42,LW*.72);
  g.addColorStop(0,'rgba(90,30,180,.55)'); g.addColorStop(1,'rgba(8,2,24,0)');
  ctx.fillStyle=g; ctx.fillRect(0,0,LW,LH);
  ctx.strokeStyle='rgba(255,255,255,.05)'; ctx.lineWidth=1;
  const off=(t*26)%44;
  for(let x=-44+off;x<LW;x+=44){ ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,LH); ctx.stroke(); }
  for(let y=-44+off;y<LH;y+=44){ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(LW,y); ctx.stroke(); }
}
function txt(s,x,y,size,col,align,weight){
  ctx.font=(weight||900)+' '+size+'px Outfit, system-ui, sans-serif';
  ctx.textAlign=align||'center'; ctx.textBaseline='middle';
  ctx.lineWidth=size*.28; ctx.lineJoin='round'; ctx.strokeStyle='rgba(0,0,0,.65)';
  ctx.strokeText(s,x,y); ctx.fillStyle=col||'#fff'; ctx.fillText(s,x,y);
}
function roundRect(x,y,w,h,r){
  ctx.beginPath();
  ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r);
  ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath();
}
function pulse(t){ return .5+.5*Math.sin(t*6); }

/* ============================================================
   GAME 1 - BERRY CATCHER
   ============================================================ */
function gameCatch(env){
  const m = env.mercy;
  const need = Math.max(45, 80 - m*10);
  let lives = 5 + m;
  let caught = 0, t = 0, spawnAt = .5, items = [], px = LW/2, pop = 0, shakeT = 0;
  const BW = 130 + m*22, BH = 26;

  function interval(){ return Math.max(.34, .72 - t*.0028); }
  function fallSpeed(){ return Math.min(470, 200 + t*3.1); }

  on(cv,'pointermove',function(e){ px = pt(e).x; });
  on(window,'keydown',function(e){ held[e.key.toLowerCase()]=1; });
  on(window,'keyup',function(e){ held[e.key.toLowerCase()]=0; });

  return {
    update:function(dt){
      t+=dt; spawnAt-=dt; pop=Math.max(0,pop-dt*4); shakeT=Math.max(0,shakeT-dt*3);
      if(held['arrowleft']||held['a']) px-=760*dt;
      if(held['arrowright']||held['d']) px+=760*dt;
      px = Math.max(BW/2, Math.min(LW-BW/2, px));

      if(spawnAt<=0){
        spawnAt = interval();
        const r = Math.random();
        const kind = r<.20 ? 'bomb' : (r<.28 ? 'gold' : 'berry');
        items.push({ x:40+Math.random()*(LW-80), y:-30, k:kind,
                     v:fallSpeed()*(.85+Math.random()*.3), r:kind==='gold'?17:15, sp:Math.random()*6 });
      }
      const by = LH-52;
      for(let i=items.length-1;i>=0;i--){
        const o=items[i]; o.y += o.v*dt; o.sp += dt*4;
        if(o.y > by-o.r && o.y < by+BH+o.r && Math.abs(o.x-px) < BW/2+o.r*.7){
          items.splice(i,1);
          if(o.k==='bomb'){ lives--; shakeT=1; Snd.buzzer(); flashScreen(.22,'#ff0033'); shake();
            if(lives<=0){ env.lose(); return; } }
          else {
            const add = o.k==='gold'?3:1;
            caught += add; pop=1;
            Snd.ding(o.k==='gold'?1400:820+Math.random()*260,undefined,.55);
            if(o.k==='gold'){ Snd.coins(4); }
            if(caught>=need){ env.win(); return; }
          }
          continue;
        }
        if(o.y > LH+40) items.splice(i,1);
      }
      env.hud('CAUGHT '+caught+' / '+need+'   ·   LIVES '+lives);
    },
    draw:function(){
      ctx.save();
      if(shakeT>0) ctx.translate((Math.random()-.5)*10*shakeT,(Math.random()-.5)*10*shakeT);
      bgGrid(t);
      const by = LH-52;
      /* basket */
      ctx.save();
      ctx.shadowColor='rgba(255,63,208,.9)'; ctx.shadowBlur=26;
      const gg=ctx.createLinearGradient(px-BW/2,0,px+BW/2,0);
      gg.addColorStop(0,'#FF3FD0'); gg.addColorStop(.5,'#8B3DFF'); gg.addColorStop(1,'#22E7FF');
      ctx.fillStyle=gg; roundRect(px-BW/2,by,BW,BH,10); ctx.fill();
      ctx.restore();
      ctx.fillStyle='rgba(255,255,255,.35)'; roundRect(px-BW/2+6,by+4,BW-12,6,3); ctx.fill();

      items.forEach(function(o){
        ctx.save(); ctx.translate(o.x,o.y); ctx.rotate(Math.sin(o.sp)*.3);
        if(o.k==='bomb'){
          ctx.fillStyle='#1a1a22'; ctx.beginPath(); ctx.arc(0,0,o.r,0,7); ctx.fill();
          ctx.strokeStyle='#ff3355'; ctx.lineWidth=3; ctx.stroke();
          ctx.font='18px serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
          ctx.fillText('💣',0,1);
        } else if(o.k==='gold'){
          ctx.shadowColor='rgba(255,212,71,1)'; ctx.shadowBlur=20;
          ctx.fillStyle='#FFD447'; ctx.beginPath(); ctx.arc(0,0,o.r,0,7); ctx.fill();
          ctx.shadowBlur=0; ctx.font='19px serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
          ctx.fillText('⭐',0,1);
        } else {
          ctx.shadowColor='rgba(120,80,255,.9)'; ctx.shadowBlur=14;
          ctx.fillStyle='#7a4cff'; ctx.beginPath(); ctx.arc(0,0,o.r,0,7); ctx.fill();
          ctx.shadowBlur=0; ctx.font='18px serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
          ctx.fillText('🫐',0,1);
        }
        ctx.restore();
      });
      if(pop>0) txt('+',px,by-30-pop*18,26+pop*14,'rgba(255,255,255,'+pop+')');
      ctx.restore();
    }
  };
}

/* ============================================================
   GAME 2 - ORK RHYTHM  (D F J K)
   ============================================================ */
function gameRhythm(env){
  const m = env.mercy;
  const KEYS = ['d','f','j','k'];
  const COLS = ['#FF3FD0','#FFD447','#22E7FF','#9DFF3C'];
  const TRAVEL = 1.9, HITLINE = LH-96;
  const WIN_MS = 0.155 + m*0.035;
  const needPct = Math.max(.48, .70 - m*.06);

  /* ============ THE SONG ============
     120 BPM, Am - F - C - G, built from one seeded pass so the
     chart and the music are literally the same notes.            */
  const BPM = 120, STEP = 30/BPM;            /* 8th note = .25s */
  const START = 2.4, STEPS = 392;            /* ~100 s of song   */
  const CHORDS = [                            /* one bar each     */
    [57,60,64,69,72],                         /* Am  A C E A C    */
    [53,57,60,65,69],                         /* F   F A C F A    */
    [48,55,60,64,67],                         /* C   C G C E G    */
    [55,59,62,67,71]                          /* G   G B D G B    */
  ];
  /* note density per 16-step phrase - it thickens as the song goes */
  const PHRASES = [
    [1,0,0,0, 0,1,0,0, 1,0,0,0, 0,1,0,0],
    [1,0,0,1, 0,1,0,0, 1,0,0,1, 0,0,0,0],
    [1,0,1,0, 0,1,0,0, 1,0,1,0, 0,1,0,0],
    [1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,0,1]
  ];

  let seed = 4242;
  function rnd(){ seed = (seed*1103515245 + 12345) & 0x7fffffff; return seed/0x7fffffff; }

  const song = [];    /* {t,type,midi} - what you hear   */
  const chart = [];   /* {t,lane,hit,dead} - what you play */

  for(let i=0;i<STEPS;i++){
    const t = START + i*STEP;
    const bar = (i/8)|0;
    const chord = CHORDS[bar % 4];
    const prog = i/STEPS;
    const phrase = PHRASES[Math.min(3, Math.floor(prog*4))];

    /* drums */
    if(i%8===0 || i%8===6) song.push({t:t, type:'kick'});
    if(i%8===4)           song.push({t:t, type:'snare'});
    if(i%2===0)           song.push({t:t, type:'hat'});

    /* bass */
    if(i%4===0) song.push({t:t, type:'bass', midi:chord[0]-12});

    /* melody + the playable chart */
    if(phrase[i%16]){
      const deg = (rnd()*chord.length)|0;
      const midi = chord[deg] + (rnd()<.25 ? 12 : 0);
      song.push({t:t, type:'lead', midi:midi});
      chart.push({t:t, lane:deg % 4, hit:false, dead:false});
    }
  }
  const endT = START + STEPS*STEP + 1.4;
  const TOTAL = chart.length;

  /* ---- audio playback with a small lookahead scheduler ---- */
  const A0 = Snd.ctx ? Snd.ctx.currentTime : 0;
  let songIdx = 0;
  function playNote(e){
    if(!Snd.ctx || Snd.muted) return;
    const when = A0 + e.t;
    const hz = e.midi ? 440*Math.pow(2,(e.midi-69)/12) : 0;
    if(e.type==='kick'){ Snd.tone(120,.22,.5,'sine',when,42); Snd.noise(.05,90,1,.18,'lowpass',when); }
    else if(e.type==='snare'){ Snd.noise(.14,1900,1.1,.20,'bandpass',when); Snd.tone(190,.09,.16,'triangle',when,110); }
    else if(e.type==='hat'){ Snd.noise(.035,9000,2.2,.055,'highpass',when); }
    else if(e.type==='bass'){ Snd.tone(hz,.42,.22,'square',when); Snd.tone(hz/2,.42,.12,'sine',when); }
    else if(e.type==='lead'){ Snd.tone(hz,.30,.085,'square',when); Snd.tone(hz*2.005,.16,.035,'triangle',when); }
  }
  function pump(now){
    while(songIdx < song.length && song[songIdx].t < now + 1.1){
      playNote(song[songIdx]); songIdx++;
    }
  }

  /* ---- the sea lions that get in the way ---- */
  const lions = [];
  let lionAt = 9 - m*1.2;
  const LION_DUR = Math.max(1.9, 3.0 - m*.3);

  let t = 0, hits = 0, misses = 0, combo = 0, best = 0;
  let flash = [0,0,0,0], judge = '', judgeT = 0;

  function judgeHit(lane){
    let bestNote = null, bestD = 9;
    for(let i=0;i<chart.length;i++){
      const n = chart[i];
      if(n.hit || n.dead) continue;
      const d = Math.abs(n.t - t);
      if(d < bestD){ bestD = d; bestNote = n; }
      if(n.t - t > WIN_MS + .3) break;
    }
    flash[lane] = 1;
    if(bestNote && bestNote.lane === lane && bestD <= WIN_MS){
      bestNote.hit = true; hits++; combo++; best = Math.max(best, combo);
      judge = bestD < WIN_MS*.4 ? 'PERFECT!' : 'GOOD'; judgeT = 1;
      Snd.ding(660 + lane*140, undefined, .42);
      if(combo % 12 === 0){ Snd.coins(5); burst(innerWidth/2, innerHeight*.55, 26, {speed:11,g:.2}); }
    } else {
      combo = 0; judge = 'MISS'; judgeT = 1; Snd.clack(1.2);
    }
  }

  on(window,'keydown',function(e){
    if(e.repeat) return;
    const i = KEYS.indexOf(e.key.toLowerCase());
    if(i >= 0){ e.preventDefault(); judgeHit(i); }
  });

  return {
    update:function(dt){
      /* the audio clock is the truth - rAF drift can never desync the chart */
      t = Snd.ctx ? (Snd.ctx.currentTime - A0) : (t + dt);
      pump(t);

      judgeT = Math.max(0, judgeT - dt*1.6);
      for(let i=0;i<4;i++) flash[i] = Math.max(0, flash[i] - dt*4);

      for(let i=0;i<chart.length;i++){
        const n = chart[i];
        if(!n.hit && !n.dead && t - n.t > WIN_MS){ n.dead = true; misses++; combo = 0; }
      }

      /* sea lion interference */
      lionAt -= dt;
      if(lionAt <= 0 && t < endT - 6){
        lionAt = (7 + Math.random()*5) + m*1.5;
        lions.push({ lane:(Math.random()*4)|0, life:LION_DUR, max:LION_DUR });
        Snd.bark(undefined, .9 + Math.random()*.3);
        judge = 'SEA LION!'; judgeT = 1;
      }
      for(let i=lions.length-1;i>=0;i--){
        lions[i].life -= dt;
        if(lions[i].life <= 0) lions.splice(i,1);
      }

      const pct = hits / TOTAL;
      env.hud('HITS ' + hits + ' / ' + TOTAL + '   ·   COMBO ' + combo +
              '   ·   NEED ' + Math.round(needPct*100) + '%   ·   NOW ' + Math.round(pct*100) + '%');

      if(t > endT){ if(pct >= needPct) env.win(); else env.lose(); return; }
      let alive = 0;
      for(let i=0;i<chart.length;i++) if(!chart[i].hit && !chart[i].dead) alive++;
      if((hits + alive)/TOTAL < needPct) env.lose();
    },

    draw:function(){
      bgGrid(t);
      const laneW = 120, x0 = LW/2 - laneW*2;

      for(let i=0;i<4;i++){
        const x = x0 + i*laneW;
        ctx.fillStyle = 'rgba(255,255,255,.045)'; ctx.fillRect(x+4, 0, laneW-8, LH);
        ctx.fillStyle = 'rgba(255,255,255,' + (0.06 + flash[i]*.32) + ')';
        ctx.fillRect(x+4, HITLINE-30, laneW-8, 60);
        ctx.save(); ctx.shadowColor = COLS[i]; ctx.shadowBlur = 12 + flash[i]*26;
        ctx.strokeStyle = COLS[i]; ctx.lineWidth = 4;
        roundRect(x+10, HITLINE-24, laneW-20, 48, 12); ctx.stroke(); ctx.restore();
        txt(KEYS[i].toUpperCase(), x + laneW/2, HITLINE, 24, COLS[i]);
      }

      chart.forEach(function(n){
        if(n.hit) return;
        const dt2 = n.t - t;
        if(dt2 > TRAVEL || dt2 < -.35) return;
        const y = HITLINE - (dt2/TRAVEL)*(HITLINE+60);
        const x = x0 + n.lane*laneW;
        ctx.save();
        ctx.globalAlpha = n.dead ? .25 : 1;
        ctx.shadowColor = COLS[n.lane]; ctx.shadowBlur = 18;
        ctx.fillStyle = COLS[n.lane];
        roundRect(x+14, y-16, laneW-28, 32, 10); ctx.fill();
        ctx.restore();
      });

      /* sea lions flop into the lane and block the view */
      lions.forEach(function(L){
        const x = x0 + L.lane*laneW;
        const k = 1 - L.life/L.max;
        const slide = Math.min(1, k*5) * Math.min(1, L.life*5);   /* in, hold, out */
        const top = 0, h = HITLINE - 150;
        ctx.save();
        ctx.globalAlpha = .93*slide;
        ctx.fillStyle = '#0d0326';
        roundRect(x+4, top, laneW-8, h, 14); ctx.fill();
        ctx.strokeStyle = '#22E7FF'; ctx.lineWidth = 3; ctx.stroke();
        ctx.globalAlpha = slide;
        ctx.font = '74px serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText('🦭', x + laneW/2, h*.5 + Math.sin(t*9)*10);
        txt('ORK', x + laneW/2, h*.5 + 62, 22, '#22E7FF');
        ctx.restore();
      });

      if(judgeT > 0){
        const col = judge === 'MISS' ? 'rgba(255,80,110,' + judgeT + ')'
                  : judge === 'SEA LION!' ? 'rgba(34,231,255,' + judgeT + ')'
                  : 'rgba(255,255,255,' + judgeT + ')';
        txt(judge, LW/2, HITLINE-120, 34 + judgeT*10, col);
      }
      txt('ORK ORK RHYTHM', LW/2, 34, 24, 'rgba(255,255,255,.55)');
    }
  };
}

/* ============================================================
   GAME 3 - BERRY MEMORY
   ============================================================ */
function gameMemory(env){
  const m = env.mercy;
  const pool = ITEMS.filter(function(it){ return imgs[it.k] && !it.fail && !it.extra; }).slice(0,12);
  const PAIRS = pool.length;
  let deck = [];
  pool.forEach(function(it,i){ deck.push({k:it.k,id:i}); deck.push({k:it.k,id:i}); });
  for(let i=deck.length-1;i>0;i--){ const j=(Math.random()*(i+1))|0; const s=deck[i]; deck[i]=deck[j]; deck[j]=s; }

  const COLS_N = 6, ROWS = Math.ceil(deck.length/COLS_N);
  const CW = 128, CH = 78, GAP = 12;
  const gridW = COLS_N*CW + (COLS_N-1)*GAP, gridH = ROWS*CH + (ROWS-1)*GAP;
  const gx = (LW-gridW)/2, gy = (LH-gridH)/2 + 14;

  deck.forEach(function(c,i){
    c.col = i%COLS_N; c.row = (i/COLS_N)|0;
    c.x = gx + c.col*(CW+GAP); c.y = gy + c.row*(CH+GAP);
    c.face = 0; c.done = false;
  });

  let t=0, left = 155 + m*45, a=null, b=null, lockT=0, matched=0, tries=0;

  on(cv,'pointerdown',function(e){
    if(lockT>0) return;
    const p = pt(e);
    for(let i=0;i<deck.length;i++){
      const c=deck[i];
      if(c.done || c===a) continue;
      if(p.x>c.x && p.x<c.x+CW && p.y>c.y && p.y<c.y+CH){
        if(!a){ a=c; Snd.clack(.9); }
        else if(!b){
          b=c; tries++; Snd.clack(.9);
          if(a.id===b.id){
            a.done=b.done=true; matched++;
            Snd.ding(700+matched*70,undefined,.7); Snd.coins(3);
            burst(innerWidth/2, innerHeight/2, 22, {speed:10,g:.2});
            a=b=null;
            if(matched>=PAIRS){ env.win(); }
          } else { lockT=.75; }
        }
        return;
      }
    }
  });

  return {
    update:function(dt){
      t+=dt; left-=dt;
      deck.forEach(function(c){
        const want = (c===a||c===b||c.done) ? 1 : 0;
        c.face += (want-c.face)*Math.min(1,dt*11);
      });
      if(lockT>0){ lockT-=dt; if(lockT<=0){ a=b=null; } }
      env.hud('PAIRS '+matched+' / '+PAIRS+'   ·   TIME '+Math.max(0,left).toFixed(0)+'s   ·   FLIPS '+tries);
      if(left<=0) env.lose();
    },
    draw:function(){
      bgGrid(t);
      txt('BERRY MEMORY  -  match every pair before the clock dies', LW/2, 30, 20, 'rgba(255,255,255,.6)');
      /* timer bar */
      const totalT = 155 + m*45;
      ctx.fillStyle='rgba(255,255,255,.12)'; roundRect(LW/2-260,48,520,9,5); ctx.fill();
      ctx.fillStyle = left<25 ? '#ff3355' : '#22E7FF';
      roundRect(LW/2-260,48,520*Math.max(0,left/totalT),9,5); ctx.fill();

      deck.forEach(function(c){
        const f = c.face, sx = Math.abs(Math.cos(f*Math.PI));
        ctx.save();
        ctx.translate(c.x+CW/2, c.y+CH/2);
        ctx.scale(Math.max(.02,sx), 1);
        ctx.globalAlpha = c.done ? .55 : 1;
        if(f<.5){
          const g=ctx.createLinearGradient(-CW/2,-CH/2,CW/2,CH/2);
          g.addColorStop(0,'#8B3DFF'); g.addColorStop(1,'#3d1080');
          ctx.fillStyle=g; roundRect(-CW/2,-CH/2,CW,CH,12); ctx.fill();
          ctx.strokeStyle='rgba(255,212,71,.7)'; ctx.lineWidth=3; ctx.stroke();
          ctx.font='30px serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
          ctx.fillText('🫐',0,2);
        } else {
          ctx.fillStyle='#fff'; roundRect(-CW/2,-CH/2,CW,CH,12); ctx.fill();
          ctx.strokeStyle= c.done ? '#9DFF3C' : '#FFD447'; ctx.lineWidth=3; ctx.stroke();
          const im=imgs[c.k];
          if(im && im.complete && im.naturalWidth){
            const ar=im.naturalWidth/im.naturalHeight;
            let w=CW-16, h=w/ar;
            if(h>CH-14){ h=CH-14; w=h*ar; }
            ctx.drawImage(im,-w/2,-h/2,w,h);
          }
        }
        ctx.restore();
      });
    }
  };
}

/* ============================================================
   GAME 4 - PYRAMID DODGE
   ============================================================ */
function gameDodge(env){
  const m = env.mercy;
  const SURVIVE = Math.max(45, 80 - m*9);
  let lives = 3 + m, t=0, inv=0, spawnAt=1.2, shots=[], px=LW/2, py=LH/2, useMouse=false;

  on(cv,'pointermove',function(e){ const p=pt(e); px=p.x; py=p.y; useMouse=true; });
  on(window,'keydown',function(e){ held[e.key.toLowerCase()]=1; });
  on(window,'keyup',function(e){ held[e.key.toLowerCase()]=0; });

  function interval(){ return Math.max(.18, .62 - t*.0055); }
  function speed(){ return 190 + t*3.4; }

  return {
    update:function(dt){
      t+=dt; inv=Math.max(0,inv-dt); spawnAt-=dt;
      const kb = 470*dt;
      if(held['arrowleft']||held['a']){ px-=kb; useMouse=false; }
      if(held['arrowright']||held['d']){ px+=kb; useMouse=false; }
      if(held['arrowup']||held['w']){ py-=kb; useMouse=false; }
      if(held['arrowdown']||held['s']){ py+=kb; useMouse=false; }
      px=Math.max(16,Math.min(LW-16,px)); py=Math.max(16,Math.min(LH-16,py));

      if(spawnAt<=0){
        spawnAt=interval();
        const n = 1 + (t>30?1:0) + (t>55?1:0);
        for(let i=0;i<n;i++){
          const side=(Math.random()*4)|0;
          let x,y;
          if(side===0){ x=Math.random()*LW; y=-20; }
          else if(side===1){ x=LW+20; y=Math.random()*LH; }
          else if(side===2){ x=Math.random()*LW; y=LH+20; }
          else { x=-20; y=Math.random()*LH; }
          const ang=Math.atan2(py-y, px-x) + (Math.random()-.5)*.5;
          const sp=speed()*(.85+Math.random()*.35);
          shots.push({x:x,y:y,vx:Math.cos(ang)*sp,vy:Math.sin(ang)*sp,r:9+Math.random()*5,rot:Math.random()*7});
        }
      }
      for(let i=shots.length-1;i>=0;i--){
        const s=shots[i]; s.x+=s.vx*dt; s.y+=s.vy*dt; s.rot+=dt*5;
        if(s.x<-60||s.x>LW+60||s.y<-60||s.y>LH+60){ shots.splice(i,1); continue; }
        if(inv<=0){
          const dx=s.x-px, dy=s.y-py;
          if(dx*dx+dy*dy < (s.r+13)*(s.r+13)){
            shots.splice(i,1); lives--; inv=1.4;
            Snd.buzzer(); flashScreen(.3,'#ff0033'); shake();
            if(lives<=0){ env.lose(); return; }
          }
        }
      }
      env.hud('SURVIVE '+Math.min(SURVIVE,t).toFixed(1)+' / '+SURVIVE+'s   ·   LIVES '+lives);
      if(t>=SURVIVE){ env.win(); }
    },
    draw:function(){
      bgGrid(t);
      ctx.fillStyle='rgba(255,255,255,.12)'; roundRect(LW/2-280,26,560,10,5); ctx.fill();
      ctx.fillStyle='#9DFF3C'; roundRect(LW/2-280,26,560*Math.min(1,t/SURVIVE),10,5); ctx.fill();
      txt('DODGE THE PYRAMID HEADS', LW/2, 60, 20, 'rgba(255,255,255,.55)');

      shots.forEach(function(s){
        ctx.save(); ctx.translate(s.x,s.y); ctx.rotate(s.rot);
        ctx.shadowColor='rgba(255,40,80,.9)'; ctx.shadowBlur=16;
        ctx.fillStyle='#ff2a4d'; ctx.beginPath();
        ctx.moveTo(0,-s.r); ctx.lineTo(s.r,s.r); ctx.lineTo(-s.r,s.r); ctx.closePath(); ctx.fill();
        ctx.restore();
      });
      ctx.save();
      ctx.globalAlpha = inv>0 ? (.35+.65*Math.abs(Math.sin(t*22))) : 1;
      ctx.shadowColor='rgba(34,231,255,1)'; ctx.shadowBlur=24;
      ctx.fillStyle='#22E7FF'; ctx.beginPath(); ctx.arc(px,py,13,0,7); ctx.fill();
      ctx.shadowBlur=0; ctx.font='16px serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
      ctx.fillText('🫐',px,py+1);
      ctx.restore();
      txt(useMouse?'mouse to move':'WASD / arrows', LW/2, LH-22, 15, 'rgba(255,255,255,.35)');
    }
  };
}

/* ============================================================
   GAME 5 - SEA LION SMACK
   ============================================================ */
function gameSmack(env){
  const m = env.mercy;
  const need = Math.max(22, 35 - m*4);
  const allowMiss = 10 + m*4;
  let t=0, hits=0, missed=0, spawnAt=.6, holes=[], pops=[];

  const COLS_N=4, ROWS=3, HW=150, HH=104, GX=(LW-(COLS_N*HW))/2, GY=118;
  for(let r=0;r<ROWS;r++) for(let c=0;c<COLS_N;c++)
    holes.push({ x:GX+c*HW+HW/2, y:GY+r*HH+HH/2, up:0, life:0, max:0, smacked:false });

  function showTime(){ return Math.max(.62, 1.25 + m*.22 - t*.006); }
  function interval(){ return Math.max(.34, .78 - t*.004); }

  on(cv,'pointerdown',function(e){
    const p=pt(e);
    let got=false;
    holes.forEach(function(h){
      if(h.life>0 && !h.smacked && Math.abs(p.x-h.x)<52 && Math.abs(p.y-h.y)<46){
        h.smacked=true; h.life=Math.min(h.life,.18); hits++; got=true;
        pops.push({x:h.x,y:h.y,t:1});
        if(hits%5===0){ Snd.seaLionLaugh(undefined,.35); } else { Snd.bark(); }
        Snd.ding(900+Math.random()*400,undefined,.5);
        if(hits>=need){ env.win(); }
      }
    });
    if(!got){ Snd.clack(.8); }
  });

  return {
    update:function(dt){
      t+=dt; spawnAt-=dt;
      if(spawnAt<=0){
        spawnAt=interval();
        const free=holes.filter(function(h){ return h.life<=0; });
        if(free.length){
          const h=free[(Math.random()*free.length)|0];
          h.max=showTime(); h.life=h.max; h.smacked=false;
        }
      }
      holes.forEach(function(h){
        if(h.life>0){
          h.life-=dt;
          const k=1-h.life/h.max;
          h.up = Math.min(1, Math.sin(Math.min(1,k*1.6)*Math.PI*.5)*1.15);
          if(h.life<=0){
            h.up=0;
            if(!h.smacked){ missed++; Snd.clack(.5); flashScreen(.12,'#ff0033'); }
          }
        }
      });
      for(let i=pops.length-1;i>=0;i--){ pops[i].t-=dt*2.2; if(pops[i].t<=0) pops.splice(i,1); }
      env.hud('SMACKED '+hits+' / '+need+'   ·   ESCAPED '+missed+' / '+allowMiss);
      if(missed>=allowMiss) env.lose();
    },
    draw:function(){
      bgGrid(t);
      txt('SMACK THE SEA LIONS - click them before they escape', LW/2, 40, 20, 'rgba(255,255,255,.6)');
      holes.forEach(function(h){
        ctx.save();
        ctx.fillStyle='rgba(0,0,0,.42)';
        ctx.beginPath(); ctx.ellipse(h.x,h.y+34,54,17,0,0,7); ctx.fill();
        if(h.up>0.02){
          const yy = h.y+34 - h.up*62;
          ctx.save();
          ctx.translate(h.x, yy);
          ctx.scale(1, .85+h.up*.2);
          ctx.shadowColor = h.smacked ? 'rgba(157,255,60,.9)' : 'rgba(34,231,255,.75)';
          ctx.shadowBlur = 20;
          ctx.fillStyle = h.smacked ? '#9DFF3C' : '#6a4a3a';
          ctx.beginPath(); ctx.ellipse(0,0,40,34,0,0,7); ctx.fill();
          ctx.shadowBlur=0;
          ctx.font='42px serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
          ctx.fillText(h.smacked?'💥':'🦭',0,2);
          ctx.restore();
        }
        ctx.restore();
      });
      pops.forEach(function(p){
        txt('+1', p.x, p.y-40-(1-p.t)*26, 26, 'rgba(157,255,60,'+p.t+')');
      });
    }
  };
}

/* ============================================================
   STAGES
   ============================================================ */
const STAGES = [
  { id:'catch',  name:'BERRY CATCHER', icon:'🫐',
    rule:'Catch the blueberries. Dodge the bombs. Gold stars are worth 3.',
    ctrl:'Mouse or ← →', make:gameCatch },
  { id:'rhythm', name:'ORK RHYTHM', icon:'🎵',
    rule:'Hit the notes as they cross the line. Keep the combo alive.',
    ctrl:'D  F  J  K', make:gameRhythm },
  { id:'memory', name:'BERRY MEMORY', icon:'🧠',
    rule:'Find every matching pair from the wishlist before the clock runs out.',
    ctrl:'Click the cards', make:gameMemory },
  { id:'dodge',  name:'PYRAMID DODGE', icon:'🔺',
    rule:'Survive the barrage. Three hits and it is over.',
    ctrl:'Mouse or WASD', make:gameDodge },
  { id:'smack',  name:'SEA LION SMACK', icon:'🦭',
    rule:'Smack every sea lion before it ducks back down. Let too many escape and you lose.',
    ctrl:'Click them', make:gameSmack }
];

/* ============================================================
   ENGINE
   ============================================================ */
function stopLoop(){
  if(raf){ cancelAnimationFrame(raf); raf=null; }
  running=false; game=null;
  unbindAll();
  for(const k in held) held[k]=0;
}

function loop(now){
  if(!running){ return; }
  const dt = Math.min(.05, (now-lastT)/1000); lastT=now;
  raf = requestAnimationFrame(loop);
  try{
    if(game){ game.update(dt); }
    if(game){ ctx.setTransform(SC,0,0,SC,0,0); game.draw(); }
  }catch(err){
    /* never let a mini game soft-lock the show */
    console.error('minigame error', err);
    stopLoop(); stageWin();
  }
}

function showCard(tag, sub, rule, btnText, btnFn, cls){
  card.className = 'mgCard ' + (cls||'');
  cTag.textContent = tag; cSub.textContent = sub; cRule.textContent = rule;
  cBtn.textContent = btnText;
  cBtn.onclick = btnFn;
  card.style.display='block';
  cv.style.visibility='hidden'; hud.style.visibility='hidden';
}
function hideCard(){
  card.style.display='none';
  cv.style.visibility='visible'; hud.style.visibility='visible';
}

function renderPills(){
  let h='';
  STAGES.forEach(function(s,i){
    const st = i<stageIdx ? 'done' : (i===stageIdx ? 'now' : '');
    h += '<div class="mgPill '+st+'">'+s.icon+' '+s.name+(i<stageIdx?' ✔':'')+'</div>';
  });
  pills.innerHTML=h;
}

function startStage(){
  renderPills();
  const s = STAGES[stageIdx];
  const f = fails[s.id]||0;
  setTimeout(function(){ try{ SUR.next(); }catch(e){} }, 900);
  showCard(
    'STAGE ' + (stageIdx+1) + ' / ' + STAGES.length,
    s.icon + '  ' + s.name,
    s.rule + '\n\nControls: ' + s.ctrl + (f? '\n\nRetry #'+f+' - this run is easier.' : ''),
    'START', runStage, 'intro');
  Snd.ding(520,undefined,.8); Snd.ding(780,Snd.t+.12,.8);
}

function runStage(){
  const s = STAGES[stageIdx];
  document.body.classList.remove('sur-flip','sur-disco');
  try{ GRAV_MUL = 1; }catch(e){}
  hideCard(); fit();
  const env = {
    mercy: fails[s.id]||0,
    hud: function(txt2){ hud.textContent = txt2; },
    win: function(){ if(!running) return; stopLoop(); stageWin(); },
    lose:function(){ if(!running) return; stopLoop(); stageLose(); }
  };
  game = s.make(env);
  running = true; lastT = performance.now();
  raf = requestAnimationFrame(loop);
  Snd.ding(880,undefined,.9);
}

function stageWin(){
  const s = STAGES[stageIdx];
  Snd.fanfare(); cannons(); rainConfetti(90); shake(); flashScreen(.6);
  burst(innerWidth/2, innerHeight*.5, 90, {speed:16,g:.2,coin:.3});
  stageIdx++;
  renderPills();
  if(stageIdx >= STAGES.length){
    showCard('GAUNTLET CLEARED', '🏆  YOU GOT THEM BACK',
      'All five games beaten. Two spins have been returned to the wheel.',
      'CLAIM +2 SPINS', finish, 'win');
    Snd.jackpot(); fireworks(6);
  } else {
    setTimeout(function(){ try{ SUR.next(); }catch(e){} }, 1400);
    showCard('STAGE CLEARED', '✔  ' + s.name,
      (STAGES.length-stageIdx) + ' to go. Keep it together, Blue.',
      'NEXT STAGE', startStage, 'win');
  }
}

function stageLose(){
  const s = STAGES[stageIdx];
  fails[s.id] = (fails[s.id]||0) + 1;
  Snd.buzzer(); setTimeout(function(){ Snd.sadTrombone(); }, 320);
  shake(); flashScreen(.7,'#ff0033');
  showCard('STAGE FAILED', '💀  ' + s.name,
    'No penalty - you can retry as many times as you want, and every retry is easier than the last.',
    'TRY AGAIN', runStage, 'lose');
}

function finish(){
  activeFlag=false;
  ov.classList.remove('on');
  document.body.classList.remove('mg-open');
  stopLoop();
  if(typeof gauntletCleared === 'function') gauntletCleared();
}

function open(){
  activeFlag=true;
  /* make sure no surprise effect is left hanging over the games */
  document.body.classList.remove('sur-flip','sur-disco');
  try{ GRAV_MUL = 1; document.getElementById('surLayer').innerHTML=''; }catch(e){}
  stageIdx=0; fails={};
  ov.classList.add('on');
  document.body.classList.add('mg-open');
  fit();
  showCard('THE COMEBACK GAUNTLET', '5 GAMES · 2 SPINS ON THE LINE',
    'You lost everything on the wheel. This is the only way back.\n' +
    'Beat all five games and you win 2 spins - and those spins are guaranteed real prizes.\n' +
    'Unlimited retries. Every retry gets easier. You cannot get stuck.',
    'LET US GO', startStage, 'intro');
  Snd.riser(2.2);
}

return {
  open:open,
  active:function(){ return activeFlag; },
  inGame:function(){ return running; },
  abort:function(){
    stopLoop(); activeFlag=false;
    ov.classList.remove('on');
    document.body.classList.remove('mg-open');
  },
  /* operator escape hatches */
  goto:function(i){ stopLoop(); stageIdx=Math.max(0,Math.min(STAGES.length-1,i)); startStage(); },
  skip:function(){ if(!activeFlag) return; stopLoop(); stageWin(); }
};
})();

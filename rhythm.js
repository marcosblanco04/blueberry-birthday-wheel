function gameRhythm(env){
  const m = env.mercy;
  const KEYS = ['d','f','j','k'];
  const COLS = ['#FF3FD0','#FFD447','#22E7FF','#9DFF3C'];
  const TRAVEL = 1.9, HITLINE = LH-96;
  const WIN_MS = 0.155 + m*0.035;
  const needPct = Math.max(.52, .75 - m*.06);

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
    [1,0,0,1, 0,1,0,0, 1,0,0,1, 0,1,0,0],
    [1,0,1,0, 0,1,0,1, 1,0,1,0, 0,1,0,0],
    [1,0,1,1, 0,1,0,1, 1,0,1,0, 1,1,0,1],
    [1,1,0,1, 1,0,1,1, 1,0,1,1, 0,1,1,1]
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
      t = (Snd.ctx && !Snd.muted) ? (Snd.ctx.currentTime - A0) : (t + dt);
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

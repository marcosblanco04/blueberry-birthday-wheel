p = 'template.html'
s = open(p, encoding='utf-8').read()
o = s

# ---------- yippee voice synth ----------
s = s.replace(
"""  seaLionSong(){""",
"""  /* a little crowd of squeaky voices going YIP-PEE! */
  yip(when,pitch,pan){
    if(this.muted||!this.ctx)return;
    const t=when||this.t, f=(pitch||1)*430;
    const o=this.ctx.createOscillator(); o.type='sawtooth';
    o.frequency.setValueAtTime(f*.72,t);
    o.frequency.exponentialRampToValueAtTime(f*1.18,t+.13);
    o.frequency.setValueAtTime(f*1.05,t+.30);
    o.frequency.exponentialRampToValueAtTime(f*1.34,t+.46);
    o.frequency.exponentialRampToValueAtTime(f*1.14,t+.62);
    const vib=this.ctx.createOscillator(); vib.type='sine'; vib.frequency.value=6.5;
    const vg=this.ctx.createGain(); vg.gain.value=f*.02; vib.connect(vg); vg.connect(o.frequency);
    vib.start(t); vib.stop(t+.7);
    const out=this.gain(0);
    [[330,9,1],[2350,13,.85],[3100,10,.4]].forEach(function(q){
      const bp=Snd.ctx.createBiquadFilter(); bp.type='bandpass';
      bp.frequency.value=q[0]; bp.Q.value=q[1];
      const g=Snd.gain(q[2],out); o.connect(bp); bp.connect(g);
    });
    /* YI ... p ... PEEE */
    out.gain.setValueAtTime(.0001,t);
    out.gain.linearRampToValueAtTime(.30,t+.03);
    out.gain.setValueAtTime(.26,t+.20);
    out.gain.exponentialRampToValueAtTime(.004,t+.26);
    out.gain.linearRampToValueAtTime(.34,t+.33);
    out.gain.setValueAtTime(.30,t+.55);
    out.gain.exponentialRampToValueAtTime(.0001,t+.72);
    o.start(t); o.stop(t+.75);
    this.noise(.04,2600,3,.07,'bandpass',t+.275);      /* the "p" */
  },
  yippee(){
    if(this.muted||!this.ctx)return;
    const t=this.t;
    [[0,1.0],[.03,1.14],[.06,.9],[.09,1.28],[.02,1.05]].forEach(function(v){
      Snd.yip(t+v[0], v[1]);
    });
    /* second, higher round */
    [[.85,1.06],[.88,1.2],[.91,.95],[.94,1.35]].forEach(function(v){
      Snd.yip(t+v[0], v[1]);
    });
    this.coins(10,t+.4);
  },
  seaLionSong(){""")

# ---------- yippee gif on the final win ----------
s = s.replace(
"""    <div id="seaLionBox"><img id="seaLionGif" alt="sea lion"><div id="orkText">ORK ORK ORK!</div></div>""",
"""    <div id="seaLionBox"><img id="seaLionGif" alt="sea lion"><div id="orkText">ORK ORK ORK!</div></div>
      <div id="yippeeBox"><img id="yippeeGif" alt="yippee"><div id="yipText">YIPPEE!!</div></div>""")

s = s.replace(
"""#seaLionBox{display:none;flex:0 0 auto}""",
"""#seaLionBox,#yippeeBox{display:none;flex:0 0 auto}
#yippeeBox img{height:clamp(150px,24vh,260px);border-radius:18px;
  box-shadow:0 0 50px rgba(255,212,71,.9);animation:wob .4s ease-in-out infinite}
#yipText{font-family:'Bungee',cursive;font-size:clamp(16px,2.6vw,36px);color:var(--gold);
  text-shadow:0 0 26px rgba(255,212,71,.95);animation:pop .3s ease-in-out infinite;margin-top:6px}""")

s = s.replace(
"""  const box=document.getElementById('seaLionBox');
  box.style.display = isSeaLion?'block':'none';""",
"""  const box=document.getElementById('seaLionBox');
  box.style.display = isSeaLion?'block':'none';
  const ybox=document.getElementById('yippeeBox');
  ybox.style.display = isFinal?'block':'none';
  if(isFinal){
    document.getElementById('yippeeGif').src = A.yippeegif||'';
    Snd.yippee();
    setTimeout(function(){Snd.yippee();},1700);
    setTimeout(function(){Snd.yippee();},3400);
    setTimeout(function(){Snd.yippee();},5200);
  }""")

# make the SUPER prize card read as the biggest moment
s = s.replace(
"    ? 'THE BIG ONE - THE DREAM ITEM - IT IS YOURS'",
"    ? 'SUPER PRIZE - THE BIGGEST DREAM ITEM ON THE WHOLE LIST'")

assert s != o, 'nothing changed'
open(p, 'w', encoding='utf-8').write(s)
print('patched ok')

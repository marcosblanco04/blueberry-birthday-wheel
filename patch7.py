p = 'template.html'
s = open(p, encoding='utf-8').read()
o = s

# real sea-lion laugh sample, played through the same master bus as the synth
s = s.replace(
"""  seaLionSong(){
    if(this.muted||!this.ctx)return;
    const t=this.t;
    [0,.26,.5,.86,1.1,1.32,1.72,1.96,2.2,2.62,2.9].forEach(function(dt,i){
      Snd.bark(t+dt, .88+Math.random()*.34 + (i%3===0?.1:0));
    });
    this.noise(1.4,2600,.6,.08,'highpass',t+.1);
  }""",
"""  _slBuf:null, _slLoading:false,
  loadSample(){
    if(this._slBuf||this._slLoading||!this.ctx||!A.sealionsnd) return;
    this._slLoading=true;
    const bin=atob(A.sealionsnd.split(',')[1]);
    const arr=new Uint8Array(bin.length);
    for(let i=0;i<bin.length;i++) arr[i]=bin.charCodeAt(i);
    this.ctx.decodeAudioData(arr.buffer, function(b){ Snd._slBuf=b; }, function(){});
  },
  seaLionLaugh(when,vol){
    if(this.muted||!this.ctx||!this._slBuf) return false;
    const t=when||this.t;
    const src=this.ctx.createBufferSource(); src.buffer=this._slBuf;
    const g=this.gain(vol===undefined?1.15:vol);
    src.connect(g); src.start(t);
    return true;
  },
  seaLionSong(){
    if(this.muted||!this.ctx)return;
    const t=this.t;
    if(this.seaLionLaugh(t)) return;          /* real sample when it is ready */
    [0,.26,.5,.86,1.1,1.32,1.72,1.96,2.2,2.62,2.9].forEach(function(dt,i){
      Snd.bark(t+dt, .88+Math.random()*.34 + (i%3===0?.1:0));
    });
    this.noise(1.4,2600,.6,.08,'highpass',t+.1);
  }""")

# decode the sample as soon as audio is unlocked
s = s.replace("  Snd.init(); Snd.ctx.resume();\n  startEl.classList.add('gone');",
              "  Snd.init(); Snd.ctx.resume(); Snd.loadSample();\n  startEl.classList.add('gone');")

# sea lion win: play the laugh a few times over the gif
s = s.replace(
"""    Snd.seaLionSong();
    setTimeout(function(){Snd.seaLionSong();}, 3300);
    setTimeout(function(){Snd.seaLionSong();}, 6600);""",
"""    Snd.seaLionSong();
    setTimeout(function(){Snd.seaLionSong();}, 3600);
    setTimeout(function(){Snd.seaLionSong();}, 7200);""")

assert s != o, 'nothing changed'
open(p, 'w', encoding='utf-8').write(s)
print('patched ok')

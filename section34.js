/* ============================================================
   3. WHEEL RENDERING  (drawn once into a sprite, only rotated per frame)
   ============================================================ */
const wheelC = document.getElementById('wheel'), wctx = wheelC.getContext('2d');
const bulbC  = document.getElementById('bulbs'),  bctx = bulbC.getContext('2d');
const imgs = {};
ITEMS.forEach(function(it){
  if(!A[it.k]) return;
  const im=new Image();
  im.onload=function(){ buildWheelSprite(); };
  im.src=A[it.k]; imgs[it.k]=im;
});

const PAL = [
  ['#8B3DFF','#4B12A8'], ['#FF3FD0','#A80D7C'], ['#22E7FF','#0785A8'],
  ['#FFD447','#C98A00'], ['#9DFF3C','#4E9500'], ['#FF7A3D','#B33800'],
];
let R=0; const DPR=Math.min(window.devicePixelRatio||1,2);
const sprite=document.createElement('canvas'), sctx=sprite.getContext('2d');

function sizeCanvases(){
  const wrap=document.getElementById('wheelWrap');
  const s=Math.max(200, wrap.clientWidth);
  wheelC.width=s*DPR; wheelC.height=s*DPR; wheelC.style.width=s+'px'; wheelC.style.height=s+'px';
  const bs=Math.round(s*1.07);
  bulbC.width=bs*DPR; bulbC.height=bs*DPR; bulbC.style.width=bs+'px'; bulbC.style.height=bs+'px';
  R=s/2;
  const p=document.getElementById('pointer');
  p.setAttribute('width', Math.max(56,s*.115)); p.setAttribute('height', Math.max(72,s*.15));
  buildWheelSprite();
}
window.addEventListener('resize', sizeCanvases);

function buildWheelSprite(){
  if(!R) return;
  sprite.width=Math.round(R*2*DPR); sprite.height=Math.round(R*2*DPR);
  const ctx=sctx; ctx.setTransform(DPR,0,0,DPR,0,0);
  ctx.clearRect(0,0,R*2,R*2);
  ctx.save(); ctx.translate(R,R);

  for(let i=0;i<N;i++){
    const it=ITEMS[i], a0=i*SEG-Math.PI/2-SEG/2, a1=a0+SEG;
    const grad=ctx.createRadialGradient(0,0,R*.12,0,0,R);
    if(it.fail){ grad.addColorStop(0,'#2b0008'); grad.addColorStop(.6,'#7a001c'); grad.addColorStop(1,'#12000a'); }
    else { const c=PAL[i%PAL.length];
      if(it.win){ grad.addColorStop(0,'#ffffff'); grad.addColorStop(.14,c[0]); grad.addColorStop(1,c[1]); }
      else { grad.addColorStop(0,c[0]); grad.addColorStop(1,c[1]); } }
    ctx.beginPath(); ctx.moveTo(0,0); ctx.arc(0,0,R-6,a0,a1); ctx.closePath();
    ctx.fillStyle=grad; ctx.fill();

    ctx.save(); ctx.clip();
    const sh=ctx.createLinearGradient(0,-R,0,R);
    sh.addColorStop(0,'rgba(255,255,255,.20)'); sh.addColorStop(.5,'rgba(255,255,255,0)');
    sh.addColorStop(1,'rgba(0,0,0,.28)');
    ctx.fillStyle=sh; ctx.fillRect(-R,-R,R*2,R*2);
    ctx.restore();

    ctx.beginPath(); ctx.moveTo(0,0);
    ctx.lineTo(Math.cos(a0)*(R-6),Math.sin(a0)*(R-6));
    ctx.strokeStyle='rgba(255,212,71,.6)'; ctx.lineWidth=Math.max(1,R*.007); ctx.stroke();

    const mid=a0+SEG/2;
    ctx.save(); ctx.rotate(mid);
    const im=imgs[it.k], isz=R*.15, ix=R*.795;
    if(im && im.complete && im.naturalWidth){
      ctx.save();
      ctx.beginPath(); ctx.arc(ix,0,isz*.62,0,7);
      ctx.fillStyle='rgba(255,255,255,.95)'; ctx.fill();
      ctx.strokeStyle='rgba(255,255,255,.8)'; ctx.lineWidth=Math.max(1,R*.004); ctx.stroke();
      ctx.clip();
      const ar=im.naturalWidth/im.naturalHeight;
      const w=isz*1.18*(ar>1?1:ar), h=w/ar;
      ctx.translate(ix,0); ctx.rotate(Math.PI/2);
      ctx.drawImage(im,-w/2,-h/2,w,h);
      ctx.restore();
    } else if(it.fail){
      ctx.save(); ctx.translate(ix,0); ctx.rotate(Math.PI/2);
      ctx.font=(R*.15)+'px serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
      ctx.fillText('💀',0,0); ctx.restore();
    }

    const lines=it.s.split('\n');
    ctx.textAlign='right'; ctx.textBaseline='middle';
    const fs=R*(lines.length>1?.042:.05);
    ctx.font='900 '+fs+'px Outfit, system-ui, sans-serif';
    ctx.lineWidth=fs*.36; ctx.lineJoin='round';
    ctx.strokeStyle='rgba(0,0,0,.62)';
    ctx.fillStyle= it.fail?'#ffd2da' : '#ffffff';
    const lx=R*.63;
    lines.forEach(function(ln,li){
      const y=(li-(lines.length-1)/2)*fs*1.02;
      ctx.strokeText(ln,lx,y); ctx.fillText(ln,lx,y);
    });
    ctx.restore();
  }

  ctx.beginPath(); ctx.arc(0,0,R-6,0,7);
  ctx.lineWidth=R*.028; ctx.strokeStyle='rgba(255,212,71,.9)'; ctx.stroke();
  ctx.beginPath(); ctx.arc(0,0,R*.13,0,7);
  ctx.fillStyle='#1a0533'; ctx.fill();
  ctx.restore();
}

function drawWheel(rotation){
  if(!R || !sprite.width) return;
  const ctx=wctx; ctx.setTransform(DPR,0,0,DPR,0,0);
  ctx.clearRect(0,0,R*2,R*2);
  ctx.save(); ctx.translate(R,R); ctx.rotate(rotation);
  ctx.drawImage(sprite,-R,-R,R*2,R*2);
  ctx.restore();
}

/* rim bulbs: plain circles under 'lighter', no per-frame gradients, 30fps */
let bulbPhase=0, winMode=false, bulbAcc=0;
function drawBulbs(dt){
  bulbPhase += dt*(winMode?7.5:2.2);
  bulbAcc += dt; if(bulbAcc < 1/30) return; bulbAcc = 0;
  const ctx=bctx, s=bulbC.width/DPR, c=s/2, rr=c-6;
  ctx.setTransform(DPR,0,0,DPR,0,0); ctx.clearRect(0,0,s,s);
  ctx.globalCompositeOperation='lighter';
  const COUNT=48, rad=s*.0115;
  for(let i=0;i<COUNT;i++){
    const a=(i/COUNT)*Math.PI*2 - Math.PI/2;
    const x=c+Math.cos(a)*rr, y=c+Math.sin(a)*rr;
    const on = winMode ? (Math.sin(bulbPhase + i*.9)>0) : (((i+Math.floor(bulbPhase))%3)===0);
    if(on){
      const hue = winMode ? ((i*24+bulbPhase*90)%360) : ((i*15+bulbPhase*18)%360);
      ctx.fillStyle='hsla('+hue+',100%,60%,.16)';
      ctx.beginPath(); ctx.arc(x,y,rad*3.4,0,7); ctx.fill();
      ctx.fillStyle='hsla('+hue+',100%,66%,.30)';
      ctx.beginPath(); ctx.arc(x,y,rad*1.9,0,7); ctx.fill();
      ctx.fillStyle='hsla('+hue+',100%,92%,1)';
      ctx.beginPath(); ctx.arc(x,y,rad*.85,0,7); ctx.fill();
    } else {
      ctx.fillStyle='rgba(255,255,255,.16)';
      ctx.beginPath(); ctx.arc(x,y,rad*.75,0,7); ctx.fill();
    }
  }
  ctx.globalCompositeOperation='source-over';
}

/* ============================================================
   4. PARTICLE FX  (sprite-based, budgeted, self-throttling)
   ============================================================ */
const fx=document.getElementById('fx'), fctx=fx.getContext('2d');
const rays=document.getElementById('rays'), rctx=rays.getContext('2d');
let P=[];
function fxSize(){ [fx,rays].forEach(function(c){ c.width=innerWidth*DPR;c.height=innerHeight*DPR;
  c.style.width=innerWidth+'px';c.style.height=innerHeight+'px'; }); }
fxSize(); addEventListener('resize',fxSize);

const EMOJI=['💜','🫐','✨','💖','🎉','⭐','💎','🎂'];
const EMOJI_SPR = EMOJI.map(function(ch){
  const c=document.createElement('canvas'); c.width=c.height=44;
  const x=c.getContext('2d'); x.font='34px serif'; x.textAlign='center'; x.textBaseline='middle';
  x.fillText(ch,22,23); return c;
});
const COIN_SPR = (function(){
  const S=40, c=document.createElement('canvas'); c.width=c.height=S;
  const x=c.getContext('2d');
  const g=x.createRadialGradient(S*.36,S*.32,1,S/2,S/2,S/2);
  g.addColorStop(0,'#fff6c2'); g.addColorStop(.55,'#FFD447'); g.addColorStop(1,'#a86400');
  x.fillStyle=g; x.beginPath(); x.arc(S/2,S/2,S/2-1,0,7); x.fill();
  x.strokeStyle='rgba(255,255,255,.7)'; x.lineWidth=2;
  x.beginPath(); x.arc(S/2,S/2,S*.32,0,7); x.stroke();
  return c;
})();

/* quality budget - shrinks itself if the machine can't keep up */
let fpsAvg=60;
const CAP=1000;
function qual(){ return Math.max(.3, Math.min(1, (fpsAvg-24)/34)); }
function trim(){ if(P.length>CAP) P.splice(0, P.length-CAP); }

function burst(x,y,n,opt){
  opt=opt||{}; n=Math.round(n*qual());
  const emoP=(opt.emoji===undefined?.14:opt.emoji), coinP=(opt.coin||0);
  for(let i=0;i<n;i++){
    const a=(opt.dir!==undefined) ? opt.dir+(Math.random()-.5)*(opt.spread||1.2)
                                  : Math.random()*Math.PI*2;
    const sp=(opt.speed||9)*(.35+Math.random());
    const r=Math.random();
    const kind = r<emoP ? 'e' : (r<emoP+coinP ? 'c' : (r<emoP+coinP+.34 ? 'r' : (r<emoP+coinP+.62?'s':'b')));
    P.push({
      x:x,y:y, vx:Math.cos(a)*sp, vy:Math.sin(a)*sp-(opt.lift||0),
      g:opt.g||.26, w:6+Math.random()*10, h:5+Math.random()*12,
      rot:Math.random()*7, vr:(Math.random()-.5)*.5,
      life:1, decay:.0042+Math.random()*.006,
      col:'hsl('+(opt.hue!==undefined?opt.hue+Math.random()*40:Math.random()*360)+',100%,66%)',
      kind:kind, ei:(Math.random()*EMOJI_SPR.length)|0,
      drag:.988, sw:Math.random()*7
    });
  }
  trim();
}
function rainConfetti(n,hue){
  n=Math.round(n*qual());
  for(let i=0;i<n;i++) P.push({
    x:Math.random()*innerWidth, y:-30-Math.random()*innerHeight*.5,
    vx:(Math.random()-.5)*2.2, vy:1.5+Math.random()*3.5, g:.055,
    w:6+Math.random()*9,h:5+Math.random()*13, rot:Math.random()*7, vr:(Math.random()-.5)*.35,
    life:1, decay:.0026,
    col:'hsl('+(hue!==undefined?hue+Math.random()*50:Math.random()*360)+',100%,66%)',
    kind:Math.random()<.16?'e':(Math.random()<.5?'r':'b'), ei:(Math.random()*EMOJI_SPR.length)|0,
    drag:.995, sw:Math.random()*7
  });
  trim();
}
function fireworks(count){
  for(let i=0;i<count;i++) setTimeout(function(){
    const x=innerWidth*(.12+Math.random()*.76), y=innerHeight*(.1+Math.random()*.42);
    burst(x,y,46,{speed:13,g:.14,hue:Math.random()*360,emoji:.04});
    flashScreen(.18); Snd.ding(500+Math.random()*900,undefined,.7);
    Snd.noise(.5,220,.8,.13,'lowpass');
  }, i*(280+Math.random()*340));
}
function cannons(){
  burst(0, innerHeight, 80, {dir:-Math.PI/2.85, spread:.85, speed:26, g:.3, lift:6});
  burst(innerWidth, innerHeight, 80, {dir:-Math.PI/1.55, spread:.85, speed:26, g:.3, lift:6});
  Snd.noise(.35,180,.7,.3,'lowpass'); Snd.tone(60,.4,.33,'sine',undefined,25);
}
function drawP(dt){
  fctx.setTransform(DPR,0,0,DPR,0,0); fctx.clearRect(0,0,innerWidth,innerHeight);
  const k=dt*60;
  for(let i=P.length-1;i>=0;i--){
    const p=P[i];
    p.vy+=p.g; p.vx*=p.drag; p.vy*=p.drag; p.sw+=.12;
    p.x+=p.vx+Math.sin(p.sw)*.7; p.y+=p.vy; p.rot+=p.vr; p.life-=p.decay*k;
    if(p.life<=0||p.y>innerHeight+90||p.x<-160||p.x>innerWidth+160){ P.splice(i,1); continue; }
    fctx.save();
    fctx.globalAlpha=p.life>.6?1:p.life*1.6;
    fctx.translate(p.x,p.y); fctx.rotate(p.rot);
    if(p.kind==='e'){ const sz=p.w*2.4; fctx.drawImage(EMOJI_SPR[p.ei],-sz/2,-sz/2,sz,sz); }
    else if(p.kind==='c'){ const sz=p.w*2, hh=sz*Math.abs(Math.cos(p.rot))+2;
      fctx.drawImage(COIN_SPR,-sz/2,-hh/2,sz,hh); }
    else if(p.kind==='s'){
      fctx.fillStyle=p.col; fctx.beginPath();
      for(let q=0;q<10;q++){ const rr=q%2?p.w*.42:p.w, a=q*Math.PI/5;
        if(q) fctx.lineTo(Math.cos(a)*rr,Math.sin(a)*rr); else fctx.moveTo(Math.cos(a)*rr,Math.sin(a)*rr); }
      fctx.closePath(); fctx.fill();
    }
    else if(p.kind==='b'){ fctx.fillStyle=p.col;
      fctx.beginPath(); fctx.arc(0,0,p.w*.55,0,7); fctx.fill(); }
    else { fctx.fillStyle=p.col;
      fctx.fillRect(-p.w/2,-p.h/2,p.w,p.h*Math.abs(Math.cos(p.rot*1.7))); }
    fctx.restore();
  }
}
let rayAngle=0, rayAcc=0, raysCleared=true;
function drawRays(dt){
  if(!rays.classList.contains('on')){
    if(!raysCleared){ rctx.setTransform(1,0,0,1,0,0); rctx.clearRect(0,0,rays.width,rays.height); raysCleared=true; }
    return;
  }
  raysCleared=false;
  rayAngle+=dt*.55;
  rayAcc+=dt; if(rayAcc<1/30) return; rayAcc=0;
  rctx.setTransform(DPR,0,0,DPR,0,0); rctx.clearRect(0,0,innerWidth,innerHeight);
  const cx=innerWidth/2, cy=innerHeight*.45, len=Math.hypot(innerWidth,innerHeight);
  rctx.globalCompositeOperation='lighter';
  for(let i=0;i<16;i++){
    const a=rayAngle+i*(Math.PI*2/16), w=.06;
    const g=rctx.createLinearGradient(cx,cy,cx+Math.cos(a)*len,cy+Math.sin(a)*len);
    g.addColorStop(0,'hsla('+((i*26+rayAngle*60)%360)+',100%,70%,.30)');
    g.addColorStop(1,'hsla(0,0%,100%,0)');
    rctx.fillStyle=g; rctx.beginPath(); rctx.moveTo(cx,cy);
    rctx.arc(cx,cy,len,a-w,a+w); rctx.closePath(); rctx.fill();
  }
  rctx.globalCompositeOperation='source-over';
}
const flashEl=document.getElementById('flash');
function flashScreen(str,color){
  flashEl.style.background=color||'#fff';
  flashEl.style.opacity=0;
  flashEl.animate([{opacity:str||.85},{opacity:0}],{duration:430,easing:'ease-out'});
}
function shake(){ const s=document.getElementById('stage');
  s.classList.remove('shake'); void s.offsetWidth; s.classList.add('shake'); }


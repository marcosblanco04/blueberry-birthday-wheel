def sub(s, a, b, n=1):
    assert a in s, 'NOT FOUND: ' + a[:80].replace('\n', '\\n')
    return s.replace(a, b, n)

f = 'template.html'
s = open(f, encoding='utf-8').read()
o = s

# ---- the unused bonus slice becomes the sealed secret prize ----
s = sub(s, " {k:'EXTRA',    n:'SECRET EXTRA SPIN',                 s:'EXTRA\\nSPIN', extra:1},",
           " {k:'SECRET',   n:'SECRET PRIZE',                      s:'SECRET\\nPRIZE', secret:1},")

# gold slice, padlock instead of a product photo
s = sub(s, "    else if(it.extra){ grad.addColorStop(0,'#fffbe6'); grad.addColorStop(.35,'#FFD447'); grad.addColorStop(1,'#a35c00'); }",
           "    else if(it.secret){ grad.addColorStop(0,'#fffbe6'); grad.addColorStop(.35,'#FFD447'); grad.addColorStop(1,'#a35c00'); }")
s = sub(s, "    } else if(it.fail || it.extra){",
           "    } else if(it.fail || it.secret){")
s = sub(s, "      ctx.fillText(it.fail?'💀':'⭐',0,0); ctx.restore();",
           "      ctx.fillText(it.fail?'💀':'🔒',0,0); ctx.restore();")
s = sub(s, "    ctx.strokeStyle= it.extra?'rgba(255,255,255,.85)':'rgba(0,0,0,.62)';",
           "    ctx.strokeStyle= it.secret?'rgba(255,255,255,.85)':'rgba(0,0,0,.62)';")
s = sub(s, "    ctx.fillStyle= it.fail?'#ffd2da' : (it.extra?'#3a1f00':(owned?'#ff5b7a':'#ffffff'));",
           "    ctx.fillStyle= it.fail?'#ffd2da' : (it.secret?'#3a1f00':(owned?'#ff5b7a':'#ffffff'));")

# it can never be landed on, but be safe about it
s = sub(s, """  if(item.fail) doFail();
  else if(item.extra) doExtra();
  else doWin(item);""",
"""  if(item.fail || item.secret) doFail();
  else doWin(item);""")

# ---- the sealed card in the finale ----
s = sub(s, '    <div id="sumGrid"></div>',
"""    <div id="sumGrid"></div>
    <div id="sumSecret">
      <div class="lock">&#128274;</div>
      <div class="st">AND ONE MORE. A SECRET ONE.</div>
      <div class="sr">REVEALED ON THE 12TH</div>
      <div class="sh">Hint: it normally comes by the dozen &mdash; this is not a dozen.<br>
        You will smell it before you see it, and it will not last the week.<br>
        That is exactly the point.</div>
      <div class="sc" id="secretCountdown"></div>
    </div>""")

s = sub(s, "#sumFoot{margin-top:16px;",
"""#sumSecret{margin:18px auto 0;max-width:min(680px,92vw);padding:16px 20px;border-radius:22px;
  border:3px dashed rgba(255,212,71,.75);background:rgba(255,212,71,.08);
  box-shadow:0 0 40px rgba(255,212,71,.25) inset}
#sumSecret .lock{font-size:clamp(26px,4vw,44px);animation:pop 2.2s ease-in-out infinite}
#sumSecret .st{font-family:'Bungee',cursive;font-size:clamp(11px,1.5vw,18px);letter-spacing:2px;
  color:#FFD447;margin-top:4px}
#sumSecret .sr{font-family:'Bungee',cursive;font-size:clamp(16px,2.8vw,36px);line-height:1.05;margin-top:6px;
  background:linear-gradient(92deg,#FFD447,#fff,#FF3FD0,#FFD447);background-size:300% 100%;
  -webkit-background-clip:text;background-clip:text;color:transparent;animation:flow 3s linear infinite}
#sumSecret .sh{margin-top:10px;font-weight:700;font-size:clamp(10px,1.15vw,14px);line-height:1.65;
  color:rgba(255,255,255,.72);font-style:italic}
#sumSecret .sc{margin-top:10px;font-family:'Bungee',cursive;font-size:clamp(12px,1.8vw,22px);color:#22E7FF;
  letter-spacing:1px}
#sumFoot{margin-top:16px;""")

# ---- countdown to the next 12th ----
s = sub(s, "function giftConfirmed(){",
"""/* ticks down to midnight on the next 12th, wherever the show happens to run */
let secretTimer = null;
function startSecretCountdown(){
  const el = document.getElementById('secretCountdown');
  if(!el) return;
  function target(){
    const now = new Date();
    let t = new Date(now.getFullYear(), now.getMonth(), 12, 0, 0, 0);
    if(t <= now) t = new Date(now.getFullYear(), now.getMonth()+1, 12, 0, 0, 0);
    return t;
  }
  const when = target();
  function tick(){
    const ms = when - new Date();
    if(ms <= 0){ el.textContent = "IT IS THE 12TH \\ud83d\\udc9c"; return; }
    const d = Math.floor(ms/86400000);
    const h = Math.floor(ms/3600000) % 24;
    const m = Math.floor(ms/60000) % 60;
    const sec = Math.floor(ms/1000) % 60;
    el.textContent = (d>0 ? d + 'd ' : '') +
      String(h).padStart(2,'0') + ':' + String(m).padStart(2,'0') + ':' + String(sec).padStart(2,'0');
  }
  tick();
  if(secretTimer) clearInterval(secretTimer);
  secretTimer = setInterval(tick, 1000);
}

function giftConfirmed(){""")

s = sub(s, "  document.getElementById('sumGrid').innerHTML=g;",
           "  document.getElementById('sumGrid').innerHTML=g;\n  startSecretCountdown();")

assert s != o
open(f, 'w', encoding='utf-8').write(s)
print('template.html patched (secret prize)')

# admin shortcut
f = 'endgame.js'
s = open(f, encoding='utf-8').read()
o = s
s = sub(s, "    btn(r, 'Mute / unmute', function(){ Snd.muted = !Snd.muted; });",
"""    btn(r, 'Show secret prize card', function(){
      closePanel();
      document.getElementById('dim').classList.add('on');
      startSecretCountdown();
      document.getElementById('sumOv').classList.add('on');
    });
    btn(r, 'Mute / unmute', function(){ Snd.muted = !Snd.muted; });""")
assert s != o
open(f, 'w', encoding='utf-8').write(s)
print('endgame.js patched')

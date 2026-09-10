p = 'template.html'
s = open(p, encoding='utf-8').read()
o = s

old = "    const lines=it.s.split('\\n');"
new = "    const lines = owned ? ['ALREADY','WON'] : it.s.split('\\n');"
assert old in s, 'lines decl not found'
s = s.replace(old, new, 1)

old2 = "    ctx.fillStyle= it.fail?'#ffd2da' : (it.extra?'#3a1f00':(owned?'rgba(255,255,255,.45)':'#ffffff'));"
assert old2 in s, 'fillStyle not found'
s = s.replace(old2,
    "    ctx.fillStyle= it.fail?'#ffd2da' : (it.extra?'#3a1f00':(owned?'#ff5b7a':'#ffffff'));", 1)

old3 = """    if(owned){
      const fs2=R*.036;
      ctx.font='900 '+fs2+'px Outfit, system-ui, sans-serif';
      ctx.lineWidth=fs2*.5; ctx.strokeStyle='rgba(0,0,0,.85)';
      ctx.fillStyle='#ff5b7a';
      ctx.strokeText('ALREADY WON', R*.365, 0);
      ctx.fillText('ALREADY WON', R*.365, 0);
    }
"""
assert old3 in s, 'stamp block not found'
s = s.replace(old3, '', 1)

assert s != o
open(p, 'w', encoding='utf-8').write(s)
print('patched')

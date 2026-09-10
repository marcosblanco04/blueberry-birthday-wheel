import json, sys

tpl = open('template.html', encoding='utf-8').read()
mg = (open('minigames.js', encoding='utf-8').read()
      + '\n'
      + open('surprises.js', encoding='utf-8').read()
      + '\n'
      + open('endgame.js', encoding='utf-8').read())
assets = open('assets/assets.json', encoding='utf-8').read()

MARK = '\n/* GAUNTLET MODULE */\n'
if MARK in tpl:
    head, _, tail = tpl.partition(MARK)
    tail = tail.split('</script>', 1)[1]
    tpl = head + MARK + mg + '\n</script>' + tail
else:
    i = tpl.rindex('</script>')
    tpl = tpl[:i] + MARK + mg + '\n' + tpl[i:]
    open('template.html', 'w', encoding='utf-8').write(tpl)

out = tpl.replace('/*ASSETS*/{}', assets)
if out == tpl:
    print('ERROR: asset placeholder not found'); sys.exit(1)

open('Blueberry-Birthday-Wheel.html', 'w', encoding='utf-8').write(out)
open('public/index.html', 'w', encoding='utf-8').write(out)
print('built %.2f MB' % (len(out.encode('utf-8')) / 1048576))

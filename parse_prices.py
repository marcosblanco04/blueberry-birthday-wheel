import re, os, sys

D = 'pages'
target = '7d355302-b8a2-423b-896f-b2d9bd3c9b4c'   # cowboy hat, displayed goal SEK 218.29
h = open(os.path.join(D, target + '.html'), encoding='utf-8', errors='ignore').read()

# find every "key":number pair and show the ones whose value could be 218.29 / 21829
pairs = re.findall(r'\\?"([A-Za-z][A-Za-z0-9_]{2,30})\\?"\s*:\s*(-?[0-9]+\.?[0-9]*)', h)
seen = {}
for k, v in pairs:
    seen.setdefault(k, set()).add(v)

print('--- keys whose value looks like 218.29 or 21829 ---')
for k, vs in seen.items():
    for v in vs:
        f = float(v)
        if abs(f - 218.29) < 0.6 or abs(f - 21829) < 60:
            print(' ', k, '=', v)

print()
print('--- money-ish keys present ---')
for k in sorted(seen):
    if re.search(r'price|amount|goal|total|cost|ship|fund|target', k, re.I):
        print(' ', k, '=', sorted(seen[k])[:6])

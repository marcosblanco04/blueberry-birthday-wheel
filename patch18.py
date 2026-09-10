def sub(s, a, b):
    assert a in s, 'NOT FOUND: ' + a[:80].replace('\n', '\\n')
    return s.replace(a, b, 1)

f = 'template.html'
s = open(f, encoding='utf-8').read(); o = s

# The fake-out must never dangle something she cannot have. Only slices she
# has ALREADY won are allowed as decoys - then the near miss is a joke, not a
# heartbreak.
s = sub(s, """function pickDecoy(targetIdx){
  if(fakeOutForced === false) return null;
  const lastLoss  = (phase==='losses'   && spinsTaken === LOSS_SPINS-1);
  const lastPrize = (phase==='comeback' && spinsTaken+1 >= spinsAllowed);
  const secret    = !!(ITEMS[targetIdx] && ITEMS[targetIdx].secret);
  const force = (fakeOutForced === true) || lastLoss || lastPrize || secret;
  if(!force && Math.random() > FAKEOUT_CHANCE) return null;

  let pick = null;
  [2,3,4].forEach(function(k){
    const i = (targetIdx + k) % N, it = ITEMS[i];
    if(it.fail || it.secret || it.alreadyWon) return;
    if(!pick) pick = {idx:i, item:it};
    else if(BIG_LOOKING.indexOf(it.k) >= 0 && BIG_LOOKING.indexOf(pick.item.k) < 0) pick = {idx:i, item:it};
  });
  return pick;
}""",
"""function isOwned(it){
  return !!it && (it.alreadyWon || WON.indexOf(it.k) >= 0);
}
function pickDecoy(targetIdx){
  if(fakeOutForced === false) return null;
  const lastLoss  = (phase==='losses'   && spinsTaken === LOSS_SPINS-1);
  const lastPrize = (phase==='comeback' && spinsTaken+1 >= spinsAllowed);
  const secret    = !!(ITEMS[targetIdx] && ITEMS[targetIdx].secret);
  const force = (fakeOutForced === true) || lastLoss || lastPrize || secret;
  if(!force && Math.random() > FAKEOUT_CHANCE) return null;

  /* only slices she already owns - closest one that is at least 2 slices away */
  let pick = null, bestK = 99;
  for(let i=0;i<N;i++){
    const it = ITEMS[i];
    if(!isOwned(it) || i === targetIdx) continue;
    const k = ((i - targetIdx) % N + N) % N;
    if(k < 2) continue;
    if(k < bestK){ bestK = k; pick = {idx:i, item:it, k:k}; }
  }
  return pick;
}""")

# the creep back to the real result scales with how far the decoy sat
s = sub(s, """      runSpin(targetIdx, {dur:3200, holdAt:1, holdMs:0, turns:0, jitter:.3, pow:3.6},
              function(){ land(item); });""",
"""      const creep = Math.min(4200, 1700 + (decoy.k || 3)*230);
      runSpin(targetIdx, {dur:creep, holdAt:1, holdMs:0, turns:0, jitter:.3, pow:3.6},
              function(){ land(item); });""")

# the celebration should read as "you already have this one"
s = sub(s, """function fakeCelebrate(item, done){
  if(FF){ done(); return; }
  const box = document.getElementById('fakeWin');
  document.getElementById('fakeWinName').textContent = item.n;""",
"""function fakeCelebrate(item, done){
  if(FF){ done(); return; }
  const box = document.getElementById('fakeWin');
  document.getElementById('fakeWinName').textContent = item.n + '  (you already have this one)';""")

assert s != o
open(f, 'w', encoding='utf-8').write(s)
print('patched')

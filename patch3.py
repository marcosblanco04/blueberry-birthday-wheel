p = 'template.html'
s = open(p, encoding='utf-8').read()
o = s

# The card is transformed, so it forms a stacking context and a z-index:-1
# pseudo-element paints OVER its background. Use a real gradient border instead.
s = s.replace(
"""  border-radius:30px;transform:scale(.6) rotate(-7deg);transition:.6s cubic-bezier(.15,1.7,.4,1);
  background:linear-gradient(160deg,rgba(60,15,120,.96),rgba(20,4,50,.96));
  box-shadow:0 0 0 3px rgba(255,212,71,.9),0 0 90px rgba(255,63,208,.65),0 30px 90px rgba(0,0,0,.7)}""",
"""  border-radius:30px;transform:scale(.6) rotate(-7deg);transition:.6s cubic-bezier(.15,1.7,.4,1);
  border:5px solid transparent;
  background:linear-gradient(160deg,#2b0a5e,#12032e) padding-box,
             conic-gradient(from 0deg,#FFD447,#FF3FD0,#22E7FF,#8B3DFF,#9DFF3C,#FFD447) border-box;
  animation:cardGlow 1.6s ease-in-out infinite}
@keyframes cardGlow{
 0%,100%{box-shadow:0 0 60px rgba(255,63,208,.55),0 0 130px rgba(139,61,255,.35),0 30px 90px rgba(0,0,0,.75)}
 50%{box-shadow:0 0 110px rgba(255,212,71,.75),0 0 190px rgba(34,231,255,.4),0 30px 90px rgba(0,0,0,.75)}}""")

s = s.replace(
"""#winCard::before{content:'';position:absolute;inset:-5px;border-radius:35px;z-index:-1;
  background:conic-gradient(from 0deg,var(--gold),var(--pink),var(--cyan),var(--purple),var(--gold));
  animation:hueSpin 3.5s linear infinite;filter:blur(4px)}
@keyframes hueSpin{to{filter:blur(4px) hue-rotate(360deg)}}
""", "")

assert s != o, 'nothing changed'
open(p, 'w', encoding='utf-8').write(s)
print('patched ok')

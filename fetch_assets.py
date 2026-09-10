import json, io, os, urllib.request, base64
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)

ITEMS = [
 ("ps5",      "Blueberryvibezz PS5 Controller", "https://cdn.throne.com/wishlistItems/twitch:604435946/a2789ca8-9897-4139-8bd5-704be8366d0b?version=1788534251649"),
 ("bangle",   "Everything's Romantic Bangle Set", "https://cdn.shopify.com/s/files/1/0371/4842/6372/files/EVERYTHINGSROMANTICBANGLESTACK.jpg?v=1741502489"),
 ("sealion",  "Sea Lion Sound Plush Toy", "https://cdn.shopify.com/s/files/1/0675/8134/5891/files/32213.png?v=1784474261"),
 ("cowboy",   "Cowboy Hat (Brown)", "https://cdn.throne.com/wishlistItems/7d355302-b8a2-423b-896f-b2d9bd3c9b4c/914c19e3-2752-46d2-8148-47463438c03a.webp?version=1788469063871"),
 ("tender",   "Tender Hearted Bangle Set", "https://cdn.shopify.com/s/files/1/0371/4842/6372/files/tenderheartedgoldbangleset_47ec8760-4c52-4aab-b4e9-6d9ef4a13014.jpg?v=1777861267"),
 ("jersey",   "Silent Hill Is Broken Mesh Jersey", "https://img-va.myshopline.com/image/store/1724296904210/22--6.jpeg?w=1000&h=1000"),
 ("celsius48","48 x Celsius Peachy Vibe", "https://cdn.shopify.com/s/files/1/1063/7734/7410/files/PB-462799.webp?v=1781031314"),
 ("celsius24","24 x Celsius Peach Vibe", "https://cdn.throne.com/wishlistItems/twitch:604435946/22ca1988-d0c5-4f0b-86e6-9b3d6fa5803e?version=1788270203267"),
 ("enderman", "The Enderman Ushanka", "https://cdn.shopify.com/s/files/1/1297/1509/files/Enderman_Ushanka_Updated_Flatlay.png?v=1779941488"),
 ("axolotl",  "The Axolotl Ushanka", "https://cdn.shopify.com/s/files/1/1297/1509/files/AxolotleHat_8f8e480c-61a4-4725-ac4c-6cdd215b0e39.jpg?v=1763720671"),
 ("rabbit",   "Goth Rabbit Spa Headband", "https://cdn.shopify.com/s/files/1/0306/6745/files/goth-rabbit-spa-headband-2-pack-accessory-322.jpg?v=1762200221"),
 ("untildawn","Until Dawn", "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2172010/header.jpg?t=1750959555"),
 ("gow",      "God of War", "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1593500/header.jpg?t=1763059412"),
 ("dispatch", "Dispatch", "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2592160/fcfd39596c29e58f0d0c44ca56b8490d91fb3b76/capsule_616x353.jpg?t=1779899220"),
 ("horns",    "3D Printed Headset Horns", "https://i.etsystatic.com/24139329/r/il/cb34c8/3606581799/il_1080xN.3606581799_24no.jpg"),
 ("wig",      "Zero Two Cosplay Wig", "https://cdn.shopify.com/s/files/1/1789/1993/products/1_4230ad55-9350-42ed-9c46-3b6bcf0b558a.jpg?v=1616736761"),
 ("leon",     "Leon S. Kennedy Figure", "https://m.media-amazon.com/images/I/41w3epz7UYL._SY500_.jpg"),
 ("nurse",    "Silent Hill Bubble Head Nurse", "https://m.media-amazon.com/images/I/71XbeZGRuQL._SY500_.jpg"),
 ("pyramid",  "Red Pyramid Head Figure", "https://m.media-amazon.com/images/I/71sVbdd9wgL._SY500_.jpg"),
 ("monitor",  "ASUS ROG Swift OLED 27\"", "https://cdn.throne.com/wishlistItems/4bfafddc-ec09-4590-85d3-7318281e5f7b/4f2e45c9-a870-4345-a683-565aa3fc971d.webp?version=1775104922572"),
 ("neon",     "Govee RGBIC Neon Lights", "https://m.media-amazon.com/images/I/71LL4Sk9TFL._SY500_.jpg"),
 ("hexa",     "Govee Glide Hexa Panels", "https://m.media-amazon.com/images/I/61WCvyYZPcL._SY500_.jpg"),
]
GIF = "https://media1.tenor.com/m/q2vIYYobXZIAAAAd/sea-lion.gif"
BIG = {"bangle", "sealion", "jersey"}
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def thumb(raw, size):
    im = Image.open(io.BytesIO(raw))
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
    im.thumbnail((size, size), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=86, method=5)
    return buf.getvalue()

out = {}
for key, name, url in ITEMS:
    try:
        raw = get(url)
        small = thumb(raw, 700 if key in BIG else 200)
        out[key] = "data:image/webp;base64," + base64.b64encode(small).decode()
        print(f"OK   {key:10s} {len(small)//1024:5d} KB  {name}")
    except Exception as e:
        out[key] = ""
        print(f"FAIL {key:10s} {e}")

try:
    g = get(GIF)
    out["sealiongif"] = "data:image/gif;base64," + base64.b64encode(g).decode()
    print(f"OK   {'gif':10s} {len(g)//1024:5d} KB")
except Exception as e:
    out["sealiongif"] = ""
    print("FAIL gif", e)

with open(os.path.join(OUT, "assets.json"), "w", encoding="utf-8") as f:
    json.dump(out, f)
print("total payload MB:", round(sum(len(v) for v in out.values())/1048576, 2))

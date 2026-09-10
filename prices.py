import re, json, urllib.request, sys, time

ITEMS = [
 ("a2789ca8-9897-4139-8bd5-704be8366d0b", "PS5 Controller (custom)"),
 ("7d355302-b8a2-423b-896f-b2d9bd3c9b4c", "Cowboy Hat - Brown"),
 ("18327fe4-7666-4089-b83d-02996a601aeb", "Tender Hearted Bangle Set"),
 ("4e365b5a-0918-4174-b83a-ac0c7708262b", "48 x Celsius Peachy Vibe"),
 ("8716d1b1-08cf-4462-bf81-f1d5a1b53df6", "24 x Celsius Peach Vibe"),
 ("2e57e8af-a9a3-4466-a286-0ad24a00634a", "Enderman Ushanka"),
 ("c5a7deb4-56ee-4231-bf2e-9991c604ab10", "Axolotl Ushanka"),
 ("20bf1901-a99f-467a-bf4a-ef874132cefa", "Goth Rabbit Spa Headband 2-pack"),
 ("552babf4-f56e-45d2-9fb6-a47c9528beb5", "Until Dawn (Steam)"),
 ("993fc117-9d26-48f8-8d0a-30481af5c1f2", "God of War (Steam)"),
 ("86e34c64-16ea-4d2a-b1b8-15004a46c52f", "Dispatch (Steam)"),
 ("c3966aea-c58b-44ab-9d06-c77cbf720e1d", "3D Printed Headset Horns (Etsy)"),
 ("6c1ffb36-3808-48f5-abfe-f7f42c8afcb0", "Zero Two Cosplay Wig"),
 ("9beef462-819e-46cf-85c1-f59c31abb5ea", "Leon S. Kennedy Figure"),
 ("f54a7392-a271-4580-a59a-ae3a27c597ba", "Bubble Head Nurse Figure"),
 ("cff1f931-4822-489c-b56b-8838a0603900", "Red Pyramid Head Figure"),
 ("4bfafddc-ec09-4590-85d3-7318281e5f7b", 'ASUS ROG Swift 27" OLED'),
 ("7d2e828c-0bb2-49bb-8342-bf4e22c8c33e", "Govee RGBIC Neon Lights"),
 ("5c6ae205-dd1e-4a51-b71f-d8056bf05135", "Govee Glide Hexa Panels"),
]

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}

KEYS = ["price", "shippingPrice", "totalPrice", "goal", "goalAmount",
        "amountNeeded", "targetAmount", "fundedAmount", "currency"]

rows = []
for iid, name in ITEMS:
    url = "https://throne.com/blueberryvibezz/item/" + iid
    try:
        req = urllib.request.Request(url, headers=UA)
        h = urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "ignore")
    except Exception as e:
        print("FAIL", name, e)
        continue
    found = {}
    for k in KEYS:
        for m in re.finditer(r'\\?"' + k + r'\\?"\s*:\s*("?[A-Za-z0-9_.]+"?)', h):
            found.setdefault(k, []).append(m.group(1).strip('"'))
    rows.append((name, found))
    print(name, "->", {k: v[:4] for k, v in found.items()})
    time.sleep(0.3)

json.dump([[n, f] for n, f in rows], open("prices_raw.json", "w"), indent=1)
print("saved")

#!/usr/bin/env bash
set -u
OUT=/c/Users/melan/spin-wheel/pages
mkdir -p "$OUT"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

ids="
a2789ca8-9897-4139-8bd5-704be8366d0b
7d355302-b8a2-423b-896f-b2d9bd3c9b4c
18327fe4-7666-4089-b83d-02996a601aeb
4e365b5a-0918-4174-b83a-ac0c7708262b
8716d1b1-08cf-4462-bf81-f1d5a1b53df6
2e57e8af-a9a3-4466-a286-0ad24a00634a
c5a7deb4-56ee-4231-bf2e-9991c604ab10
20bf1901-a99f-467a-bf4a-ef874132cefa
552babf4-f56e-45d2-9fb6-a47c9528beb5
993fc117-9d26-48f8-8d0a-30481af5c1f2
86e34c64-16ea-4d2a-b1b8-15004a46c52f
c3966aea-c58b-44ab-9d06-c77cbf720e1d
6c1ffb36-3808-48f5-abfe-f7f42c8afcb0
9beef462-819e-46cf-85c1-f59c31abb5ea
f54a7392-a271-4580-a59a-ae3a27c597ba
cff1f931-4822-489c-b56b-8838a0603900
4bfafddc-ec09-4590-85d3-7318281e5f7b
7d2e828c-0bb2-49bb-8342-bf4e22c8c33e
5c6ae205-dd1e-4a51-b71f-d8056bf05135
"

for id in $ids; do
  f="$OUT/$id.html"
  if [ -s "$f" ]; then echo "cached $id"; continue; fi
  code=$(curl -sL --compressed -m 40 -o "$f" -w "%{http_code}" \
    -A "$UA" \
    -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
    -H "Accept-Language: en-US,en;q=0.9" \
    -H "Referer: https://throne.com/blueberryvibezz" \
    "https://throne.com/blueberryvibezz/item/$id")
  echo "$id -> $code ($(wc -c < "$f") bytes)"
  [ "$code" != "200" ] && rm -f "$f"
  sleep 2
done
echo done

import urllib.parse, subprocess, time, os

BASE = ("cute flat vector illustration, close-up front-facing portrait focusing on face and forehead, "
        "{bangs}, warm chocolate brown hair color, soft minimal facial features, gentle warm smile, "
        "warm cream skin tone, clean flat pastel illustration style, soft cel-shading, centered composition, "
        "plain soft pastel blush pink circular background, no text, no watermark, square image, "
        "modern beauty app character design")

PROMPTS = {
    "O": "center-parted curtain bangs with soft face-framing pieces, trendy balanced fringe",
    "R": "thin see-through wispy bangs with volume at the roots for height, narrow fringe width",
    "L": "blunt straight-across full bangs at eyebrow length, wide thick fringe cut straight",
    "S": "long side-swept curtain bangs framing the jawline, diamond-shaped silhouette",
    "H": "light asymmetric side-swept fringe, sparse wispy bangs gently covering one side of the forehead",
}
SEED_BASE = 800

os.makedirs("fringe_illustrations", exist_ok=True)
for i, (key, bangs) in enumerate(PROMPTS.items()):
    outpath = f"fringe_illustrations/{key}.jpg"
    if os.path.exists(outpath) and os.path.getsize(outpath) > 5000:
        print(key, "exists, skip")
        continue
    prompt = BASE.format(bangs=bangs)
    enc = urllib.parse.quote(prompt)
    seed = SEED_BASE + i
    url = f"https://image.pollinations.ai/prompt/{enc}?width=512&height=512&model=flux&nologo=true&seed={seed}"
    ok = False
    for attempt in range(6):
        subprocess.run(["curl", "-sL", "--max-time", "60", "-o", outpath, url])
        ftype = subprocess.run(["file", "-b", outpath], capture_output=True, text=True).stdout
        size = os.path.getsize(outpath) if os.path.exists(outpath) else 0
        if ("JPEG" in ftype or "PNG" in ftype) and size > 5000:
            ok = True
            print(key, "OK", size, "bytes, attempt", attempt+1)
            break
        print(key, "retry", attempt+1, ftype.strip()[:80])
        time.sleep(6)
    if not ok:
        print(key, "FAILED")
    time.sleep(2)

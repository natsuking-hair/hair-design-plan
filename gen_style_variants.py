import urllib.parse, subprocess, time, os

BASE_STYLE = ("cute flat vector illustration, front-facing bust portrait of a young Japanese woman, "
              "{hair}, warm chocolate brown hair color, soft minimal facial features, gentle warm smile, "
              "warm cream skin tone, clean flat pastel illustration style, soft cel-shading, centered composition, "
              "plain soft pastel blush pink circular background, no text, no watermark, square image, "
              "modern beauty app character design")

PROMPTS = {
    "S_teiban":   "chin-length straight blunt bob haircut, sharp clean sleek lines, short length",
    "S_konare":   "long sleek straight hair past the shoulders, glossy smooth low-maintenance length",
    "S_hanayaka": "medium length straight hair with ends flipped outward, face-framing playful flip",
    "W_teiban":   "medium length soft loose wavy hair, romantic volume, gentle waves",
    "W_konare":   "long tousled undone beach waves, effortless relaxed texture",
    "W_hanayaka": "long voluminous glamorous curled waves, bouncy body and shine",
    "N_teiban":   "medium length layered wolf-cut hairstyle, textured shag layers",
    "N_konare":   "short tousled mushroom mash-cut hairstyle, choppy textured wispy bangs",
    "N_hanayaka": "long shaggy layered mullet-wolf hairstyle, bold voluminous edgy texture",
}
SEED_BASE = 500

os.makedirs("style_illustrations", exist_ok=True)
for i, (key, hairDesc) in enumerate(PROMPTS.items()):
    outpath = f"style_illustrations/{key}.jpg"
    if os.path.exists(outpath) and os.path.getsize(outpath) > 5000:
        print(key, "exists, skip")
        continue
    prompt = BASE_STYLE.format(hair=hairDesc)
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

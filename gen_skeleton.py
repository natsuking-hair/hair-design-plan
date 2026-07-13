import urllib.parse, subprocess, time, os

PROMPTS = {
    "S": ("cute flat vector fashion illustration, front view of a young Japanese woman's upper body and shoulders, "
          "wearing a simple structured sleeveless top, straight boxy silhouette with elegant upper-body volume, "
          "defined straight shoulder line, subtle smooth collarbone, elegant upright posture, "
          "minimal fashion croquis style focusing on neckline collarbone and shoulder line, soft flat cel-shading, "
          "plain soft pastel blush pink circular background, no face close-up detail, no text, no watermark, square image"),
    "W": ("cute flat vector fashion illustration, front view of a young Japanese woman's upper body and shoulders, "
          "wearing a soft flowing draped top, curved soft delicate silhouette with narrow rounded shoulders, "
          "delicate visible collarbone, gentle relaxed soft posture, lower body volume feeling, "
          "minimal fashion croquis style focusing on neckline collarbone and shoulder line, soft flat cel-shading, "
          "plain soft pastel blush pink circular background, no face close-up detail, no text, no watermark, square image"),
    "N": ("cute flat vector fashion illustration, front view of a young Japanese woman's upper body and shoulders, "
          "wearing a relaxed oversized casual top, angular loose silhouette with broad frame shoulders, "
          "visible collarbone and joint structure, casual relaxed slouchy posture, sporty frame, "
          "minimal fashion croquis style focusing on neckline collarbone and shoulder line, soft flat cel-shading, "
          "plain soft pastel blush pink circular background, no face close-up detail, no text, no watermark, square image"),
}
SEED = {"S": 101, "W": 102, "N": 103}

os.makedirs("skeleton_illustrations", exist_ok=True)
for key, prompt in PROMPTS.items():
    outpath = f"skeleton_illustrations/{key}.jpg"
    enc = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{enc}?width=512&height=512&model=flux&nologo=true&seed={SEED[key]}"
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

#!/bin/bash
# Render every svg/*.svg to png/*.png at 2x with headless Chromium, then crop to the SVG's exact size.
# Headless Chromium's viewport is shorter than --window-size, so the window is made taller and the PNG is cropped.
cd "$(dirname "$0")"; mkdir -p png
CH=${CHROME:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}
for f in svg/*.svg; do
  w=$(grep -o 'width="[0-9]*"' "$f" | head -1 | grep -o '[0-9]*'); h=$(grep -o 'height="[0-9]*"' "$f" | head -1 | grep -o '[0-9]*')
  out="png/$(basename "${f%.svg}").png"
  "$CH" --headless --no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --window-size=$w,$((h + 200)) \
    --screenshot="$out" "file://$PWD/$f" >/dev/null 2>&1
  python3 -c "from PIL import Image; im=Image.open('$out'); im.crop((0,0,2*$w,2*$h)).save('$out')" && echo "$out"
done

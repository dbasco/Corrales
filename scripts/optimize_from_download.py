import sys, json, base64, io, pathlib
from PIL import Image, ImageOps
src, out_path, maxw, quality = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
d = json.loads(pathlib.Path(src).read_text())
raw = base64.b64decode(d["content"])
im = ImageOps.exif_transpose(Image.open(io.BytesIO(raw))).convert("RGB")
w,h = im.size
if w > maxw:
    im = im.resize((maxw, round(h*maxw/w)), Image.LANCZOS)
outp = pathlib.Path(out_path)
im.save(outp, "JPEG", quality=quality, optimize=True, progressive=True)
print(f"{outp.name}: {im.size[0]}x{im.size[1]}  {outp.stat().st_size/1024:.0f} KB  (orig {w}x{h}, {d['title']})")

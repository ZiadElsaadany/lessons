# -*- coding: utf-8 -*-
"""صورة الغلاف الجاهزة (المدرس + الأيقونات التلاتية الأبعاد حواليه، على خلفية بيضا) ← assets/teacher_hero.png + ضلّها.

    python3 tools/hero_photo.py <الصورة (PNG/JPG/WEBP بخلفية بيضا)>

- المدرس: بيتقص بموديل rembg (birefnet-general-lite) عشان الشعر الكيرلي يطلع ناعم.
- الأيقونات والشرطات: الموديلات بتعتبرها خلفية، فبتتاخد بالمسافة عن الأبيض: كل حاجة مش بيضا + سدّ الفراغات جوه
  الشكل (عشان الوشوش البيضا للروبوت والكارت ماتبقاش شفافة)، والأطراف بتتنعّم من درجة البُعد عن الأبيض.
- الدمج: الأيقونات بره منطقة المدرس بس، فحواف الشعر بتفضل من الموديل.
- تكبير ×1.5 (Lanczos) + حدة خفيفة عشان الطباعة، وfade تحت زي teacher_photo.py.
"""
import os, sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi

TOOLS = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(TOOLS), "assets")


def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    from rembg import remove, new_session
    src = Image.open(sys.argv[1]).convert("RGB")
    person = np.asarray(remove(src, session=new_session("birefnet-general-lite")))[..., 3].astype(np.float32) / 255
    rgb = np.asarray(src).astype(np.float32)
    d = 255 - rgb.min(-1)                                             # البُعد عن الأبيض
    solid = ndi.binary_fill_holes(ndi.binary_closing(d > 14, iterations=2))
    lab, n = ndi.label(solid)                                         # نشيل النقط الصغيرة (بقايا حواف الأبيض)
    sizes = ndi.sum(solid, lab, range(1, n + 1))
    solid = np.isin(lab, 1 + np.nonzero(sizes >= 400)[0])
    core = ndi.binary_erosion(solid, iterations=2)
    icons = np.where(core, 1.0, np.clip(d / 22, 0, 1) * ndi.binary_dilation(solid, iterations=1))
    near_person = ndi.binary_dilation(person > 0.5, iterations=8)
    alpha = np.maximum(person, icons * (~near_person))
    img = Image.fromarray(np.dstack([rgb, alpha * 255]).astype(np.uint8))
    img = img.crop(img.getbbox())
    img = img.resize((int(img.width * 1.5), int(img.height * 1.5)), Image.LANCZOS)
    r, g, b, a = img.split()
    rgb_img = Image.merge("RGB", (r, g, b)).filter(ImageFilter.UnsharpMask(radius=2, percent=45, threshold=2))
    a = np.asarray(a).astype(np.float32) / 255
    H = a.shape[0]
    a = a * np.clip((H - np.arange(H)) / (0.09 * H), 0, 1)[:, None] ** 1.4     # fade تحت
    out = Image.fromarray(np.dstack([np.asarray(rgb_img), (a * 255).astype(np.uint8)]))
    out.save(os.path.join(ASSETS, "teacher_hero.png"), optimize=True)
    # الضل (ربع الدقة + pad) لفصل الصورة عن الدايرة
    pad = 40
    sm = Image.fromarray((a * 255).astype(np.uint8)).resize((out.width // 4, out.height // 4), Image.LANCZOS)
    sh = Image.new("L", (sm.width + 2 * pad, sm.height + 2 * pad), 0); sh.paste(sm, (pad, pad))
    sh = sh.filter(ImageFilter.GaussianBlur(9))
    shadow = Image.new("RGBA", sh.size, (60, 30, 5, 0)); shadow.putalpha(sh.point(lambda v: int(v * 0.38)))
    shadow.save(os.path.join(ASSETS, "teacher_hero_shadow.png"), optimize=True)
    print("written teacher_hero.png", out.size, "shadow", shadow.size, "pad(full px)", pad * 4)


if __name__ == "__main__":
    main()

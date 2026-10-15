# -*- coding: utf-8 -*-
"""صورة المدرس للغلاف الخارجي: assets/teacher_cut.png + assets/teacher_shadow.png.

    python3 tools/teacher_photo.py <صورة مقصوصة PNG بخلفية شفافة>
    python3 tools/teacher_photo.py --src <الصورة الأصلية (HEIC/JPG)>     (يقص الخلفية بـ rembg الأول)

- الوش والشعر والنضارة والإيد ماتتلمسش: التعديلات كلها عامة (تباين/حدة خفيفة) أو على التيشيرت والحواف بس.
- الحواف: alpha بيتنضف (أطراف شفافة جدًا بتتشال + feather خفيف) عشان مايبقاش فيه هالة من الحيطة القديمة.
- التيشيرت: طبعة صغيرة <AI/> على الصدر (أبيض + برتقالي) متطبعة "جوه" القماش: بتاخد ضلّ وطيّات التيشيرت
  من إضاءة الصورة نفسها، ومايلة بزاوية الجسم، وأطرافها ناعمة زي حبر الطباعة.
- تحت: الصورة بتختفي تدريجي (fade) بدل القطع المستقيم عند الوسط.
- الضل: نسخة مطموسة من شكل الجسم (منفصلة، دقة قليلة) بتتحط ورا الصورة عشان تفصلها عن الدايرة البرتقالي.
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance

TOOLS = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(TOOLS)
ASSETS = os.path.join(BASE, "assets")
MONO = os.path.join(BASE, "fonts", "DejaVuSansMono-Bold.ttf")
AMBER = (249, 142, 3)

# مكان الطبعة على الصدر (إحداثيات الصورة المقصوصة 1612×2334؛ بتتظبط بالنسبة لو المقاس اتغيّر)
REF_W = 1612
PRINT_CENTER = (1168, 1105)
PRINT_WIDTH = 250
PRINT_ANGLE = -4          # درجات — ميلة الصدر في الصورة


def cut_from_source(src):
    import pillow_heif; pillow_heif.register_heif_opener()
    from rembg import remove, new_session
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    out = remove(im, session=new_session("isnet-general-use"), alpha_matting=True,
                 alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=15, alpha_matting_erode_size=8)
    return out.crop(out.getbbox())


def clean_alpha(a):
    """يشيل البقايا الشفافة جدًا، ويقفل الأطراف سنة، وfeather خفيف."""
    a = np.where(a < 0.08, 0, a)
    a = np.clip((a - 0.08) / 0.84, 0, 1)
    img = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.9))
    return np.asarray(img).astype(np.float32) / 255


def chest_print(rgb, alpha, scale):
    """<AI/> على الصدر: الحروف مضروبة في إضاءة القماش نفسه فبتاخد الطيّات والضل."""
    W = int(PRINT_WIDTH * scale)
    f = ImageFont.truetype(MONO, 200)
    parts = [("<", (255, 255, 255)), ("AI", AMBER), ("/>", (255, 255, 255))]
    tmp = Image.new("RGBA", (1400, 320), (0, 0, 0, 0)); d = ImageDraw.Draw(tmp); x = 10
    for t, c in parts:
        d.text((x, 40), t, font=f, fill=c + (255,)); x += d.textlength(t, font=f) - 6
    tmp = tmp.crop(tmp.getbbox())
    tmp = tmp.resize((W, int(tmp.height * W / tmp.width)), Image.LANCZOS).rotate(PRINT_ANGLE, resample=Image.BICUBIC, expand=True)
    tmp = tmp.filter(ImageFilter.GaussianBlur(0.6 * scale))          # حرف حبر مش حرف ديجيتال حاد
    p = np.asarray(tmp).astype(np.float32) / 255
    cx, cy = int(PRINT_CENTER[0] * scale), int(PRINT_CENTER[1] * scale)
    x0, y0 = cx - tmp.width // 2, cy - tmp.height // 2
    reg = rgb[y0:y0 + tmp.height, x0:x0 + tmp.width]
    lum = reg.mean(-1, keepdims=True)
    ref = np.median(lum)
    shade = np.clip(0.80 + (lum - ref) * 4.0, 0.6, 1.15)                # طيّات القماش
    ink = np.clip(p[..., :3] * shade * 0.94, 0, 1)                      # الحبر مش أبيض ناصع
    k = p[..., 3:4] * 0.95 * alpha[y0:y0 + tmp.height, x0:x0 + tmp.width, None]
    rgb[y0:y0 + tmp.height, x0:x0 + tmp.width] = reg * (1 - k) + ink * k


def main():
    args = sys.argv[1:]
    if not args: sys.exit(__doc__)
    im = cut_from_source(args[1]) if args[0] == "--src" else Image.open(args[0]).convert("RGBA")
    scale = im.width / REF_W
    # تحسين عام خفيف: تباين + حدة (من غير ما نغيّر ألوان البشرة)
    rgbim = ImageEnhance.Contrast(im.convert("RGB")).enhance(1.06)
    rgbim = rgbim.filter(ImageFilter.UnsharpMask(radius=2.2 * scale, percent=55, threshold=2))
    rgb = np.asarray(rgbim).astype(np.float32) / 255
    alpha = clean_alpha(np.asarray(im)[..., 3].astype(np.float32) / 255)
    chest_print(rgb, alpha, scale)
    H = alpha.shape[0]
    fade = np.clip((H - np.arange(H)) / (0.11 * H), 0, 1)[:, None] ** 1.4   # آخر 11% بيختفي تدريجي
    alpha = alpha * fade
    out = Image.fromarray((np.dstack([rgb, alpha]) * 255).astype(np.uint8))
    out.save(os.path.join(ASSETS, "teacher_cut.png"), optimize=True)
    # الضل: شكل الجسم مطموس، بلون بني غامق، بدقة الربع (هو مطموس أصلًا)
    sm = Image.fromarray((alpha * 255).astype(np.uint8)).resize((out.width // 4, out.height // 4), Image.LANCZOS)
    pad = 40
    sh = Image.new("L", (sm.width + 2 * pad, sm.height + 2 * pad), 0); sh.paste(sm, (pad, pad))
    sh = sh.filter(ImageFilter.GaussianBlur(9))
    shadow = Image.new("RGBA", sh.size, (60, 30, 5, 0)); shadow.putalpha(sh.point(lambda v: int(v * 0.42)))
    shadow.save(os.path.join(ASSETS, "teacher_shadow.png"), optimize=True)
    print("written teacher_cut.png", out.size, "+ teacher_shadow.png", shadow.size, "pad", pad * 4)


if __name__ == "__main__":
    main()

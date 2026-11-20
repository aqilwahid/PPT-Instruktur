"""Render an instructor deck from UTF-8 JSON. Requires python-pptx and Pillow."""
import argparse
import io
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Inches, Pt

ASSETS = Path(__file__).resolve().parent.parent / "assets"
W, H = 13 + 1 / 3, 7.5
WHITE, INK, NAVY, NIGHT = "FFFFFF", "1B2A4A", "132B49", "090A36"
BLUE, SKY, RED, MUTE = "105A96", "55C6F4", "C50731", "49576B"
PALE, EDGE, PALEBLUE = "F2F5F9", "D7DFEA", "DDEAF9"
FONT = "Aptos"


def color(value):
    return RGBColor.from_string(value)


def area(x, y, width, height):
    return tuple(Inches(v) for v in (x, y, width, height))


def shape(slide, x, y, w, h, fill, kind=MSO_SHAPE.RECTANGLE, stroke=None):
    obj = slide.shapes.add_shape(kind, *area(x, y, w, h))
    obj.fill.solid()
    obj.fill.fore_color.rgb = color(fill)
    if stroke:
        obj.line.color.rgb = color(stroke)
        obj.line.width = Pt(0.8)
    else:
        obj.line.fill.background()
    return obj


def measured_font(size, bold):
    names = ["Aptos-Bold.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"] if bold else ["Aptos.ttf", "arial.ttf", "DejaVuSans.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


def fits(text, width, height, size, bold):
    font = measured_font(size, bold)
    limit = width * 72 * 0.94
    lines = 0
    for paragraph in text.split("\n"):
        row = ""
        lines += 1
        for word in paragraph.split():
            if font.getlength(word) > limit:
                return False
            candidate = f"{row} {word}" if row else word
            if row and font.getlength(candidate) > limit:
                lines += 1
                row = word
            else:
                row = candidate
    return lines * size * 1.18 <= height * 72


def label(s, x, y, w, h, value, size=20, *, ink=INK, bold=False, italic=False,
          floor=None, align=PP_ALIGN.LEFT, center=False):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Teks kosong atau bukan string.")
    floor = size if floor is None else floor
    while size > floor and not fits(value, w, h, size, bold):
        size -= 1
    if not fits(value, w, h, size, bold):
        raise ValueError(f"Teks terlalu panjang untuk bidangnya. Ringkas atau pecah slide: {value[:80]}")
    obj = s.shapes.add_textbox(*area(x, y, w, h))
    obj.name = value.splitlines()[0][:85]
    tf = obj.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE if center else MSO_ANCHOR.TOP
    for i, line in enumerate(value.splitlines()):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(0)
        p.space_before = Pt(0)
        p.line_spacing = 1.04
        r = p.add_run()
        r.text = line
        r.font.name = FONT
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = color(ink)
    return obj


def panel_title(s, x, y, w, text, dark=False):
    return label(s, x, y, w, 0.68, text, 24, bold=True, floor=19, ink=WHITE if dark else INK)


def items(s, x, y, w, h, values, dark=False):
    if not isinstance(values, list) or not 1 <= len(values) <= 6:
        raise ValueError("Gunakan 1–6 butir per bidang.")
    gap = min(0.2, h / len(values) / 6)
    step = h / len(values)
    for i, value in enumerate(values):
        yy = y + i * step
        shape(s, x, yy + 0.10, 0.105, 0.105, SKY if dark else BLUE, MSO_SHAPE.OVAL)
        label(s, x + 0.26, yy, w - 0.26, step - gap, value, 20, floor=16, ink=WHITE if dark else INK)


def background(s, fill):
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = color(fill)


def polygon(s, points, fill):
    builder = s.shapes.build_freeform(*points[0], scale=Inches(1) / 100)
    builder.add_line_segments(points[1:], close=True)
    obj = builder.convert_to_shape()
    obj.fill.solid()
    obj.fill.fore_color.rgb = color(fill)
    obj.line.fill.background()


def ribbons(s, small=False):
    if small:
        polygon(s, [(0,0),(115,0),(0,158)], "143963")
        polygon(s, [(0,0),(57,0),(0,82)], "197CBE")
        polygon(s, [(1333,750),(1224,750),(1333,589)], "143963")
        polygon(s, [(1333,750),(1284,750),(1333,680)], "197CBE")
    else:
        polygon(s, [(1333,12),(1333,750),(855,750)], "111C50")
        polygon(s, [(1333,0),(1333,106),(1065,536),(1026,536)], "10477E")
        polygon(s, [(1333,116),(1333,167),(1134,479),(1109,479)], "1577B8")
        polygon(s, [(0,0),(240,0),(90,228),(0,228)], "111C50")
        polygon(s, [(120,0),(156,0),(47,164),(16,164)], "10477E")


def path_for(value, base):
    if value == "@kelas":
        return ASSETS / "kelas.jpg"
    p = Path(value)
    return p if p.is_absolute() else base / p


def image_buffer(image):
    stream = io.BytesIO()
    image.save(stream, "PNG")
    stream.seek(0)
    return stream


def picture(s, source, base, x, y, w, h, *, cover=False, alt=None):
    path = path_for(source, base)
    with Image.open(path) as original:
        im = ImageOps.exif_transpose(original).convert("RGBA")
        if cover:
            scaled = ImageOps.fit(im, (1440,810), centering=(0.52,0.46))
            overlay = Image.new("RGBA", scaled.size)
            draw = ImageDraw.Draw(overlay)
            for col in range(scaled.width):
                alpha = round(244 - 117 * col / (scaled.width - 1))
                draw.line((col,0,col,scaled.height),fill=(5,16,43,alpha))
            art = Image.alpha_composite(scaled,overlay).convert("RGB")
        else:
            ratio = min(w / im.width, h / im.height)
            ww, hh = im.width * ratio, im.height * ratio
            x, y, w, h = x + (w-ww)/2, y + (h-hh)/2, ww, hh
            art = im
        obj = s.shapes.add_picture(image_buffer(art), *area(x,y,w,h))
        obj._element.nvPicPr.cNvPr.set("descr", alt or path.stem)


def header(s, d):
    if d.get("tag"):
        label(s,0.73,0.60,10.7,0.31,d["tag"].upper(),13,ink=RED,bold=True)
    label(s,0.71,1.00,11.68,1.03,d["title"],32,floor=25,bold=True)


def brand(s, meta, base, dark=False):
    if meta.get("logo"):
        source = meta.get("logo_light",meta["logo"]) if dark else meta["logo"]
        picture(s,source,base,11.58,0.17,1.12,0.47,alt=meta.get("organization","Logo penyelenggara"))
    if meta.get("credit"):
        label(s,0.75,7.08,11.85,0.24,meta["credit"],10,ink=PALEBLUE if dark else MUTE,align=PP_ALIGN.RIGHT)


def covers(s, d, base):
    role = d["role"]
    background(s, BLUE if role == "goals" else NIGHT)
    if role in ("cover","hook") and d.get("image"):
        picture(s,d["image"],base,0,0,W,H,cover=True,alt=d.get("alt"))
    else:
        ribbons(s)
    if role == "goals":
        label(s,.94,1.09,9.5,.90,d["title"],35,floor=29,bold=True,ink=WHITE)
        vals=d["items"]
        if not 1 <= len(vals) <= 5:
            raise ValueError("Tujuan memerlukan 1–5 butir.")
        for i,val in enumerate(vals):
            yy=2.33+i*0.78
            shape(s,1.0,yy+.085,.18,.18,BLUE,stroke=WHITE)
            label(s,1.40,yy,8.3,.66,val,22,floor=18,ink=WHITE)
    elif role == "hook":
        label(s,1.42,1.86,10.45,2.78,d["title"],39,floor=29,bold=True,ink=WHITE,align=PP_ALIGN.CENTER,center=True)
        if d.get("subtitle"):
            label(s,4.15,5.48,7.8,.82,d["subtitle"],19,floor=16,ink=WHITE,align=PP_ALIGN.RIGHT)
    else:
        title = label(s,.93,2.72,9.75,1.64,d["title"],43,floor=31,bold=True,ink=WHITE,center=True)
        if role == "cover" and d.get("accent_last_line") and len(title.text_frame.paragraphs) > 1:
            for run in title.text_frame.paragraphs[-1].runs:
                run.font.color.rgb = color("50EBEA")
        if d.get("subtitle"):
            label(s,.97,4.58,8.82,1.12,d["subtitle"],23,floor=18,ink=PALEBLUE,italic=role=="divider")


def roadmap(s,d):
    ribbons(s,small=True)
    label(s,1.35,.86,10.6,.94,d["title"],33,floor=25,bold=True,align=PP_ALIGN.CENTER)
    rows=d["rows"]
    if not 1 <= len(rows) <= 4:
        raise ValueError("Peta program memerlukan 1–4 modul per slide.")
    step=min(1.36,4.75/len(rows))
    for i,row in enumerate(rows):
        y=2.16+i*step
        label(s,1.53,y,.63,.5,row["key"],22,bold=True,ink=BLUE)
        label(s,2.35,y,9.7,.49,row["title"],23,floor=19,bold=True)
        label(s,2.35,y+.51,9.7,.67,row["text"],19,floor=16,italic=True)


def compare(s,d,base):
    for i,key in enumerate(("left","right")):
        x=.76+i*6.17
        dark=i==1
        obj=d[key]
        shape(s,x,2.16,5.72,4.38,NAVY if dark else PALE)
        panel_title(s,x+.31,2.53,5.09,obj["title"],dark)
        yy=3.52
        if obj.get("image"):
            picture(s,obj["image"],base,x+.36,3.26,4.96,1.12,alt=obj.get("alt"))
            yy=4.57
        items(s,x+.32,yy,5.07,6.31-yy,obj["items"],dark)


def process(s,d,base):
    nodes=d["stages"]
    if not 2 <= len(nodes) <= 5:
        raise ValueError("Alur memerlukan 2–5 tahap.")
    step=11.9/len(nodes)
    for i,node in enumerate(nodes):
        x=.72+i*step
        if node.get("image"):
            picture(s,node["image"],base,x+.15,2.34,step-.5,1.16,alt=node.get("alt"))
        else:
            shape(s,x+.13,2.40,.82,.82,NAVY if i%2==0 else BLUE,MSO_SHAPE.OVAL)
            label(s,x+.13,2.40,.82,.82,str(i+1),22,ink=WHITE,bold=True,align=PP_ALIGN.CENTER,center=True)
        if i+1<len(nodes):
            shape(s,x+step-.42,2.73,.33,.20,BLUE,MSO_SHAPE.RIGHT_ARROW)
        label(s,x+.12,3.71,step-.40,.94,node["title"],23,floor=18,bold=True)
        label(s,x+.12,4.73,step-.41,1.25,node["text"],19,floor=16)
    if d.get("cue"):
        label(s,.83,6.36,11.6,.50,d["cue"],17,floor=15,italic=True,ink=MUTE)


def cards(s,d,base):
    vals=d["cards"]
    if not 2 <= len(vals) <= 6:
        raise ValueError("Gunakan 2–6 kartu.")
    cols=2 if len(vals) in (2,4) else 3
    rows=math.ceil(len(vals)/cols)
    cw=(11.85-(cols-1)*.22)/cols
    ch=(4.53-(rows-1)*.20)/rows
    for i,obj in enumerate(vals):
        x=.74+i%cols*(cw+.22); y=2.12+i//cols*(ch+.20)
        shape(s,x,y,cw,ch,PALE,stroke=EDGE)
        label(s,x+.23,y+.22,cw-.85,.32,f"{i+1:02}",15,ink=RED,bold=True)
        if obj.get("image"):
            picture(s,obj["image"],base,x+cw-.86,y+.12,.60,.54,alt=obj.get("alt"))
        label(s,x+.23,y+.67,cw-.47,.58,obj["title"],21,floor=17,bold=True)
        label(s,x+.23,y+1.30,cw-.47,ch-1.40,obj["text"],18,floor=15)


def lab_panel(s, d, x, y, w, h):
    shape(s,x,y,w,h,NAVY)
    shape(s,x+.28,y+.27,1.47,.35,RED)
    label(s,x+.31,y+.29,1.41,.27,d["badge"],13,ink=WHITE,bold=True,align=PP_ALIGN.CENTER)
    label(s,x+.30,y+.81,w-.60,.64,d["name"],23,floor=18,bold=True,ink=WHITE)
    label(s,x+.30,y+1.53,w-.58,.43,d["time"],16,floor=14,ink=PALEBLUE,italic=True)
    items(s,x+.30,y+2.07,w-.60,h-3.13,d["steps"],True)
    shape(s,x+.30,y+h-.93,w-.6,.015,"536E89")
    output_text = d.get("output_label", "Output") + " · " + d["output"]
    label(s,x+.30,y+h-.79,w-.65,.68,output_text,17,floor=15,bold=True,ink=WHITE)


def lab(s,d,base):
    left_w=5.62
    if d.get("image"):
        picture(s,d["image"],base,.78,2.23,left_w,1.73,alt=d.get("alt"))
        items(s,.85,4.16,5.40,2.32,d["items"])
    else:
        items(s,.85,2.50,5.4,3.80,d["items"])
    lab_panel(s,d["lab"],6.71,1.96,5.80,4.90)


def solo_lab(s,d,base):
    lab=d["lab"]
    shape(s,.76,.53,1.60,.36,RED)
    label(s,.78,.56,1.55,.26,lab["badge"],13,ink=WHITE,bold=True,align=PP_ALIGN.CENTER)
    label(s,.76,1.02,11.72,.88,d["title"],32,floor=25,bold=True)
    label(s,.79,1.94,11.47,.45,lab["time"],17,floor=15,italic=True,ink=MUTE)
    source=d.get("items",[])
    prompt=" ".join(source)
    if prompt:
        label(s,.79,2.52,11.60,.71,prompt,20,floor=17)
    steps=lab["steps"]
    if not 1 <= len(steps) <= 6:
        raise ValueError("Micro-lab memerlukan 1–6 tugas.")
    field_w=7.18 if d.get("image") else 11.70
    cols=2 if len(steps)>3 and not d.get("image") else 1
    rows=math.ceil(len(steps)/cols)
    block_w=(field_w-(cols-1)*.15)/cols
    block_h=min(.83,2.70/rows-.08)
    for i,line in enumerate(steps):
        x=.79+(i%cols)*(block_w+.15)
        y=3.40+(i//cols)*(block_h+.08)
        shape(s,x,y,block_w,block_h,NAVY)
        label(s,x+.13,y,.47,block_h,chr(65+i),17,floor=14,ink=SKY,bold=True,center=True)
        label(s,x+.69,y,block_w-.88,block_h,line,18,floor=15,ink=WHITE,center=True)
    if d.get("image"):
        picture(s,d["image"],base,8.13,3.13,4.42,2.98,alt=d.get("alt"))
    output_text = lab.get("output_label", "Output") + " · " + lab["output"]
    label(s,.79,6.26,11.70,.54,output_text,18,floor=16,bold=True)



def takeaway(s,d,base):
    if d.get("image"):
        picture(s,d["image"],base,5.85,1.87,7.06,4.90,alt=d.get("alt"))
    label(s,.87,2.03,5.08 if d.get("image") else 10.9,1.99,d["title"],34,floor=26,bold=True)
    label(s,.90,4.31,4.96 if d.get("image") else 10.7,1.72,d["subtitle"],22,floor=18,italic=True)


def project(s,d):
    shape(s,.76,2.08,11.8,.76,PALE)
    label(s,.98,2.24,11.33,.44,d["setup"],17,floor=15,bold=True)
    label(s,.88,3.21,5.6,.59,d.get("work_title","Tugas"),23,bold=True)
    items(s,.88,4.03,5.50,2.45,d["work"])
    shape(s,6.77,3.04,5.75,3.68,NAVY)
    label(s,7.05,3.32,5.19,.65,d.get("evidence_title","Bukti yang dikumpulkan"),22,floor=18,bold=True,ink=WHITE)
    items(s,7.05,4.18,5.09,2.28,d["evidence"],True)


def close(s,d,meta,base):
    polygon(s,[(887,0),(1025,0),(1333,375),(1025,750),(887,750),(1195,375)],"F4F6F9")
    if meta.get("logo"):
        picture(s,meta["logo"],base,4.60,2.10,4.13,1.58,alt=meta.get("organization","Penyelenggara"))
    label(s,1.30,3.98 if meta.get("logo") else 2.68,10.7,1.16,d["title"],30,floor=24,bold=True,center=True,align=PP_ALIGN.CENTER)
    if d.get("subtitle"):
        label(s,1.65,5.23 if meta.get("logo") else 4.09,10.03,.95,d["subtitle"],20,floor=17,align=PP_ALIGN.CENTER,ink=MUTE)


def render(spec, base):
    prs=Presentation()
    prs.slide_width,prs.slide_height=Inches(W),Inches(H)
    meta=spec.get("meta",{})
    if not isinstance(spec.get("slides"),list) or not spec["slides"]:
        raise ValueError("slides harus berupa daftar yang berisi setidaknya satu slide.")
    prs.core_properties.title=meta.get("title",spec["slides"][0].get("title","PPT Instruktur"))
    prs.core_properties.author=meta.get("organization","")
    for i,d in enumerate(spec["slides"],1):
        try:
            role=d["role"]
            s=prs.slides.add_slide(prs.slide_layouts[6])
            background(s,WHITE)
            dark=role in ("cover","hook","day","divider","goals")
            if dark:
                covers(s,d,base)
            elif role=="roadmap":
                roadmap(s,d)
            elif role=="lab":
                solo_lab(s,d,base)
            elif role=="takeaway":
                takeaway(s,d,base)
            elif role=="close":
                close(s,d,meta,base)
            else:
                header(s,d)
                if role=="compare": compare(s,d,base)
                elif role=="process": process(s,d,base)
                elif role=="cards": cards(s,d,base)
                elif role=="teach_lab": lab(s,d,base)
                elif role=="project": project(s,d)
                else: raise ValueError(f"Peran slide tidak dikenal: {role}")
            brand(s,meta if role!="close" else {"credit":meta.get("credit")},base,dark)
            if not isinstance(d.get("notes"),str) or not d["notes"].strip():
                raise ValueError("Tambahkan notes untuk instruktur.")
            s.notes_slide.notes_text_frame.text=d["notes"]
        except (KeyError,ValueError,TypeError,OSError) as exc:
            raise ValueError(f"Slide {i}: {exc}") from exc
    return prs


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief",type=Path)
    parser.add_argument("output",type=Path)
    args=parser.parse_args()
    spec=json.loads(args.brief.read_text(encoding="utf-8-sig"))
    deck=render(spec,args.brief.resolve().parent)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    from tempfile import NamedTemporaryFile
    with NamedTemporaryFile(suffix=".pptx",dir=args.output.parent,delete=False) as f:
        temp=Path(f.name)
    try:
        deck.save(temp)
        temp.replace(args.output)
    finally:
        temp.unlink(missing_ok=True)
    print(f"{len(deck.slides)} slide tersimpan di {args.output}")


if __name__=="__main__":
    try:
        main()
    except (ValueError, OSError) as exc:
        sys.exit(str(exc))

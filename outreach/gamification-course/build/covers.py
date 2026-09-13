#!/usr/bin/env python3
"""Generate branded Gumroad cover images (1280x720) for each product."""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = "/home/user/STORMSTUDIO/outreach/gamification-course/gumroad/covers"
os.makedirs(OUT, exist_ok=True)
FD = "/usr/share/fonts/truetype/liberation/"
def F(name,size): return ImageFont.truetype(FD+name, size)

INK=(31,42,48); GREEN=(46,110,78); COPPER=(181,101,46)
PAPER=(250,247,240); MUTED=(94,106,110); RULE=(228,222,207)
W,H=1280,720

def wrap(draw, text, font, maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if draw.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def cover(fname, kicker, title, subtitle, tag=None):
    img=Image.new("RGB",(W,H),PAPER); d=ImageDraw.Draw(img)
    # left accent bar
    d.rectangle([0,0,16,H],fill=GREEN)
    x=90; y=250
    # kicker
    d.text((x,y),kicker.upper(),font=F("LiberationSans-Bold.ttf",26),fill=COPPER)
    y+=44
    # copper rule
    d.rectangle([x,y,x+90,y+5],fill=COPPER); y+=42
    # title (serif bold, wrap)
    tf=F("LiberationSerif-Bold.ttf",76)
    for ln in wrap(d,title,tf,W-x-90):
        d.text((x,y),ln,font=tf,fill=INK); y+=88
    y+=8
    if subtitle:
        sf=F("LiberationSerif-Italic.ttf",34)
        for ln in wrap(d,subtitle,sf,W-x-120):
            d.text((x,y),ln,font=sf,fill=MUTED); y+=46
    # footer
    d.line([(x,H-70),(W-70,H-70)],fill=RULE,width=2)
    d.text((x,H-52),"StormStudio  ·  Curriculum by Kevin Storm",font=F("LiberationSans-Regular.ttf",24),fill=MUTED)
    kf=F("LiberationSans-Bold.ttf",24)
    d.text((W-70-d.textlength("kevinstorm.eu",font=kf),H-52),"kevinstorm.eu",font=kf,fill=GREEN)
    # optional tag chip top-right
    if tag:
        cf=F("LiberationSans-Bold.ttf",24)
        tw=d.textlength(tag,font=cf); pad=18
        d.rounded_rectangle([W-70-tw-pad*2, 60, W-70, 108], radius=8, fill=INK)
        d.text((W-70-tw-pad, 72), tag, font=cf, fill=PAPER)
    img.save(os.path.join(OUT,fname),"PNG")
    print("wrote",fname)

cover("01-complete-course.png","Complete course","Gamification & Immersive Learning",
      "The complete two-day teacher-training course","FLAGSHIP")
cover("02-ai-in-education.png","Mini-course","AI in Education",
      "Practical AI for teachers, and AI literacy for students")
cover("03-game-design-delightex.png","Mini-course","Game Design with Delightex",
      "Build 3D worlds, code them, step inside in AR/VR")
cover("04-inclusive-gamification.png","Mini-course","Inclusive Gamification",
      "Game-based learning that works for every learner")
cover("05-bundle.png","Bundle","Full Immersive Educator Bundle",
      "The full course plus all three mini-courses","BEST VALUE")
cover("06-six-levers-free.png","Free field guide","The 6 Levers of Engagement",
      "Gamify any lesson, without the gimmicks","FREE")
print("done")

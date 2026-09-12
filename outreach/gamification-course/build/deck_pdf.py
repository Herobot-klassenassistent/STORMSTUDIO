#!/usr/bin/env python3
"""StormStudio Curriculum - slide deck renderer (landscape).
Each '## ' starts a new slide; '# ' is a section divider slide.
'- ' bullets; '> note' becomes a speaker note line. Front-matter title -> title slide.
Usage: python3 deck_pdf.py <slides.md> <out.pdf>
"""
import sys, re
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as canvasmod

FD="/usr/share/fonts/truetype/liberation/"
for n,f in [("Serif","LiberationSerif-Regular.ttf"),("Serif-B","LiberationSerif-Bold.ttf"),
            ("Serif-I","LiberationSerif-Italic.ttf"),("Sans","LiberationSans-Regular.ttf"),
            ("Sans-B","LiberationSans-Bold.ttf"),("Sans-I","LiberationSans-Italic.ttf")]:
    try: pdfmetrics.registerFont(TTFont(n,FD+f))
    except: pass

INK=colors.HexColor("#1F2A30"); GREEN=colors.HexColor("#2E6E4E")
COPPER=colors.HexColor("#B5652E"); MUTED=colors.HexColor("#5E6A6E")
RULE=colors.HexColor("#D7D2C4"); CREAM=colors.HexColor("#FBF9F3")
PW,PH=landscape(A4); LM=22*mm

def parse(src):
    fm={}; body=src
    m=re.match(r"^---\n(.*?)\n---\n(.*)$",src,re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line: k,v=line.split(":",1); fm[k.strip()]=v.strip()
        body=m.group(2)
    return fm,body

def slides_from(body):
    slides=[]; cur=None
    for raw in body.splitlines():
        s=raw.rstrip()
        st=s.strip()
        if st.startswith("## "):
            if cur: slides.append(cur)
            cur={"type":"content","title":st[3:],"bullets":[],"note":None,"sub":[]}
        elif st.startswith("# "):
            if cur: slides.append(cur)
            cur={"type":"divider","title":st[2:],"bullets":[],"note":None,"sub":[]}
        elif st.startswith("### "):
            if cur: cur["bullets"].append(("h",st[4:]))
        elif re.match(r">\s*",st) and cur:
            cur["note"]=re.sub(r">\s*(\[!\w+\]\s*)?","",st)
        elif (st.startswith("- ") or st.startswith("* ")) and cur:
            cur["bullets"].append(("b",st[2:]))
        elif st and cur and cur["type"]=="content":
            cur["bullets"].append(("p",st))
    if cur: slides.append(cur)
    return slides

def clean(t):
    t=re.sub(r"\*\*(.+?)\*\*",r"\1",t); t=re.sub(r"\*(.+?)\*",r"\1",t)
    t=re.sub(r"`(.+?)`",r"\1",t); t=re.sub(r"\[(.+?)\]\(.+?\)",r"\1",t)
    return t

def wrap(c,text,font,size,maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if c.stringWidth(t,font,size)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def chrome(c,idx,total):
    c.setFillColor(GREEN); c.rect(0,0,4*mm,PH,fill=1,stroke=0)
    c.setStrokeColor(RULE); c.setLineWidth(0.5); c.line(LM,14*mm,PW-18*mm,14*mm)
    c.setFont("Sans",8); c.setFillColor(MUTED)
    c.drawString(LM,9.5*mm,"STORMSTUDIO · CURRICULUM   ·   kevinstorm.eu/curriculum")
    c.setFillColor(COPPER); c.drawRightString(PW-18*mm,9.5*mm,f"{idx}/{total}")

def title_slide(c,fm):
    c.setFillColor(GREEN); c.rect(0,0,4*mm,PH,fill=1,stroke=0)
    x=LM; y=PH-70*mm
    c.setFont("Sans-B",11); c.setFillColor(COPPER)
    c.drawString(x,y+16*mm,fm.get("kicker","StormStudio Curriculum").upper())
    c.setStrokeColor(COPPER); c.setLineWidth(2.4); c.line(x,y+10*mm,x+22*mm,y+10*mm)
    c.setFillColor(INK)
    for ln in wrap(c,fm.get("title","Slides"),"Serif-B",40,PW-LM-40*mm):
        c.setFont("Serif-B",40); c.drawString(x,y,ln); y-=15*mm
    if fm.get("subtitle"):
        c.setFillColor(MUTED); c.setFont("Serif-I",16)
        c.drawString(x,y+3*mm,fm["subtitle"])
    c.setFont("Sans-B",10); c.setFillColor(GREEN)
    c.drawString(x,20*mm,"kevinstorm.eu/curriculum")
    c.showPage()

def divider_slide(c,title,idx,total):
    c.setFillColor(INK); c.rect(0,0,PW,PH,fill=1,stroke=0)
    c.setFillColor(GREEN); c.rect(0,0,4*mm,PH,fill=1,stroke=0)
    c.setFont("Sans-B",11); c.setFillColor(COPPER)
    c.drawString(LM,PH/2+14*mm,"SECTION")
    c.setFillColor(CREAM)
    y=PH/2
    for ln in wrap(c,clean(title),"Serif-B",34,PW-LM-40*mm):
        c.setFont("Serif-B",34); c.drawString(LM,y,ln); y-=13*mm
    c.setFillColor(colors.HexColor("#9AA6A0")); c.setFont("Sans",8)
    c.drawRightString(PW-18*mm,9.5*mm,f"{idx}/{total}")
    c.showPage()

def content_slide(c,s,idx,total):
    x=LM; top=PH-24*mm
    c.setFont("Sans-B",9.5); c.setFillColor(COPPER)
    c.drawString(x,PH-16*mm,"GAMIFICATION & IMMERSIVE LEARNING")
    c.setFillColor(INK)
    ty=top
    for ln in wrap(c,clean(s["title"]),"Serif-B",25,PW-LM-30*mm):
        c.setFont("Serif-B",25); c.drawString(x,ty,ln); ty-=10*mm
    c.setStrokeColor(COPPER); c.setLineWidth(2); c.line(x,ty+4*mm,x+18*mm,ty+4*mm)
    y=ty-6*mm
    for kind,txt in s["bullets"]:
        txt=clean(txt)
        if kind=="h":
            c.setFillColor(GREEN); c.setFont("Sans-B",14)
            for ln in wrap(c,txt,"Sans-B",14,PW-LM-32*mm):
                c.drawString(x,y,ln); y-=8*mm
            y-=1*mm
        else:
            c.setFillColor(GREEN); c.setFont("Sans-B",13); c.drawString(x,y,"•")
            c.setFillColor(INK); c.setFont("Sans",13)
            lines=wrap(c,txt,"Sans",13,PW-LM-34*mm)
            for i,ln in enumerate(lines):
                c.drawString(x+7*mm,y,ln); y-=7.2*mm
            y-=1.4*mm
        if y<26*mm: break
    if s.get("note"):
        c.setStrokeColor(RULE); c.setLineWidth(0.5); c.line(LM,20*mm,PW-18*mm,20*mm)
        c.setFillColor(MUTED); c.setFont("Sans-I",8.5)
        note=clean(s["note"])
        nl=wrap(c,"Trainer note: "+note,"Sans-I",8.5,PW-LM-30*mm)
        yy=16.5*mm
        for ln in nl[:1]:
            c.drawString(LM,yy,ln)
    chrome(c,idx,total)
    c.showPage()

def render(src_path,out_path):
    with open(src_path) as f: src=f.read()
    fm,body=parse(src); slides=slides_from(body)
    c=canvasmod.Canvas(out_path,pagesize=landscape(A4))
    c.setTitle(fm.get("title","Slides"))
    total=len(slides)+1
    title_slide(c,fm)
    for i,s in enumerate(slides,start=2):
        if s["type"]=="divider": divider_slide(c,s["title"],i,total)
        else: content_slide(c,s,i,total)
    c.save(); print("wrote",out_path,"(",total,"slides )")

if __name__=="__main__":
    render(sys.argv[1],sys.argv[2])

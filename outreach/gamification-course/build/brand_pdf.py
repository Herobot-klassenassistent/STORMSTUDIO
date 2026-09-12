#!/usr/bin/env python3
"""StormStudio Curriculum - branded PDF renderer (portrait documents).

Usage: python3 brand_pdf.py <source.md> <out.pdf>
Markdown front-matter (--- ... ---) keys: kicker, title, subtitle, doclabel.
Supports: # ## ### headings, - bullets, 1. numbered, pipe tables, --- rules,
callouts  > [!note] / [!tip] / [!assignment] / [!step] / [!quote] text,
inline **bold** *italic* `code`.
"""
import sys, re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    ListFlowable, ListItem, Table, TableStyle, PageBreak, Flowable, KeepTogether,
    FrameBreak, NextPageTemplate, PageTemplate, Frame)
from reportlab.platypus.tableofcontents import TableOfContents

# ---------- fonts ----------
FD = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("Serif",      FD+"LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-B",    FD+"LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Serif-I",    FD+"LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Sans",       FD+"LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans-B",     FD+"LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-I",     FD+"LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Mono",       FD+"LiberationMono-Regular.ttf"))

# ---------- palette ----------
INK    = colors.HexColor("#1F2A30")
GREEN  = colors.HexColor("#2E6E4E")
COPPER = colors.HexColor("#B5652E")
PAPER  = colors.HexColor("#F3F0E7")   # callout fill
CREAM  = colors.HexColor("#FBF9F3")
RULE   = colors.HexColor("#D7D2C4")
MUTED  = colors.HexColor("#5E6A6E")
LIGHT  = colors.HexColor("#EFECE3")

PW, PH = A4
LM = RM = 20*mm
TM = 20*mm; BM = 20*mm

def st(name,font="Sans",size=10.2,lead=15,color=INK,after=7,before=0,align=TA_LEFT,li=0):
    return ParagraphStyle(name,fontName=font,fontSize=size,leading=lead,textColor=color,
        spaceAfter=after,spaceBefore=before,alignment=align,leftIndent=li)

BODY = st("body",lead=14,after=6)
H2   = st("h2",font="Serif-B",size=15,lead=19,color=INK,before=16,after=5)
H3   = st("h3",font="Sans-B",size=11,lead=15,color=GREEN,before=10,after=3)
LIS  = st("li",after=3,lead=14.5)
NUM  = st("num",after=3,lead=14.5,li=15)
META = st("meta",font="Sans-I",size=9,lead=13,color=MUTED,after=6)
CALL = st("call",size=9.8,lead=14.5,color=INK,after=0)
CALLL= st("calll",font="Sans-B",size=7.6,lead=10,color=GREEN,after=3)
TH   = st("th",font="Sans-B",size=9,lead=12,color=colors.white)
TD   = st("td",font="Sans",size=9,lead=12.5,color=INK)

import os as _os
_LANG = _os.environ.get("PDF_LANG","en")
if _LANG == "nl":
    CALLOUT_COLORS = {
     "note":(GREEN,"NB"),"tip":(COPPER,"TIP"),"assignment":(INK,"OPDRACHT"),
     "step":(GREEN,"STAP"),"quote":(COPPER,"") ,"key":(COPPER,"KERN")}
else:
    CALLOUT_COLORS = {
     "note":(GREEN,"NOTE"),"tip":(COPPER,"TIP"),"assignment":(INK,"ASSIGNMENT"),
     "step":(GREEN,"STEP"),"quote":(COPPER,"") ,"key":(COPPER,"KEY POINT")}

def inline(t):
    t=t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    t=re.sub(r"\*\*(.+?)\*\*",r"<b>\1</b>",t)
    t=re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)",r"<i>\1</i>",t)
    t=re.sub(r"`(.+?)`",r'<font face="Mono" size="9" color="#B5652E">\1</font>',t)
    t=re.sub(r"\[(.+?)\]\((.+?)\)",r'<font color="#2E6E4E"><u>\1</u></font>',t)
    t=re.sub(r"(?<![\">=])(https?://[^\s<)]+)",r'<font color="#2E6E4E"><u>\1</u></font>',t)
    return t

class Callout(Flowable):
    def __init__(self,kind,text):
        super().__init__(); self.kind=kind
        self.bar,self.label=CALLOUT_COLORS.get(kind,(GREEN,kind.upper()))
        self.text=text; self.width=PW-LM-RM
    def wrap(self,aw,ah):
        self.width=aw
        self._label=Paragraph(self.label,CALLL) if self.label else None
        self._p=Paragraph(inline(self.text),CALL)
        innerw=aw-20
        lh=self._label.wrap(innerw,1000)[1]+2 if self._label else 0
        ph=self._p.wrap(innerw,1000)[1]
        self.h=lh+ph+16
        return aw,self.h
    def draw(self):
        c=self.canv
        c.setFillColor(PAPER); c.setStrokeColor(PAPER)
        c.roundRect(0,0,self.width,self.h,3,fill=1,stroke=0)
        c.setFillColor(self.bar)
        c.rect(0,0,3.2,self.h,fill=1,stroke=0)
        y=self.h-10
        if self._label:
            self._label.drawOn(c,12,y-self._label.height+2); y-=self._label.height+3
        self._p.drawOn(c,12,y-self._p.height)

def make_table(rows):
    header=[Paragraph(inline(c),TH) for c in rows[0]]
    data=[header]+[[Paragraph(inline(c),TD) for c in r] for r in rows[1:]]
    n=len(rows[0]); avail=PW-LM-RM
    t=Table(data,colWidths=[avail/n]*n,repeatRows=1)
    sty=[("BACKGROUND",(0,0),(-1,0),INK),("TEXTCOLOR",(0,0),(-1,0),colors.white),
         ("VALIGN",(0,0),(-1,-1),"TOP"),("TOPPADDING",(0,0),(-1,-1),5),
         ("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),7),
         ("RIGHTPADDING",(0,0),(-1,-1),7),
         ("LINEBELOW",(0,0),(-1,-1),0.4,RULE),("LINEAFTER",(0,0),(-2,-1),0.4,RULE)]
    for i in range(1,len(data)):
        if i%2==0: sty.append(("BACKGROUND",(0,i),(-1,i),LIGHT))
    t.setStyle(TableStyle(sty)); return t

# ---------- parse ----------
def parse(src):
    fm={}; body=src
    m=re.match(r"^---\n(.*?)\n---\n(.*)$",src,re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k,v=line.split(":",1); fm[k.strip()]=v.strip()
        body=m.group(2)
    return fm,body

def build_story(body):
    story=[]; bullets=[]; tbl=[]
    def flush_b():
        nonlocal bullets
        if bullets:
            items=[ListItem(Paragraph(inline(b),LIS),leftIndent=4) for b in bullets]
            story.append(ListFlowable(items,bulletType="bullet",start="•",
                leftIndent=14,bulletColor=GREEN,bulletFontSize=7,bulletOffsetY=1))
            story.append(Spacer(1,4)); bullets=[]
    def flush_t():
        nonlocal tbl
        if tbl:
            story.append(Spacer(1,2)); story.append(make_table(tbl))
            story.append(Spacer(1,8)); tbl=[]
    for raw in body.splitlines():
        s=raw.strip()
        if s.startswith("|") and s.endswith("|"):
            cells=[c.strip() for c in s.strip("|").split("|")]
            if set("".join(cells).replace("-","").replace(":",""))==set(): continue
            tbl.append(cells); continue
        else: flush_t()
        if not s: flush_b(); continue
        cm=re.match(r">\s*\[!(\w+)\]\s*(.*)",s)
        if cm:
            flush_b(); story.append(Spacer(1,2))
            story.append(Callout(cm.group(1).lower(),cm.group(2))); story.append(Spacer(1,8)); continue
        if s.startswith("## "):
            flush_b()
            story.append(HRFlowable(width=40,thickness=2,color=COPPER,spaceBefore=14,spaceAfter=1,hAlign="LEFT"))
            story.append(Paragraph(inline(s[3:]),H2)); continue
        if s.startswith("### "):
            flush_b(); story.append(Paragraph(inline(s[4:]),H3)); continue
        if s.startswith("# "):
            flush_b(); story.append(Paragraph(inline(s[2:]),st("h1big",font="Serif-B",size=19,lead=23,after=6))); continue
        if re.match(r"^(---|\*\*\*|___)$",s):
            flush_b(); story.append(HRFlowable(width="100%",thickness=0.6,color=RULE,spaceBefore=8,spaceAfter=8)); continue
        mnum=re.match(r"^(\d+)\.\s+(.*)",s)
        if mnum:
            flush_b()
            story.append(Paragraph(f'<font color="#B5652E" face="Sans-B">{mnum.group(1)}.</font>&nbsp;&nbsp;{inline(mnum.group(2))}',NUM)); continue
        if s.startswith("- ") or s.startswith("* "):
            bullets.append(s[2:]); continue
        flush_b(); story.append(Paragraph(inline(s),BODY))
    flush_b(); flush_t()
    return story

# ---------- cover + chrome ----------
def _wrap(canvas,text,font,size,maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if canvas.stringWidth(t,font,size)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def draw_cover(canvas,doc,fm):
    canvas.saveState()
    # slim left accent bar
    canvas.setFillColor(GREEN); canvas.rect(0,0,4*mm,PH,fill=1,stroke=0)
    x=LM; y=PH-92*mm
    if fm.get("kicker"):
        canvas.setFont("Sans-B",9.5); canvas.setFillColor(COPPER)
        canvas.drawString(x,y,fm["kicker"].upper()); y-=8*mm
    canvas.setStrokeColor(COPPER); canvas.setLineWidth(2.4)
    canvas.line(x,y,x+19*mm,y); y-=12*mm
    canvas.setFillColor(INK)
    for ln in _wrap(canvas,fm.get("title","Untitled"),"Serif-B",33,PW-LM-RM):
        canvas.setFont("Serif-B",33); canvas.drawString(x,y,ln); y-=13*mm
    y-=1*mm
    if fm.get("subtitle"):
        canvas.setFillColor(MUTED)
        for ln in _wrap(canvas,fm["subtitle"],"Serif-I",14,PW-LM-RM-6*mm):
            canvas.setFont("Serif-I",14); canvas.drawString(x,y,ln); y-=6.6*mm
    # footer block
    canvas.setStrokeColor(RULE); canvas.setLineWidth(0.8)
    canvas.line(LM,30*mm,PW-RM,30*mm)
    canvas.setFont("Sans",9.5); canvas.setFillColor(MUTED)
    dl=fm.get("doclabel","Course material")
    canvas.drawString(LM,24*mm,f"StormStudio   ·   Curriculum by Kevin Storm   ·   {dl}")
    canvas.setFont("Sans-B",9.5); canvas.setFillColor(GREEN)
    canvas.drawString(LM,18.5*mm,"kevinstorm.eu/curriculum")
    canvas.restoreState()

def make_chrome(fm):
    doctitle=fm.get("title","")
    def chrome(canvas,doc):
        canvas.saveState()
        if doc.page>1:
            canvas.setFont("Sans",7.5); canvas.setFillColor(MUTED)
            canvas.drawString(LM,PH-12*mm,"STORMSTUDIO · CURRICULUM")
            canvas.drawRightString(PW-RM,PH-12*mm,doctitle.upper()[:60])
            canvas.setStrokeColor(RULE); canvas.setLineWidth(0.4)
            canvas.line(LM,PH-13.5*mm,PW-RM,PH-13.5*mm)
            canvas.setStrokeColor(RULE); canvas.line(LM,15*mm,PW-RM,15*mm)
            canvas.setFont("Sans",8); canvas.setFillColor(MUTED)
            canvas.drawString(LM,10.5*mm,"kevinstorm.eu")
            canvas.setFillColor(COPPER)
            canvas.drawRightString(PW-RM,10.5*mm,str(doc.page))
        canvas.restoreState()
    return chrome

def render(src_path,out_path):
    with open(src_path) as f: src=f.read()
    fm,body=parse(src)
    story=[PageBreak()]+build_story(body)
    doc=SimpleDocTemplate(out_path,pagesize=A4,leftMargin=LM,rightMargin=RM,
        topMargin=TM,bottomMargin=BM,title=fm.get("title",""),author="Kevin Storm")
    ch=make_chrome(fm)
    doc.build(story,onFirstPage=lambda c,d:draw_cover(c,d,fm),onLaterPages=ch)
    print("wrote",out_path)

if __name__=="__main__":
    render(sys.argv[1],sys.argv[2])

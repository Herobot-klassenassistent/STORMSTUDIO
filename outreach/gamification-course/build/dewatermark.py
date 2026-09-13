#!/usr/bin/env python3
"""Remove AI-typographic tells: em dashes, en dashes, curly quotes.
Keeps meaning; converts to plain human punctuation Kevin uses."""
import sys, re, glob, os

def fix_line(line):
    # headings and title/front-matter lines read better with a colon
    is_head = line.lstrip().startswith("#") or re.match(r"^(title|subtitle|kicker):", line)
    if " — " in line and is_head:
        line = line.replace(" — ", ": ", 1)
    line = line.replace(" — ", ", ")
    line = line.replace(" —", ",").replace("— ", ", ").replace("—", ", ")
    line = line.replace(" – ", ", ").replace("–", "-")
    return line

def fix(text):
    text = "\n".join(fix_line(l) for l in text.split("\n"))
    # curly quotes -> straight
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("…", "...")  # ellipsis char -> ...
    # tidy doubles created
    text = re.sub(r",\s*,", ",", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r",\s*\.", ".", text)
    text = re.sub(r"\(\s*,\s*", "(", text)
    return text

files=[]
for d in ["product","product-nl","gumroad","market"]:
    files += glob.glob(f"{d}/**/*.md", recursive=True)
    files += glob.glob(f"{d}/**/*.html", recursive=True)
changed=0
for f in files:
    s=open(f,encoding="utf-8").read()
    n=fix(s)
    if n!=s:
        open(f,"w",encoding="utf-8").write(n); changed+=1; print("cleaned",f)
print(f"--- {changed} files changed ---")

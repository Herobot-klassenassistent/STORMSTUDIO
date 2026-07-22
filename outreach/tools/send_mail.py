#!/usr/bin/env python3
"""
Verstuur e-mail via de Gmail API (alleen HTTPS - werkt binnen het
netwerkbeleid van deze omgeving; SMTP en derde-partij mail-API's zijn hier
geblokkeerd).

Leest de credentials UITSLUITEND uit environment variables. Zet nooit
geheimen in dit bestand of in de repo:

    GMAIL_CLIENT_ID       OAuth client id
    GMAIL_CLIENT_SECRET   OAuth client secret
    GMAIL_REFRESH_TOKEN   refresh token met scope gmail.send
    GMAIL_SENDER          jouw afzenderadres (bv. kevinstorm1980@gmail.com)

Gebruik:
    # testverbinding (haalt alleen een access token op, verstuurt niets)
    python send_mail.py --check

    # 1 mail sturen (dry-run laat zien wat er zou gaan, verstuurt niets)
    python send_mail.py --to naam@school.nl --subject "..." --body-file mail.txt --dry-run
    python send_mail.py --to naam@school.nl --subject "..." --body-file mail.txt

Exit codes: 0 ok, 1 configuratie/afzender-fout, 2 verzendfout.
"""
import argparse
import base64
import json
import os
import sys
import urllib.parse
import urllib.request
from email.message import EmailMessage

TOKEN_URL = "https://oauth2.googleapis.com/token"
SEND_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"


def _need(name):
    val = os.environ.get(name)
    if not val:
        sys.stderr.write(
            f"FOUT: environment variable {name} ontbreekt. Zet de Gmail-"
            f"credentials in de omgevingsinstellingen, niet in dit bestand.\n"
        )
        sys.exit(1)
    return val


def get_access_token():
    data = urllib.parse.urlencode({
        "client_id": _need("GMAIL_CLIENT_ID"),
        "client_secret": _need("GMAIL_CLIENT_SECRET"),
        "refresh_token": _need("GMAIL_REFRESH_TOKEN"),
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=data)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)["access_token"]
    except urllib.error.HTTPError as e:
        sys.stderr.write("Token ophalen mislukt: %s\n%s\n" % (e, e.read().decode()))
        sys.exit(2)


def build_mime(sender, to, subject, body):
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    return base64.urlsafe_b64encode(msg.as_bytes()).decode()


def send(access_token, raw):
    body = json.dumps({"raw": raw}).encode()
    req = urllib.request.Request(
        SEND_URL, data=body,
        headers={"Authorization": "Bearer " + access_token,
                 "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.stderr.write("Verzenden mislukt: %s\n%s\n" % (e, e.read().decode()))
        sys.exit(2)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true",
                   help="alleen token ophalen om de verbinding te testen")
    p.add_argument("--to")
    p.add_argument("--subject")
    p.add_argument("--body-file")
    p.add_argument("--dry-run", action="store_true",
                   help="toon de mail maar verstuur niet")
    a = p.parse_args()

    if a.check:
        get_access_token()
        print("OK - Gmail API bereikbaar en credentials werken.")
        return

    if not (a.to and a.subject and a.body_file):
        p.error("--to, --subject en --body-file zijn verplicht")

    sender = _need("GMAIL_SENDER")
    with open(a.body_file, encoding="utf-8") as f:
        body = f.read()

    print(f"Van : {sender}\nAan : {a.to}\nOnd.: {a.subject}\n--- body ---\n{body}\n---")
    if a.dry_run:
        print("[dry-run] niets verstuurd.")
        return

    token = get_access_token()
    res = send(token, build_mime(sender, a.to, a.subject, body))
    print("Verstuurd. Message id:", res.get("id"))


if __name__ == "__main__":
    main()

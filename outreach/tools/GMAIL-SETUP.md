# Gmail-verzending instellen (eenmalig)

Waarom Gmail API en niet gewoon SMTP of een tool als Resend? In deze omgeving
blokkeert het netwerkbeleid SMTP en de meeste mail-API's. Alleen Google's
HTTPS-endpoints zijn bereikbaar. Daarom: Gmail API met OAuth.

> **Veiligheid:** plak de client secret en het refresh token NOOIT in de chat
> of in een bestand in de repo. Ze horen thuis in de omgevingsinstellingen
> (secrets/env-vars). Belanden ze toch ergens zichtbaar? Intrekken en opnieuw
> aanmaken.

## Stap 1 — Google Cloud project + Gmail API
1. Ga naar https://console.cloud.google.com/ en maak een project (bv. "storm-mail").
2. "APIs & Services" > "Enable APIs and Services" > zoek **Gmail API** > Enable.

## Stap 2 — OAuth consent screen
1. "APIs & Services" > "OAuth consent screen".
2. User type: **External**. Vul app-naam + jouw e-mail in.
3. Scopes: voeg toe `https://www.googleapis.com/auth/gmail.send`.
4. Test users: voeg **jouw eigen Gmail-adres** toe (kevinstorm1980@gmail.com).
   (Zolang de app in "testing" staat is dat genoeg; niet publiceren nodig.)

## Stap 3 — OAuth client
1. "APIs & Services" > "Credentials" > "Create credentials" > "OAuth client ID".
2. Application type: **Desktop app**. Maak aan.
3. Noteer **Client ID** en **Client secret**.

## Stap 4 — Eenmalig een refresh token maken
Dit doe je **op je eigen computer** (deze omgeving heeft geen browser voor de
consent-redirect). Twee manieren:

**A. OAuth 2.0 Playground (snelst)**
1. Ga naar https://developers.google.com/oauthplayground
2. Klik het tandwiel rechtsboven > "Use your own OAuth credentials" > vul je
   Client ID + secret in.
3. Links bij "Input your own scopes" typ: `https://www.googleapis.com/auth/gmail.send`
   > Authorize APIs > log in met je Gmail > sta toe.
4. Klik "Exchange authorization code for tokens". Kopieer het **refresh token**.

**B. Lokaal scriptje** (als je liever geen Playground gebruikt) — vraag me,
dan geef ik een klein Python-flowtje dat je één keer lokaal draait.

## Stap 5 — Zet de secrets in de omgeving (niet in de chat!)
Zet in de omgevingsinstellingen van Claude Code op het web (Environment >
variables/secrets) deze vier waarden:

    GMAIL_CLIENT_ID       = <client id uit stap 3>
    GMAIL_CLIENT_SECRET   = <client secret uit stap 3>
    GMAIL_REFRESH_TOKEN   = <refresh token uit stap 4>
    GMAIL_SENDER          = kevinstorm1980@gmail.com

Docs over omgevingsvariabelen:
https://code.claude.com/docs/en/claude-code-on-the-web

## Stap 6 — Testen (doe ik in de volgende sessie)
    python outreach/tools/send_mail.py --check
    # daarna een testmail naar jezelf:
    python outreach/tools/send_mail.py --to kevinstorm1980@gmail.com \
        --subject "Test" --body-file outreach/mails/01-...md --dry-run

## Belangrijk voor koude werving
- Gmail-limiet is ~500 ontvangers/dag; stuur in kleine, gespreide batches.
- Zet onderaan elke mail wie je bent + een makkelijke afmeldregel (AVG).
- Werkwijze blijft: ik zet klaar, jij keurt goed, ik verstuur per batch.

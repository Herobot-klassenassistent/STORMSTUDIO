# Storm Network Map

An interactive, filterable map of Kevin's professional network, by sector, built to
empower the search for work. Live artifact: published from
`storm-network-map.html` (private, owner-only unless shared).

## What it shows
Kevin at the centre, sector hubs around him, and every verified contact attached to
the sectors they belong to. Click a node for the relationship: how they worked
together, the network they came through, location, note, and email. Filter by sector
and by warmth (hot lead, worked together, warm, known contact, door left open). Search
jumps to a name.

## Sectors
music, edtech & international, education/PD, primary & schools, special needs & care,
culture & arts, libraries, media & literacy, social & refugees, government & funding.

## How it was seeded
From relationships verifiable in Kevin's mail and the outreach working files as of the
build date. It is NOT the cold-outreach list; it is people Kevin has a real line to.
Job changes and "who now sits where" are only added when there is a real signal; none
are invented.

## How to grow it
Tell Claude in the working thread: a new contact, a job change, a correction to how a
connection really works, or a whole new sector. Claude edits the `PEOPLE` array near
the top of `storm-network-map.html` and republishes to the same artifact URL. Each
person is one object: name, org, sectors (first = primary colour), warmth, loc, mail,
how, net, note.

## To open it again
Ask Claude for the link, or find "Storm Network Map" in the artifacts gallery.

## Tracking positions and job changes
Each contact now carries a current role / where they work (shown as "Currently" on
their card) and, when they move, a "Recently moved" line. A move is one of the best
openings there is: the person already knows Kevin, now in a new seat, often a bigger
one. Example in the map: G. Schinkel moved Ambelt to OOZ; Sirelin left the Tartu
school and Evelin Lemetti took over.

How the watching works (be honest about this): Claude cannot read LinkedIn directly
(no connector, and the site blocks automated access). Instead, on each twice-weekly
engine run Claude scans Gmail for job-change signals, a new work domain, a changed
signature, a bounce from an old address, or a reply saying someone has left, updates
the map's role / org / moved fields, and flags any that look like an opening for Kevin
to confirm on LinkedIn himself. New contacts from the week are added the same way.

---
kicker: Brand & web
title: StormStudio Housestyle
subtitle: The design system for kevinstorm.eu and all StormStudio materials
doclabel: For Kevin & the web developer
---

## What this is

The single reference for the new StormStudio look, used on the PDFs, the product
landing page and the homepage redesign. Apply it across the whole website so
everything feels like one brand. Keep the workshop cards as they are in layout;
only bring their colours into this palette. Leave the "pip" and "plugins" areas
out of the restyle for now.

> [!key] Golden rule: forest green leads, copper is a small accent only, warm paper is the ground. No purple, no gradients-as-decoration, nothing shouty. Classy and calm.

## Colour palette

### Light (default)
| Token | Hex | Use |
|---|---|---|
| Ink | #1F2A30 | Text, dark feature blocks |
| Green | #2E6E4E | Primary accent, buttons, links, active |
| Green deep | #245A40 | Link text, button hover, dark-block CTA |
| Copper | #B5652E | Small accents only: eyebrows, rules, numbers |
| Paper | #FAF7F0 | Page background |
| Surface | #FFFFFF | Cards, panels |
| Muted | #5E6A6E | Secondary text |
| Rule | #E4DECF | Hairlines, borders |

### Dark (for theme-aware pages)
| Token | Hex |
|---|---|
| Ink (text) | #EDEAE1 |
| Green | #7FB896 |
| Green deep | #9CCBAF |
| Copper | #D89A63 |
| Paper (bg) | #161C1E |
| Surface | #1E2628 |
| Muted | #9AA6A4 |
| Rule | #2E3A3C |

Text on a green button uses white in light mode and a near-black (#12211B) in dark
mode, so it always stays legible.

## Typography

- **Display / headings:** Fraunces (a warm, editorial serif). Weights 600 and 900.
  Google Fonts. Fallback: Georgia, "Times New Roman", serif.
- **Body / UI / labels:** Libre Franklin (a clean, humanist sans). Weights 400-700.
  Fallback: -apple-system, "Segoe UI", sans-serif.
- **Eyebrows / labels:** Libre Franklin, uppercase, letter-spacing .14em, in copper.
- Body around 17px, line-height 1.6, running text max ~65 characters wide.

> [!tip] Headings get `text-wrap: balance`. Keep a clear type scale and stay on it; do not mix in extra fonts.

## Components

- **Buttons:** solid green (primary) with white/near-black text; "ghost" is a
  1px rule border with ink text. Radius 8px. Small lift on hover.
- **Cards:** white surface, 1px rule border, 14px radius, soft shadow. On hover,
  lift slightly and turn the border green. Keep the workshop-card layout; just
  apply these colours.
- **Eyebrow + rule:** a copper uppercase label above a short 54px copper rule,
  above the heading. This is the signature section opener.
- **Feature block:** ink background, paper text, green-deep CTA — for the one
  thing you want to stand out per page (e.g. the curriculum).
- **Hairlines:** use the rule token, never heavy borders. Let spacing separate
  things, not boxes.

## Do / don't

- Do lead with green; keep copper to eyebrows, thin rules and numbers.
- Do use plenty of warm-paper space; let the layout breathe.
- Do keep one accent per block; everything else quiet.
- Don't use purple, neon, or gradient hero backgrounds.
- Don't put a shadow and border and radius on every element — spend them by role.
- Don't add emoji as section markers.

## Applying it to the site

1. Set the colour tokens and the two fonts globally.
2. Restyle the header/nav, hero, section headings (eyebrow + rule pattern),
   buttons, and footer first — that carries 80% of the feel.
3. Recolour the workshop cards to the card style above; keep their layout.
4. Use the ink feature block once per page for the key call to action.
5. Leave "pip" and "plugins" as they are for now.
6. Reference implementations: the homepage redesign and the product landing page
   (both provided) are built exactly to this system — copy their CSS tokens.

> [!note] The PDFs use the same palette with Liberation Serif/Sans (print-safe stand-ins for Fraunces/Libre Franklin). Everything already matches; this guide just makes it repeatable on the web.

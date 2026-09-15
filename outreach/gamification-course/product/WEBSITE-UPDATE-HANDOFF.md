# Task: add a "Courses" section with buy buttons to the curriculum page

You are working on Kevin Storm's **stormstudio** static website (the local source
folder that deploys to the Netlify project `stormstudio`, live at
stormstudio.netlify.app). It is a small static site: `index.html`,
`curriculum.html`, `workshops.html`, `over-mij.html`, `hero-in-de-klas.html`,
plus a few assets and a `_redirects` / `netlify.toml`.

## What to do

Add the self-contained HTML block below into **`curriculum.html`**, inside the
main content area, at the point where the courses/shop should appear (a good spot
is after the page's intro/hero and before the footer). Do **not** change any other
page or asset. Do **not** restyle the rest of the site.

The block is fully scoped to `#stormstudio-courses`, so its CSS will not leak into
or clash with the existing page styles. Paste it as-is.

After inserting it, **deploy the site**:
- If the folder is connected to Git and Netlify auto-deploys, commit and push.
- Otherwise deploy the whole folder to the existing Netlify project named
  `stormstudio` (do not create a new site). A drag-and-drop deploy of the folder,
  or `netlify deploy --prod --dir=<the site folder>`, both work.

Then show Kevin the live URL so he can confirm.

## Verify the buttons before you finish

Each button links to `https://stormintheclass.gumroad.com/l/<permalink>`. Open
Kevin's Gumroad store and confirm each product's real URL matches the `href`
below. If Gumroad assigned a different slug to any product, update that one `href`.
The six expected permalinks are:

- Complete Course -> `gamification-course`
- Full Bundle -> `immersive-educator-bundle`
- AI in Education -> `ai-in-education`
- Game Design with Delightex -> `game-design-delightex`
- Inclusive Gamification -> `inclusive-gamification`
- The 6 Levers (free) -> `six-levers`

## The block to paste into curriculum.html

```html
<!-- StormStudio · Courses section (scoped to #stormstudio-courses) -->
<section id="stormstudio-courses">
  <style>
    #stormstudio-courses{
      --ink:#1F2A30; --green:#2E6E4E; --green-deep:#245A40; --copper:#B5652E;
      --paper:#FAF7F0; --surface:#FFFFFF; --muted:#5E6A6E; --rule:#E4DECF;
      --on-green:#ffffff;
      --serif:"Fraunces",Georgia,"Times New Roman",serif;
      --sans:"Libre Franklin",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
      background:var(--paper); color:var(--ink); font-family:var(--sans);
      padding:56px 0; line-height:1.6;
    }
    @media (prefers-color-scheme:dark){
      #stormstudio-courses{
        --ink:#EDEAE1; --green:#7FB896; --green-deep:#9CCBAF; --copper:#D89A63;
        --paper:#161C1E; --surface:#1E2628; --muted:#9AA6A4; --rule:#2E3A3C;
        --on-green:#12211b;
      }
    }
    #stormstudio-courses *{box-sizing:border-box}
    #stormstudio-courses .ss-wrap{max-width:1120px;margin:0 auto;padding-inline:24px}
    #stormstudio-courses .ss-eyebrow{font-weight:600;font-size:.74rem;letter-spacing:.14em;
      text-transform:uppercase;color:var(--copper)}
    #stormstudio-courses h2{font-family:var(--serif);font-weight:600;line-height:1.1;
      font-size:clamp(1.8rem,3.5vw,2.5rem);margin:10px 0 0}
    #stormstudio-courses .ss-lede{color:var(--muted);margin:14px 0 34px;max-width:62ch}
    #stormstudio-courses .ss-cards{display:grid;
      grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px}
    #stormstudio-courses .ss-card{background:var(--surface);border:1px solid var(--rule);
      border-radius:14px;padding:26px;display:flex;flex-direction:column;
      box-shadow:0 1px 2px rgba(31,42,48,.05),0 8px 28px rgba(31,42,48,.07)}
    #stormstudio-courses .ss-card.ss-flag{border-color:var(--green);border-width:1.5px}
    #stormstudio-courses .ss-card.ss-best{border-color:var(--copper);border-width:1.5px}
    #stormstudio-courses .ss-tag{font-size:.72rem;font-weight:600;letter-spacing:.1em;
      text-transform:uppercase;color:var(--copper);margin-bottom:12px}
    #stormstudio-courses .ss-card.ss-flag .ss-tag{color:var(--green)}
    #stormstudio-courses .ss-card h3{font-family:var(--serif);font-weight:600;font-size:1.35rem;
      margin:0 0 6px}
    #stormstudio-courses .ss-who{font-size:.92rem;color:var(--muted);margin-bottom:16px}
    #stormstudio-courses .ss-price{font-family:var(--serif);font-weight:600;font-size:1.15rem;
      margin:auto 0 16px}
    #stormstudio-courses .ss-price small{display:block;font-family:var(--sans);font-weight:400;
      font-size:.82rem;color:var(--muted);margin-top:3px}
    #stormstudio-courses .ss-btn{display:inline-block;text-align:center;font-weight:600;
      font-size:.96rem;padding:12px 22px;border-radius:8px;text-decoration:none;
      transition:transform .12s ease}
    #stormstudio-courses .ss-btn:hover{transform:translateY(-1px)}
    #stormstudio-courses .ss-btn-primary{background:var(--green);color:var(--on-green)}
    #stormstudio-courses .ss-btn-copper{background:var(--copper);color:#fff}
    #stormstudio-courses .ss-btn-ghost{background:transparent;color:var(--ink);
      border:1px solid var(--rule)}
    #stormstudio-courses .ss-free{background:transparent;border-style:dashed}
  </style>

  <div class="ss-wrap">
    <span class="ss-eyebrow">The courses</span>
    <h2>Gamification &amp; Immersive Learning, ready to download</h2>
    <p class="ss-lede">Buy the complete two-day course, start with a single mini-course,
      or take everything in one bundle. Each one is delivered in English and Dutch, and
      every teacher leaves with a real, playable lesson that works for every learner.</p>

    <div class="ss-cards">

      <div class="ss-card ss-flag">
        <div class="ss-tag">Flagship</div>
        <h3>Complete Course</h3>
        <div class="ss-who">The full two-day gamification &amp; immersive learning course.</div>
        <div class="ss-price">From &euro;149<small>School licence &euro;549 &middot; live delivery on request</small></div>
        <a class="ss-btn ss-btn-primary" target="_blank" rel="noopener"
           href="https://stormintheclass.gumroad.com/l/gamification-course">Get the course</a>
      </div>

      <div class="ss-card ss-best">
        <div class="ss-tag">Best value</div>
        <h3>Full Bundle</h3>
        <div class="ss-who">The complete course plus all three mini-courses.</div>
        <div class="ss-price">From &euro;199<small>School licence &euro;749</small></div>
        <a class="ss-btn ss-btn-copper" target="_blank" rel="noopener"
           href="https://stormintheclass.gumroad.com/l/immersive-educator-bundle">Get everything</a>
      </div>

      <div class="ss-card">
        <div class="ss-tag">Mini-course</div>
        <h3>AI in Education</h3>
        <div class="ss-who">Plan, differentiate and produce material in minutes, and teach AI literacy honestly.</div>
        <div class="ss-price">&euro;59<small>School licence &euro;249</small></div>
        <a class="ss-btn ss-btn-primary" target="_blank" rel="noopener"
           href="https://stormintheclass.gumroad.com/l/ai-in-education">Get this module</a>
      </div>

      <div class="ss-card">
        <div class="ss-tag">Mini-course</div>
        <h3>Game Design with Delightex</h3>
        <div class="ss-who">Build 3D worlds, code them with CoBlocks, step inside in AR/VR.</div>
        <div class="ss-price">&euro;59<small>School licence &euro;249</small></div>
        <a class="ss-btn ss-btn-primary" target="_blank" rel="noopener"
           href="https://stormintheclass.gumroad.com/l/game-design-delightex">Get this module</a>
      </div>

      <div class="ss-card">
        <div class="ss-tag">Mini-course</div>
        <h3>Inclusive Gamification</h3>
        <div class="ss-who">Game-based learning that works for special-needs and mixed-ability groups.</div>
        <div class="ss-price">&euro;59<small>School licence &euro;249</small></div>
        <a class="ss-btn ss-btn-primary" target="_blank" rel="noopener"
           href="https://stormintheclass.gumroad.com/l/inclusive-gamification">Get this module</a>
      </div>

      <div class="ss-card ss-free">
        <div class="ss-tag">Free</div>
        <h3>The 6 Levers of Engagement</h3>
        <div class="ss-who">A free one-page field guide to gamify any lesson, without the gimmicks.</div>
        <div class="ss-price">Free<small>A taste of the full course</small></div>
        <a class="ss-btn ss-btn-ghost" target="_blank" rel="noopener"
           href="https://stormintheclass.gumroad.com/l/six-levers">Download free</a>
      </div>

    </div>
  </div>
</section>
```

## Notes

- Keep the site's own header/nav and footer intact; only insert this section into
  the body of `curriculum.html`.
- The section already matches Kevin's brand (deep green, copper, warm paper;
  Fraunces + Libre Franklin). Do not add purple or gradients.
- If the existing page already links those Google Fonts, the section will use them;
  if not, it falls back cleanly to system fonts. You may optionally add the font
  link to the page `<head>`, but it is not required.
- Optional nicety: for an on-site pop-up checkout instead of opening Gumroad in a
  new tab, add `<script src="https://gumroad.com/js/gumroad.js"></script>` once and
  add `class="gumroad-button"` to each anchor (and remove `target="_blank"`).

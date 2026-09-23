# NASSCC 2027 website

Public site for the North American Solid State Chemistry Conference 2027, Duquesne University,
Pittsburgh, July 25 to 28, 2027. Domain: nasscc.com (Cloudflare Registrar, Juan Chamorro's
account). Organizing record and fact sources: `Work/CMU/Service/NASSCC-2027/` in the vault.

No frameworks, no dependencies, no CI: edit `build.py`, run `python3 build.py`, commit.
GitHub Pages serves `docs/` directly.

## Layout

```
build.py            all page content, styling, and the build (Python standard library only)
img/site/           the home page photograph
img/speakers/       speaker portraits, <slug>.jpg, square crop, about 400 px
img/organizers/     organizer portraits, <slug>.jpg
docs/               BUILD OUTPUT, committed, served by GitHub Pages (CNAME and .nojekyll included)
```

Nothing in `docs/` is edited by hand. `build.py` deletes and regenerates it.

## Editing

- A new speaker: add a tuple to `SPEAKERS` (name, title, department or empty, institution, theme
  code, website or empty, photo slug). Only firm acceptances go in. Re-read Jen Aitken's sheet
  "NASSC Invited speaker list for google docs" before each publish.
- A photo: drop `img/speakers/<slug>.jpg` and rebuild. A card with no photo shows a grey box.
- Opening (keynote) speakers: `OPENING`. Organizers: `ORGANIZERS`. History: `HISTORY`, `LINEAGE`.
- Any "To be announced" is the `TBA` constant; replace it with the fact once settled.
- Design: white page, Helvetica, black rules, one muted gold for links. No cards, gradients,
  buttons, or icons. Keep it that way.

Preview: `python3 -m http.server 8000 --directory docs` then http://localhost:8000.

## Publishing (GitHub Pages plus Cloudflare DNS)

Done 2026-09-23: repository `jrchamorro-cmu/nasscc-2027`, Pages from `main` and `/docs`, custom domain nasscc.com, DNS records at Cloudflare. To publish a change: edit, `python3 build.py`, commit, `git push`. The steps below are the record of the setup.

1. Create the GitHub repository `nasscc-2027` (public) and push `main`.
2. Repository Settings, Pages: deploy from branch `main`, folder `/docs`. The custom domain
   `nasscc.com` is written by the build into `docs/CNAME`; enter it in the same screen.
3. Cloudflare dashboard, nasscc.com, DNS: add `CNAME nasscc.com -> <github-user>.github.io`
   (Cloudflare flattens the apex CNAME) and `CNAME www -> <github-user>.github.io`, both DNS
   only (grey cloud) so GitHub can issue the certificate. Add the
   `_github-pages-challenge-<github-user>` TXT record that GitHub shows under Pages, Custom
   domain, Verify. Never delete that TXT record: without it another Pages account can claim
   the name.
4. Once the certificate is issued, turn on Enforce HTTPS.

Handoff in 2029: transfer this repository and push the domain to the next host's Cloudflare
account. See the vault hub `Service/NASSCC-2027/NASSCC-2027.md`.

## Photo credit

`img/site/pittsburgh.jpg`: "Downtown Pittsburgh from Duquesne Incline in the morning" by Dllu,
Wikimedia Commons, CC BY-SA 4.0, resized to 1600 px. The caption on the home page carries the
credit and the license link, which the license requires.

# safranapp.com

Single-page marketing site (`index.html`, EN/NL toggle, client-side routes
`/`, `/privacy`, `/terms`, `/r/<token>` for shared recipes).

## Build & preview

```bash
bash build.sh        # -> dist/ (Tailwind CSS + static /privacy, /terms, 404)
npx serve dist       # asset paths are absolute: preview over http, not file://
```

## Deploy (GitHub Pages)

This folder is its own repository. `.github/workflows/pages.yml` builds and
deploys `dist/` on every push to `main`. One-time setup in that repo:

1. Settings → Pages → **Source: GitHub Actions**.
2. Settings → Pages → **Custom domain: www.safranapp.com** → Save, tick
   **Enforce HTTPS** once the certificate is issued (a few minutes).
3. DNS at your registrar:
   - `www` → CNAME → `safranapp.github.io`
   - apex `safranapp.com` → A records `185.199.108.153`, `185.199.109.153`,
     `185.199.110.153`, `185.199.111.153` (redirects to www)

## Content that lives elsewhere

- Privacy/terms text: copied from the app repo, `app/src/i18n/locales/{en,nl}.json`
  (`privacy.*`, `terms.*`). When the app text changes, re-sync (see git log
  for the one-off Python snippet) so the site and the app never disagree.
- Phone screens in "What you can do": drawn in HTML by the `SCREENS` array in
  `index.html` (texts under `screens` per language), so there are no
  captures to redo after an app release. Update them when a screen changes.
- Coach figures: `assets/coach-<id>.webp` (cards) and `coach-<id>-sm.webp`
  (in the phone screens), resized from the app's `assets/coaches/<id>/wave.png`.
  Names, roles and quotes are copied from the app (`funnel.coach.*`).
- Email header: `assets/email-header.png`, regenerate with
  `python3 scripts/email/render-header.py` from the app repo.
- App Store link + support address: `APP_STORE_URL` / `SUPPORT_EMAIL`
  constants near the top of the script block.

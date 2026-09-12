#!/usr/bin/env bash
# Build the static site into site/dist for GitHub Pages.
#
#   bash site/build.sh            # -> site/dist
#   npx serve site/dist           # local preview (paths are absolute, so
#                                 #    open via http, not file://)
#
# GitHub Pages has no rewrites: /privacy and /terms are real directories
# holding a copy of index.html (the client router reads the pathname), and
# 404.html is the same page so /r/<token> share links still render.
set -euo pipefail
cd "$(dirname "$0")"

rm -rf dist
mkdir -p dist/privacy dist/terms dist/assets

# Tailwind: one minified stylesheet from the classes used in index.html.
npx --yes tailwindcss@3 -c tailwind.config.js -i src/tailwind.css -o dist/assets/site.css --minify

# Stamp a build id into asset URLs so browsers never reuse a stale copy.
BUILD_ID="$(date -u +%Y%m%d%H%M%S)"
sed "s/__BUILD_ID__/${BUILD_ID}/g; s#/assets/site.css#/assets/site.css?v=${BUILD_ID}#g" index.html > dist/index.html
cp dist/index.html dist/privacy/index.html
cp dist/index.html dist/terms/index.html
cp dist/index.html dist/404.html
cp -R assets/. dist/assets/
cp robots.txt sitemap.xml CNAME dist/
touch dist/.nojekyll   # keep Pages from ignoring files/dirs starting with _

echo "built -> site/dist ($(du -sh dist | cut -f1))"

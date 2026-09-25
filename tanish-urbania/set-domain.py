#!/usr/bin/env python3
"""Change the site domain everywhere (canonicals, Open Graph, JSON-LD, sitemap, robots).
Usage: python3 set-domain.py https://new-domain.com
The current domain is read from the Sitemap line in robots.txt."""
import sys, glob, re
if len(sys.argv) != 2 or not sys.argv[1].startswith("http"):
    sys.exit("Usage: python3 set-domain.py https://new-domain.com")
new = sys.argv[1].rstrip("/")
old = re.search(r"Sitemap:\s*(https?://[^/\s]+)", open("robots.txt").read()).group(1)
n = 0
for f in glob.glob("**/*", recursive=True):
    if f.endswith((".html", ".xml", ".txt", ".webmanifest")):
        s = open(f, encoding="utf-8").read()
        if old in s:
            open(f, "w", encoding="utf-8").write(s.replace(old, new)); n += 1
print(f"Updated {n} files: {old} -> {new}")

#!/usr/bin/env python3
"""Render the LaTeX in index.latex.html into static MathJax SVG in index.html.

The deployed page then has no JavaScript dependency for formulas.
Requires google-chrome (headless) and the local MathJax bundle.
"""
import re
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SOURCE = HERE / "index.latex.html"
OUTPUT = HERE / "index.html"
TMP = HERE / "_math_render.html"

chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
if not chrome:
    raise SystemExit("google-chrome not found")

if not SOURCE.exists():
    raise SystemExit(f"missing source: {SOURCE}")
html = SOURCE.read_text(encoding="utf-8")
TMP.write_text(html, encoding="utf-8")
try:
    proc = subprocess.run(
        [chrome, "--headless=new", "--no-sandbox", "--disable-gpu",
         "--virtual-time-budget=12000", "--dump-dom", f"file://{TMP.resolve()}"],
        capture_output=True, text=True, timeout=120, check=True,
    )
finally:
    TMP.unlink(missing_ok=True)

dom = proc.stdout
blocks = re.findall(r'<div class="math">(.*?)</div>', dom, re.S)
blocks = [re.sub(r'<mjx-assistive-mml.*?</mjx-assistive-mml>', '', b, flags=re.S) for b in blocks]
# Keep display/centering/responsiveness even if the old CSS is cached.
blocks = [b.replace('style="position: relative;"',
                    'style="position: relative;display:block;text-align:center;margin:0.8rem 0;"')
          .replace('style="vertical-align:', 'style="max-width:100%;height:auto;vertical-align:')
          for b in blocks]
cache = re.search(r'<svg id="MJX-SVG-global-cache".*?</svg>', dom, re.S)
if len(blocks) != 8 or cache is None:
    raise SystemExit(f"unexpected math render: blocks={len(blocks)} cache={cache is not None}")

it = iter(blocks)
static = re.sub(r'<div class="math">.*?</div>',
                lambda m: '<div class="math">' + next(it) + '</div>',
                html, flags=re.S)
# Remove the runtime MathJax config and bundle; formulas are now static.
static = re.sub(r'<script>\s*window\.MathJax = \{.*?</script>\s*', '', static, count=1, flags=re.S)
static = static.replace('  <script src="assets/mathjax/tex-svg.js"></script>\n', '')
static = static.replace('  <script src="assets/mathjax/tex-svg.js"></script>', '')
static = static.replace('<body>', '<body>\n' + cache.group(0), 1)
static = static.replace(
    '公式由本地 MathJax 渲染；无外部依赖，可直接用浏览器打开。',
    '公式为预渲染 SVG，无脚本依赖。',
)
OUTPUT.write_text(static, encoding="utf-8")
print(f"wrote {OUTPUT} ({len(static)} bytes, {len(blocks)} equations)")

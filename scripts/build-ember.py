#!/usr/bin/env python3
"""Derive an independent color variant from the current, fixed Asuka theme."""
from pathlib import Path
import json
import shutil
import subprocess
from ember_palette import transform

root = Path(__file__).resolve().parents[1]
components = ['aurorae/AsukaRounded', 'plasma/desktoptheme/Asuka',
              'plasma/look-and-feel/com.omen.asuka', 'wallpapers/Asuka']
for relative in components:
    source = root / relative
    for p in source.rglob('*'):
        if not p.is_file() or p.suffix.lower() in ('.png','.jpg'):
            continue
        target = root / transform(str(p.relative_to(root)))
        target.parent.mkdir(parents=True, exist_ok=True)
        text = p.read_text()
        target.write_text(text if p.name == 'COPYING' else transform(text))
    dest = root / transform(relative) / 'metadata.json'
    meta = json.loads(dest.read_text())
    meta['KPlugin']['Description'] = 'Asuka Ember: image-inspired oxblood, vermilion, copper and teal'
    dest.write_text(json.dumps(meta,ensure_ascii=False,indent=4)+'\n')

for relative in ['Asuka.colors','color-schemes/Asuka.colors', 'konsole/Asuka.colorscheme','wallpapers/Asuka-source.svg']:
    p = root / transform(relative)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(transform((root/relative).read_text()))
for width,height in [(1920,1080),(2560,1440),(3840,2160)]:
    dest = root / f'wallpapers/AsukaEmber/contents/images/{width}x{height}.png'
    dest.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['rsvg-convert','-w',str(width),'-h',str(height),'-o',str(dest),str(root/'wallpapers/AsukaEmber-source.svg')],check=True)
print('Built AsukaEmber independently; original Asuka preserved.')

#!/usr/bin/env python3
"""Validate Ember contrast, unchanged frame geometry and variant isolation."""
from pathlib import Path
import configparser
import os
import subprocess
import tempfile
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
def ini(p):
    c = configparser.ConfigParser(interpolation=None)
    c.optionxform = str
    c.read(p)
    return c

original = root/'aurorae/AsukaRounded'
variant = root/'aurorae/AsukaEmberRounded'
assert ini(original/'AsukaRoundedrc')['Layout'] == ini(variant/'AsukaEmberRoundedrc')['Layout']
before, after = [ET.parse(p/'decoration.svg').getroot() for p in [original,variant]]
assert len(list(before.iter())) == len(list(after.iter()))
for a,b in zip(before.iter(),after.iter()):
    assert a.tag == b.tag
    for key,value in a.attrib.items():
        if key not in ('style','fill','stroke'):
            assert b.get(key) == value, (a.get('id'),key)

def lum(text):
    values = [int(v)/255 for v in text.split(',')]
    return sum((v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4)*w for v,w in zip(values,[.2126,.7152,.0722]))
colors = ini(root/'AsukaEmber.colors')
ratios = []
for section in colors.sections():
    if section.startswith('Colors:'):
        for bg in ('BackgroundNormal','BackgroundAlternate'):
            for fg in ('ForegroundNormal','ForegroundInactive','ForegroundLink','ForegroundNegative','ForegroundNeutral','ForegroundPositive'):
                a,b = sorted((lum(colors[section][bg]),lum(colors[section][fg])))
                ratios.append((b+.05)/(a+.05))
assert min(ratios) >= 4.5, min(ratios)
for p in ['color-schemes/AsukaEmber.colors','plasma/desktoptheme/AsukaEmber/colors']:
    assert (root/p).read_bytes() == (root/'AsukaEmber.colors').read_bytes()
with tempfile.TemporaryDirectory(prefix='ember-check-') as d:
    data = Path(d)/'data with spaces'
    env = dict(os.environ,XDG_DATA_HOME=str(data),QT_QPA_PLATFORM='offscreen')
    for name in ['Asuka','AsukaEmber','AsukaEmber']:
        subprocess.run(['bash',str(root/'install.sh'),name],check=True,env=env,stdout=subprocess.DEVNULL)
    defaults = ini(data/'plasma/look-and-feel/com.omen.asukaember/contents/defaults')
    assert defaults['kwinrc][org.kde.kdecoration2']['theme'] == '__aurorae__svg__AsukaEmberRounded'
    for kind,p in [('KWin/Aurorae','aurorae/themes/AsukaEmberRounded'),('Plasma/Theme','plasma/desktoptheme/AsukaEmber'),('Plasma/LookAndFeel','plasma/look-and-feel/com.omen.asukaember'),('Wallpaper/Images','wallpapers/AsukaEmber')]:
        subprocess.run(['kpackagetool6','--type',kind,'--show',str(data/p)],env=env,check=True,stdout=subprocess.DEVNULL)
    subprocess.run(['bash',str(root/'uninstall.sh'),'AsukaEmber'],env=env,check=True,stdout=subprocess.DEVNULL)
    assert not list(data.rglob('*AsukaEmber*'))
    assert not (data/'plasma/look-and-feel/com.omen.asukaember').exists()
    assert (data/'aurorae/themes/AsukaRounded/decoration.svg').read_bytes() == (original/'decoration.svg').read_bytes()
print(f'PASS: geometry/padding unchanged; minimum text contrast {min(ratios):.2f}:1; KDE metadata, repeated install and isolated uninstall.')

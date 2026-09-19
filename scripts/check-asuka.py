#!/usr/bin/env python3
"""Validate cross-component references, contrast and isolated install/uninstall."""
import configparser
import json
import os
from pathlib import Path
import subprocess
import tempfile
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
def ini(path):
    c = configparser.ConfigParser(interpolation=None)
    c.optionxform = str
    c.read(path)
    return c

def luminance(rgb):
    channels = [int(v) / 255 for v in rgb.split(',')]
    channels = [v / 12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in channels]
    return sum(v*w for v,w in zip(channels, [.2126,.7152,.0722]))

layout = ini(root / 'aurorae/AsukaRounded/AsukaRoundedrc')['Layout']
reference = ini(root / 'sources/Nothing/Nothingrc')['Layout']
for key in ['PaddingTop', 'PaddingBottom', 'PaddingLeft', 'PaddingRight']:
    assert layout[key] == reference[key], ('shadow padding mismatch', key)
frame_ids = {e.get('id') for e in ET.parse(root / 'aurorae/AsukaRounded/decoration.svg').iter()}
for side in ['center','top','bottom','left','right','topleft','topright','bottomleft','bottomright']:
    assert 'mask-' + side in frame_ids, ('missing corner mask', side)

colors = ini(root / 'Asuka.colors')
for path in ['color-schemes/Asuka.colors', 'plasma/desktoptheme/Asuka/colors']:
    assert (root / path).read_bytes() == (root / 'Asuka.colors').read_bytes()
minimum = 100
for section in colors.sections():
    if not section.startswith('Colors:'):
        continue
    for background in ['BackgroundNormal', 'BackgroundAlternate']:
        for key in ['ForegroundNormal', 'ForegroundInactive', 'ForegroundLink', 'ForegroundNegative', 'ForegroundNeutral', 'ForegroundPositive']:
            a, b = sorted([luminance(colors[section][key]), luminance(colors[section][background])])
            ratio = (b+.05)/(a+.05)
            assert ratio >= 4.5, (section, key, background, ratio)
            minimum = min(minimum, ratio)
print(f'Text contrast: minimum {minimum:.2f}:1 across checked semantic roles.')
for base in ['aurorae/AsukaRounded', 'plasma/desktoptheme/Asuka']:
    for path in (root / base).rglob('*.svg'):
        elements = ET.parse(path).getroot()
        ids = [e.get('id') for e in elements.iter() if e.get('id')]
        assert len(ids) == len(set(ids)), path
        if base.startswith('aurorae') and path.stem != 'decoration':
            for state in ['active','inactive','hover','pressed','hover-inactive','pressed-inactive','deactivated','deactivated-inactive']:
                assert state+'-center' in ids, (path, state)
        elif path.stem == 'decoration':
            for prefix in ['decoration', 'decoration-inactive']:
                for side in ['center','top','bottom','left','right','topleft','topright','bottomleft','bottomright']:
                    assert f'{prefix}-{side}' in ids
            assert 'decoration-maximized-center' in ids
            assert 'decoration-maximized-inactive-center' in ids

with tempfile.TemporaryDirectory(prefix='asuka-check-') as temp:
    data = Path(temp) / 'data with spaces'
    env = dict(os.environ, XDG_DATA_HOME=str(data), QT_QPA_PLATFORM='offscreen')
    for script, args in [('install.sh',['OmenDark']), ('install.sh',[]), ('install.sh',[])]:
        subprocess.run(['bash', str(root/script), *args], env=env, check=True, stdout=subprocess.DEVNULL)
    defaults = ini(data / 'plasma/look-and-feel/com.omen.asuka/contents/defaults')
    assert defaults['kdeglobals][General']['ColorScheme'] == 'Asuka'
    assert defaults['kwinrc][org.kde.kdecoration2']['theme'] == '__aurorae__svg__AsukaRounded'
    for kind, base, name in [('Plasma/LookAndFeel','plasma/look-and-feel','com.omen.asuka'),
                             ('Plasma/Theme','plasma/desktoptheme','Asuka'),
                             ('KWin/Aurorae','aurorae/themes','AsukaRounded'),
                             ('Wallpaper/Images','wallpapers','Asuka')]:
        # Wallpaper/Images has no default package root: use the absolute package path.
        subprocess.run(['kpackagetool6','--type',kind,'--show',str(data/base/name)], env=env, check=True)
    for base in ['aurorae/themes/AsukaRounded', 'plasma/desktoptheme/Asuka', 'plasma/look-and-feel/com.omen.asuka', 'wallpapers/Asuka']:
        json.loads((data / base / 'metadata.json').read_text())
    assert (data / 'aurorae/themes/AsukaRounded/AsukaRoundedrc').is_file()
    assert (data / 'wallpapers/Asuka/contents/images/3840x2160.png').is_file()
    subprocess.run(['bash',str(root/'uninstall.sh')], env=env, check=True, stdout=subprocess.DEVNULL)
    assert not list(data.rglob('*Asuka*'))
    assert not (data/'plasma/look-and-feel/com.omen.asuka').exists()
    assert (data/'color-schemes/OmenDark.colors').exists()
    assert (data/'aurorae/themes/OmenDark/OmenDarkrc').exists()
    for script in ['install.sh','uninstall.sh']:
        result = subprocess.run(['bash',str(root/script),'../bad'], env=env, capture_output=True)
        assert result.returncode == 2
print('Passed SVG states, metadata, KDE package discovery, repeat install, isolated uninstall and variant checks.')

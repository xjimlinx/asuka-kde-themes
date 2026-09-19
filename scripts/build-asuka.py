#!/usr/bin/env python3
"""Build the Asuka variant from the original OMEN assets; requires librsvg + Pillow."""
from pathlib import Path
import configparser
import json
import xml.etree.ElementTree as ET
import subprocess

ROOT = Path(__file__).resolve().parents[1]
NAME = 'Asuka'
ID = 'com.omen.asuka'

def write(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(data, encoding='utf-8')

def rgb(h):
    return ','.join(str(int(h[i:i+2], 16)) for i in (1, 3, 5))

def read_ini(path):
    c = configparser.ConfigParser(interpolation=None)
    c.optionxform = str
    c.read(ROOT / path)
    return c

def save_ini(path, c):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w') as f:
        c.write(f, space_around_delimiters=False)
    p.write_text(p.read_text().rstrip() + "\n")

# Keep the existing semantic roles, with readable selection foregrounds.
c = read_ini('color-schemes/OmenDark.colors')
surfaces = {'Button': ('#302326', '#39292B'), 'Complementary': ('#21181B', '#2B1D21'),
            'Header': ('#261B1F', '#302125'), 'Header][Inactive': ('#1D191C', '#251F22'),
            'Selection': ('#B82E36', '#942831'), 'Tooltip': ('#302326', '#39292B'),
            'View': ('#151316', '#1E191D'), 'Window': ('#211A1E', '#291F23')}
foregrounds = {'Normal': '#F5EDE4', 'Inactive': '#B3A2A2', 'Active': '#FF8267',
               'Link': '#83BCE8', 'Visited': '#D6A0C8', 'Negative': '#FF8A85',
               'Neutral': '#F4BD70', 'Positive': '#91C99A'}
for role, (normal, alternate) in surfaces.items():
    s = c[f'Colors:{role}']
    s['BackgroundNormal'], s['BackgroundAlternate'] = rgb(normal), rgb(alternate)
    s['DecorationFocus'], s['DecorationHover'] = rgb('#F4BD70'), rgb('#FF8267')
    for key, color in foregrounds.items():
        s['Foreground' + key] = rgb('#FFF5E8' if role == 'Selection' else color)
c['General'].update(ColorScheme=NAME, Name='Asuka', **{'Name[zh_CN]': '明日香 · 二号机'})
c['WM'].update(activeBackground=rgb('#261B1F'), activeForeground=rgb('#F5EDE4'),
               activeBlend=rgb('#F5EDE4'), inactiveBackground=rgb('#1D191C'),
               inactiveForeground=rgb('#B3A2A2'), inactiveBlend=rgb('#B3A2A2'))
for dest in ['color-schemes/Asuka.colors', 'Asuka.colors', 'plasma/desktoptheme/Asuka/colors']:
    save_ini(dest, c)

for source, dest, description in [
    ('aurorae/OmenDark', 'aurorae/AsukaRounded', 'Asuka window decoration: circular window controls, subtle rounded corners and scarlet accent'),
    ('plasma/desktoptheme/OmenDark', 'plasma/desktoptheme/Asuka', 'Asuka warm dark Plasma style'),
    ('plasma/look-and-feel/com.omen.dark', 'plasma/look-and-feel/com.omen.asuka', 'Asuka / Unit 02: warm dark surfaces, scarlet and amber'),
    ('wallpapers/OmenDark', 'wallpapers/Asuka', 'Asuka / Unit 02 geometric wallpaper')]:
    meta = json.loads((ROOT / source / 'metadata.json').read_text())
    meta['KPlugin'].update(Name=NAME, Id=ID if 'look-and-feel' in dest else NAME,
                          Description=description, Version='1.0.0', **{'Name[zh_CN]': '明日香 · 二号机'})
    if dest == 'wallpapers/Asuka':
        meta['KPackageStructure'] = 'Wallpaper/Images'
        meta['X-KDE-PlasmaImageWallpaper-AccentColor'] = '#D9443F'
    elif dest == 'aurorae/AsukaRounded':
        meta['KPackageStructure'] = 'KWin/Aurorae'
        meta['KPlugin']['Id'] = 'AsukaRounded'
        meta['KPlugin']['Authors'].append({'Name': 'jomada', 'Task': 'Original Nothing window frame and shadows'})
    elif dest == 'plasma/desktoptheme/Asuka':
        meta['KPackageStructure'] = 'Plasma/Theme'
    write(dest + '/metadata.json', json.dumps(meta, ensure_ascii=False, indent=4) + '\n')

write('aurorae/AsukaRounded/metadata.desktop', (ROOT / 'aurorae/OmenDark/metadata.desktop').read_text()
      .replace('OmenDark', NAME).replace('X-KDE-PluginInfo-Name=Asuka', 'X-KDE-PluginInfo-Name=AsukaRounded').replace('OMEN Dark window decoration with red accent', 'Asuka / Unit 02 window decoration')
      .replace('OMEN 深色窗口装饰（红色强调）', '明日香窗口装饰（圆形按钮、小圆角与朱红点缀）'))
rc = read_ini('aurorae/OmenDark/OmenDarkrc')
rc['General'].update(ActiveTextColor=rgb('#F5EDE4'), InactiveTextColor=rgb('#B3A2A2'),
                     TitleAlignment='Left', LeftButtons='M', RightButtons='IAX', UseTextShadow='false', Animation='140')
rc['Layout'].update(ButtonWidth='26', ButtonHeight='26', ButtonMarginTop='5',
                    BorderBottom='7', PaddingTop='35', PaddingBottom='90', PaddingLeft='76', PaddingRight='76', TitleHeight='36', TitleEdgeTop='2', TitleBorderLeft='12', TitleBorderRight='12')
rc['Layout'].pop('ButtonMarginLeft', None)
save_ini('aurorae/AsukaRounded/AsukaRoundedrc', rc)

# Based on Nothing 1.2 by jomada (GPL-3.0); retain the complete, matched
# radial corner shadows, linear edges and mask, with the original padding.
# See sources/Nothing and THIRD_PARTY.md for provenance and modifications.
ns = 'http://www.w3.org/2000/svg'
ET.register_namespace('', ns)
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
frame = ET.fromstring((ROOT / 'sources/Nothing/decoration.svg').read_text())
for element in frame.iter():
    style = element.get('style')
    if style:
        element.set('style', style.replace('#1b1b1d', '#261B1F').replace('#111216', '#191417').replace('#202b30', '#695057'))
# Keep active and inactive window geometry identical, including corner radii.
for element in frame.iter():
    if element.get('id', '').startswith('decoration-inactive-'):
        for child in element.iter():
            if child.get('style'):
                child.set('style', child.get('style').replace('#261B1F', '#1D191C'))
for prefix, color in [('decoration-maximized', '#261B1F'), ('decoration-maximized-inactive', '#1D191C')]:
    ET.SubElement(frame, f'{{{ns}}}rect', id=prefix+'-center', width='100', height='70', fill=color)
write('aurorae/AsukaRounded/decoration.svg', ET.tostring(frame, encoding='unicode'))
write('aurorae/AsukaRounded/COPYING', (ROOT / 'sources/Nothing/COPYING').read_text())
write('aurorae/AsukaRounded/AUTHORS.md', (ROOT / 'THIRD_PARTY.md').read_text())

# Primary controls are solid circles; auxiliary controls retain their glyphs.
icons = {
    'close': 'M9 9L17 17M17 9L9 17', 'minimize': 'M8 15H18',
    'maximize': 'M8.5 8.5H17.5V17.5H8.5Z', 'restore': 'M8 11H15V18H8ZM11 8H18V15',
    'keepabove': 'M8 15L13 10L18 15M8 9H18', 'keepbelow': 'M8 11L13 16L18 11M8 18H18',
    'alldesktops': 'M13 6L20 13L13 20L6 13Z', 'shade': 'M8 16L13 11L18 16M7 7H19',
    'help': 'M10 10C10 6 17 6 17 10C17 13 13 12 13 15M13 18V18.2',
    'appmenu': 'M7 8H19M7 13H19M7 18H19'}
for name, path in icons.items():
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="104" height="52" viewBox="0 0 104 52">']
    for i, state in enumerate(['active', 'hover', 'pressed', 'inactive', 'hover-inactive', 'pressed-inactive', 'deactivated', 'deactivated-inactive']):
        bg, fg, ring = '#222223', '#F2F2EF', '#454547'
        if name == 'close':
            fg = '#EF7167'
        if state == 'inactive':
            bg, fg, ring = '#1B1B1C', '#A0A09F', '#333335'
        elif state.startswith('hover'):
            bg, fg = ('#D9443F', '#FFFFFF') if name == 'close' else ('#F2F2EF', '#181819')
            ring = bg
        elif state.startswith('pressed'):
            bg, fg = ('#A62932', '#FFFFFF') if name == 'close' else ('#BDBDBA', '#101011')
            ring = bg
        elif state.startswith('deactivated'):
            bg, fg, ring = '#181819', '#555557', '#272729'
        primary = name in ('close', 'minimize', 'maximize', 'restore')
        if primary:
            palette = {
                'minimize': ('#F4BD70', '#FFDA94', '#D99451', '#897052'),
                'maximize': ('#E6DED5', '#FFF5E8', '#B8ADA3', '#77716E'),
                'restore': ('#E6DED5', '#FFF5E8', '#B8ADA3', '#77716E'),
                'close': ('#D9443F', '#F16A5E', '#A62932', '#7D4545'),
            }[name]
            bg = palette[1] if state.startswith('hover') else palette[2] if state.startswith('pressed') else palette[3] if state == 'inactive' else '#403A3D' if state.startswith('deactivated') else palette[0]
        shape = f'<circle cx="13" cy="13" r="7" fill="{bg}"/>' if primary else f'<rect width="26" height="26" rx="5" fill="{bg}"/>'
        svg.append(f'<g id="{state}-center" transform="translate({i%4*26} {i//4*26})"><rect width="26" height="26" fill="#000000" fill-opacity="0"/>{shape}')
        if not primary:
            svg.append(f'<path d="{path}" fill="none" stroke="{fg}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
        svg.append('</g>')
    write(f'aurorae/AsukaRounded/{name}.svg', ''.join(svg) + '</svg>')

# Preserve Nothing's rounded nine-slice geometry, shadows and blur masks.
# Recolor surfaces only; corner alpha must stay intact for Plasma and Fcitx.
for asset in ['widgets/panel-background', 'widgets/background', 'widgets/tooltip', 'dialogs/background']:
    source = (ROOT / ('sources/NothingPlasma/' + asset + '.svg')).read_text()
    surface = '#211A1E' if 'panel' in asset else '#302326'
    source = source.replace('#1b1b1d', surface).replace('#26272a', '#302326')
    write('plasma/desktoptheme/Asuka/' + asset + '.svg', source)
    if asset == 'widgets/panel-background':
        write('plasma/desktoptheme/Asuka/solid/' + asset + '.svg', source)
write('plasma/desktoptheme/Asuka/AUTHORS.md', (ROOT / 'THIRD_PARTY.md').read_text())
write('plasma/desktoptheme/Asuka/plasmarc', '[Settings]\nFallbackTheme=default\n\n[Wallpaper]\ndefaultWallpaperTheme=Asuka\ndefaultFileSuffix=.png\ndefaultWidth=3840\ndefaultHeight=2160\n')
write('plasma/look-and-feel/com.omen.asuka/contents/defaults', '''[kdeglobals][KDE]
widgetStyle=Breeze

[kdeglobals][General]
ColorScheme=Asuka
AccentColor=217,68,63

[kwinrc][org.kde.kdecoration2]
library=org.kde.kwin.aurorae
theme=__aurorae__svg__AsukaRounded

[plasmarc][Theme]
name=Asuka

[Wallpaper]
Image=Asuka
''')

terminal = read_ini('konsole/OmenDark.colorscheme')
ansi = ['#45373D', '#EF7167', '#91C99A', '#F4BD70', '#83BCE8', '#D6A0C8', '#80C7C5', '#DED0C8',
        '#AC979C', '#FF9387', '#B2DEAC', '#FFDA94', '#AED8FA', '#ECC0DF', '#A3E1DB', '#FFF5E8']
for i, color in enumerate(ansi):
    for suffix in ['', 'Faint', 'Intense']:
        terminal[f'Color{i}{suffix}']['Color'] = rgb(color)
for suffix in ['', 'Faint', 'Intense']:
    terminal['Background' + suffix]['Color'] = rgb('#151316')
    terminal['Foreground' + suffix]['Color'] = rgb('#B3A2A2' if suffix == 'Faint' else '#F5EDE4')
terminal['General'].update(Description='Asuka', Opacity='1')
save_ini('konsole/Asuka.colorscheme', terminal)

# Original vector artwork: restrained desktop space on the left, Unit 02 armor on the right.
wallpaper = '''<svg xmlns="http://www.w3.org/2000/svg" width="3840" height="2160" viewBox="0 0 1920 1080">
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#211A1E"/><stop offset="1" stop-color="#100F13"/></linearGradient>
<linearGradient id="armor" x2="1" y2="1"><stop stop-color="#E65143"/><stop offset=".5" stop-color="#B82E36"/><stop offset="1" stop-color="#67212D"/></linearGradient>
<pattern id="grid" width="72" height="72" patternUnits="userSpaceOnUse"><path d="M72 0H0V72" fill="none" stroke="#F5EDE4" stroke-opacity=".025"/></pattern></defs>
<rect width="1920" height="1080" fill="url(#bg)"/><rect width="1920" height="1080" fill="url(#grid)"/>
<path d="M1390 -100H1840L1330 1180H880Z" fill="#361D26"/>
<path d="M1490 -100H1980L1470 1180H980Z" fill="url(#armor)"/>
<path d="M1490 -100H1510L1000 1180H980Z" fill="#FF8267"/>
<path d="M1760 -100H1806L1296 1180H1250Z" fill="#211A1E"/>
<path d="M1830 -100H1842L1332 1180H1320Z" fill="#F4BD70"/>
<path d="M1250 260L1310 110H1550L1490 260Z" fill="#211A1E"/>
<path d="M1293 228L1328 141H1360L1325 228Z" fill="#83BCE8"/>
<path d="M1345 228L1380 141H1412L1377 228Z" fill="#83BCE8"/>
<path d="M1397 228L1432 141H1464L1429 228Z" fill="#F4BD70"/>
<g font-family="DejaVu Sans, sans-serif" fill="#FFF5E8"><text x="1310" y="670" font-size="250" font-weight="bold" letter-spacing="-16">02</text>
<text x="1360" y="735" font-size="22" letter-spacing="8">ASUKA</text></g>
<path d="M1370 786H1680L1655 810H1370Z" fill="#211A1E"/>
<path d="M1382 793H1450V800H1382ZM1462 793H1530V800H1462ZM1542 793H1610V800H1542Z" fill="#F4BD70"/>
<path d="M100 160V100H160M1760 980H1820V920" fill="none" stroke="#A48679" stroke-width="2"/>
<g font-family="DejaVu Sans, sans-serif"><text x="104" y="912" fill="#F5EDE4" font-size="18" letter-spacing="6">ASUKA / UNIT 02</text>
<text x="104" y="944" fill="#AC979C" font-size="11" letter-spacing="3">SECOND CHILD · SCARLET EDITION</text></g>
<path d="M104 864H168" stroke="#D9443F" stroke-width="4"/><path d="M178 864H206" stroke="#F4BD70" stroke-width="4"/>
</svg>'''
write('wallpapers/Asuka-source.svg', wallpaper)
for width, height in [(1920,1080), (2560,1440), (3840,2160)]:
    dest = ROOT / f'wallpapers/Asuka/contents/images/{width}x{height}.png'
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['rsvg-convert', '-w', str(width), '-h', str(height), '-o', str(dest), str(ROOT/'wallpapers/Asuka-source.svg')], check=True)

print('Built Asuka colors, decoration, Plasma style, global theme, Konsole and wallpaper.')

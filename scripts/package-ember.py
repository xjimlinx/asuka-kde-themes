#!/usr/bin/env python3
from pathlib import Path
import io
import shutil
import tarfile
import zipfile

root = Path(__file__).resolve().parents[1]
dist = root/'dist'
dist.mkdir(exist_ok=True)
components = {'Aurorae':'aurorae/AsukaEmberRounded', 'PlasmaStyle':'plasma/desktoptheme/AsukaEmber',
              'GlobalTheme':'plasma/look-and-feel/com.omen.asukaember', 'Wallpaper':'wallpapers/AsukaEmber'}
for label,path in components.items():
    with zipfile.ZipFile(dist/f'AsukaEmber-{label}.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted((root/path).rglob('*')):
            if p.is_file(): z.write(p,p.relative_to((root/path).parent))
shutil.copyfile(root/'AsukaEmber.colors',dist/'AsukaEmber.colors')
with tarfile.open(dist/'AsukaEmber-KDE-Theme.tar.gz','w:gz') as tar:
    for path in [*components.values(),'color-schemes/AsukaEmber.colors','konsole/AsukaEmber.colorscheme',
                 'wallpapers/AsukaEmber-source.svg','previews/AsukaEmber-preview.png','THIRD_PARTY.md','LICENSE','sources/Nothing', 'sources/NothingPlasma']:
        tar.add(root/path,arcname='AsukaEmber-KDE-Theme/'+path)
    for source,name in [('install.sh','install.sh'),('uninstall.sh','uninstall.sh'),('README-EMBER.md','README.md')]:
        data = (root/source).read_text().replace('${1:-Asuka}','${1:-AsukaEmber}').encode()
        info = tarfile.TarInfo('AsukaEmber-KDE-Theme/'+name)
        info.size = len(data)
        info.mode = 0o755 if name.endswith('.sh') else 0o644
        tar.addfile(info,io.BytesIO(data))
print('Packaged AsukaEmber-KDE-Theme.tar.gz and component ZIPs.')

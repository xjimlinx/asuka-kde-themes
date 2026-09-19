#!/usr/bin/env python3
"""Package existing generated assets; run build and render first."""
from pathlib import Path
import shutil
import tarfile
import zipfile

root = Path(__file__).resolve().parents[1]
dist = root / 'dist'
dist.mkdir(exist_ok=True)
components = {
    'GlobalTheme': 'plasma/look-and-feel/com.omen.asuka',
    'Aurorae': 'aurorae/AsukaRounded',
    'PlasmaStyle': 'plasma/desktoptheme/Asuka',
    'Wallpaper': 'wallpapers/Asuka',
}
for label, relative in components.items():
    source = root / relative
    with zipfile.ZipFile(dist / f'Asuka-{label}.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(source.rglob('*')):
            if p.is_file():
                z.write(p, p.relative_to(source.parent))
shutil.copyfile(root / 'Asuka.colors', dist / 'Asuka.colors')
with tarfile.open(dist / 'Asuka-KDE-Theme.tar.gz', 'w:gz') as tar:
    for relative in [*components.values(), 'color-schemes/Asuka.colors',
                     'konsole/Asuka.colorscheme', 'wallpapers/Asuka-source.svg',
                     'previews/Asuka-preview.png', 'THIRD_PARTY.md', 'sources/Nothing', 'sources/NothingPlasma', 'install.sh', 'uninstall.sh', 'README.md', 'README-EMBER.md', 'README-OMEN.md', 'LICENSE']:
        tar.add(root / relative, arcname='Asuka-KDE-Theme/' + relative)
print('Packaged dist/Asuka-KDE-Theme.tar.gz and individual components.')

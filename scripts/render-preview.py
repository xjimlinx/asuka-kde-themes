#!/usr/bin/env python3
"""Render actual KDE FrameSvg assets offscreen, in a composed sample desktop."""
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
os.environ['QT_QUICK_BACKEND'] = 'software'
from pathlib import Path
from PySide6.QtCore import QUrl, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView
from PySide6.QtQml import QQmlComponent
from PIL import Image

root = Path(__file__).resolve().parents[1]
variant = os.environ.get('ASUKA_VARIANT', 'Asuka')
assert variant in ('Asuka', 'AsukaEmber')
from ember_palette import transform
variant_text = transform if variant == 'AsukaEmber' else lambda text: text
app = QGuiApplication([])
view = QQuickView()
qml = '''import QtQuick
import org.kde.ksvg 1.0 as KSvg
Rectangle {
 width: 1600; height: 1000; color: "#151316"
 Image { anchors.fill: parent; source: "ROOT/wallpapers/Asuka/contents/images/1920x1080.png"; fillMode: Image.PreserveAspectCrop }
 Text { x: 64; y: 45; text: "ASUKA"; color: "#F5EDE4"; font.pixelSize: 34; font.letterSpacing: 8 }
 Text { x: 66; y: 96; text: "UNIT 02  /  KDE PLASMA"; color: "#B3A2A2"; font.pixelSize: 13; font.letterSpacing: 3 }
 Item {
  x: 55; y: 155; width: 930; height: 610
  KSvg.FrameSvgItem { x: -52; y: -11; width: parent.width + 104; height: parent.height + 69; imagePath: "ROOT/aurorae/AsukaRounded/decoration.svg"; prefix: "decoration" }
  Text { x: 46; y: 34; text: "Files — Asuka"; color: "#F5EDE4"; font.pixelSize: 15 }
  Row { x: 784; y: 30; spacing: 6
   Repeater { model: ["minimize", "maximize", "close"]
    KSvg.SvgItem { width: 26; height: 26; imagePath: "ROOT/aurorae/AsukaRounded/" + modelData + ".svg"; elementId: "active-center" }
   }
  }
  Rectangle { x: 26; y: 62; width: 878; height: 511; color: "#151316"
   Rectangle { width: 186; height: parent.height; color: "#211A1E"
    Column { x: 18; y: 24; spacing: 22
     Text { text: "PLACES"; color: "#B3A2A2"; font.pixelSize: 11; font.letterSpacing: 2 }
     Repeater { model: ["Home", "Desktop", "Documents", "Downloads", "Pictures"]
      Rectangle { width: 150; height: 34; radius: 4; color: index === 2 ? "#B82E36" : "transparent"
       Text { x: 12; anchors.verticalCenter: parent.verticalCenter; text: modelData; color: "#F5EDE4"; font.pixelSize: 14 }
      }
     }
    }
   }
   Text { x: 210; y: 24; text: "Home  /  Documents"; color: "#B3A2A2"; font.pixelSize: 14 }
   Row { x: 214; y: 98; spacing: 35
    Repeater { model: ["Projects", "Artwork", "Unit 02"]
     Column { spacing: 16
      Rectangle { width: 106; height: 75; radius: 5; color: index === 2 ? "#B82E36" : "#D99451"
       Rectangle { y: -8; width: 43; height: 16; radius: 3; color: parent.color }
      }
      Text { text: modelData; color: "#F5EDE4"; font.pixelSize: 14 }
     }
    }
   }
   Rectangle { x: 212; y: 259; width: 425; height: 118; radius: 6; color: "#302326"
    Text { x: 18; y: 16; text: "Ready for the next sortie."; color: "#F5EDE4"; font.pixelSize: 18 }
    Text { x: 18; y: 49; text: "Warm surfaces · Scarlet selection · Amber focus"; color: "#B3A2A2"; font.pixelSize: 13 }
    Rectangle { x: 18; y: 84; width: 210; height: 4; radius: 2; color: "#D9443F" }
   }
  }
 }
 Item {
  x: 755; y: 520; width: 780; height: 361
  KSvg.FrameSvgItem { x: -52; y: -11; width: parent.width + 104; height: parent.height + 69; imagePath: "ROOT/aurorae/AsukaRounded/decoration.svg"; prefix: "decoration-inactive" }
  Text { x: 45; y: 34; text: "Konsole — inactive window"; color: "#B3A2A2"; font.pixelSize: 14 }
  Row { x: 634; y: 30; spacing: 6
   Repeater { model: ["minimize", "maximize", "close"]
    KSvg.SvgItem { width: 26; height: 26; imagePath: "ROOT/aurorae/AsukaRounded/" + modelData + ".svg"; elementId: "inactive-center" }
   }
  }
  Rectangle { x: 26; y: 62; width: 728; height: 262; color: "#151316"
   Column { x: 25; y: 22; spacing: 12
    Text { text: "asuka@unit-02  ~  $ theme --status"; color: "#F4BD70"; font.family: "monospace"; font.pixelSize: 16 }
    Text { text: "ASUKA / SCARLET EDITION"; color: "#EF7167"; font.family: "monospace"; font.pixelSize: 18 }
    Text { text: "Palette     Warm dark / scarlet / amber"; color: "#F5EDE4"; font.family: "monospace"; font.pixelSize: 14 }
    Text { text: "Decoration  Circular controls · 6 px corners"; color: "#83BCE8"; font.family: "monospace"; font.pixelSize: 14 }
    Text { text: "Status      All systems ready"; color: "#91C99A"; font.family: "monospace"; font.pixelSize: 14 }
    Row { spacing: 7
     Repeater { model: ["#45373D", "#EF7167", "#91C99A", "#F4BD70", "#83BCE8", "#D6A0C8", "#80C7C5", "#FFF5E8"]
      Rectangle { width: 44; height: 22; color: modelData; radius: 2 }
     }
    }
   }
  }
 }
 Rectangle { x: 48; y: 808; width: 285; height: 116; radius: 6; color: "#211A1E" }
 Text { x: 65; y: 826; text: "WINDOW CONTROLS"; color: "#B3A2A2"; font.pixelSize: 11; font.letterSpacing: 2 }
 Row { x: 65; y: 856; spacing: 18
  Repeater { model: ["active", "hover", "pressed", "inactive"]
   Column { spacing: 9
    KSvg.SvgItem { width: 32; height: 32; imagePath: "ROOT/aurorae/AsukaRounded/close.svg"; elementId: modelData + "-center" }
    Text { text: modelData; color: "#B3A2A2"; font.pixelSize: 11 }
   }
  }
 }
 KSvg.FrameSvgItem { x: 24; y: 946; width: 1552; height: 44; imagePath: "ROOT/plasma/desktoptheme/Asuka/widgets/panel-background.svg"
  Text { x: 22; anchors.verticalCenter: parent.verticalCenter; text: "02   /   ASUKA"; color: "#F4BD70"; font.pixelSize: 14; font.bold: true }
  Text { x: 230; anchors.verticalCenter: parent.verticalCenter; text: "Files          Konsole          System Settings"; color: "#F5EDE4"; font.pixelSize: 13 }
  Text { x: 1390; anchors.verticalCenter: parent.verticalCenter; text: "14:02"; color: "#F5EDE4"; font.pixelSize: 15 }
 }
}'''.replace('ROOT', str(root))
qml = variant_text(qml)
shadow_check = os.environ.get('ASUKA_SHADOW_CHECK') == '1'
if shadow_check:
    qml = qml.replace('color: "#151316"', 'color: "#C8CDD4"', 1)
    qml = qml.replace('Image { anchors.fill: parent;', 'Image { visible: false; anchors.fill: parent;', 1)
component = QQmlComponent(view.engine())
component.setData(qml.encode(), QUrl.fromLocalFile(str(root / 'preview.qml')))
if component.isError():
    raise SystemExit('\n'.join(e.toString() for e in component.errors()))
item = component.create()
view.setContent(QUrl(), component, item)
view.show()

def capture():
    out = root / variant_text('previews/Asuka-shadow-check.png' if shadow_check else 'previews/Asuka-preview.png')
    out.parent.mkdir(exist_ok=True)
    if not view.grabWindow().save(str(out)):
        raise RuntimeError('Could not capture preview')
    if shadow_check:
        app.quit()
        return
    dest = root / variant_text('plasma/look-and-feel/com.omen.asuka/contents/previews')
    dest.mkdir(parents=True, exist_ok=True)
    im = Image.open(out).convert('RGB')
    im.save(dest / 'fullscreenpreview.jpg', quality=92)
    im.thumbnail((960, 600))
    im.save(dest / 'preview.png')
    app.quit()

QTimer.singleShot(1500, capture)
app.exec()
print('Rendered KDE FrameSvg preview: ' + variant_text('previews/Asuka-shadow-check.png' if shadow_check else 'previews/Asuka-preview.png'))

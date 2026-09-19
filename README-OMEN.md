# OMEN Dark — KDE Plasma 主题套件

基于 HP OMEN 品牌配色的完整深色 KDE 主题：近黑灰表面 + OMEN 红强调色，覆盖从窗口装饰到壁纸的整套桌面外观。

## 组件一览

| 组件 | 类型 | 内容 |
| --- | --- | --- |
| `color-schemes/` | 配色方案 | 窗口、视图、按钮、选中、标题栏等颜色 |
| `aurorae/OmenDark/` | 窗口装饰 | 深色标题栏 + 顶部 2px 红色强调线，按钮悬停变红 |
| `plasma/desktoptheme/OmenDark/` | Plasma 风格 | 面板、提示框、对话框等部件配色 |
| `plasma/look-and-feel/com.omen.dark/` | 全局主题 | 一键统一切换所有组件的入口 |
| `konsole/OmenDark.colorscheme` | 终端配色 | 与主题一致的 16 色终端配色 |
| `wallpapers/OmenDark/` | 壁纸 | 深色几何风格 + 红色斜切线条，最高 4K |
| `install.sh` / `uninstall.sh` | 安装/卸载 | 自动安装全部组件到 `~/.local/share` |

## 色板

| 用途 | 颜色 | Hex |
| --- | --- | --- |
| 主背景（窗口/标题栏） | 深灰黑 | `#17171B` |
| 内容背景（视图） | 更深的黑灰 | `#0F0F11` |
| 按钮/卡片背景 | 炭灰 | `#1F1F23` |
| 强调色（选中、焦点、装饰线） | OMEN 红 | `#E31937` |
| 强调色悬停 | 亮红 | `#FF4D5C` |
| 主文字 | 近白 | `#F2F2F4` |
| 次要文字 | 中灰 | `#8A8A93` |
| 链接文字 | 浅红 | `#FF7B8A` |
| 警告 | 琥珀 | `#FFA31A` |
| 成功 | 绿 | `#35C27B` |
| 错误 | 红 | `#E5484D` |

## 安装

### 方式一：一键安装脚本（推荐）

```bash
./install.sh
```

脚本会把所有组件复制到 `~/.local/share` 对应的 KDE 目录。需要卸载时运行 `./uninstall.sh`。

安装后整体应用：

```bash
plasma-apply-lookandfeel -a com.omen.dark
```

如果列表里没有立即出现，先刷新一次缓存：

```bash
kbuildsycoca6 --noincremental
```

### 方式二：系统设置逐个导入

也可以使用 `dist/` 下的安装包，通过系统设置的"从文件安装"导入：

- 颜色：系统设置 → 颜色 → 从文件安装 → `dist/OmenDark.tar.gz`
- 全局主题：系统设置 → 全局主题 → 从文件安装 → `dist/OmenDark-GlobalTheme.zip`
- 窗口装饰：系统设置 → 窗口装饰 → 从文件安装 → `dist/OmenDark-Aurorae.zip`
- Plasma 风格：系统设置 → Plasma 风格 → 从文件安装 → `dist/OmenDark-PlasmaStyle.zip`
- 壁纸：系统设置 → 壁纸 → 添加图片 → 选择 `dist/OmenDark-Wallpaper.zip`

### 方式三：手动复制

```bash
mkdir -p ~/.local/share/{color-schemes,aurorae/themes,plasma/desktoptheme,plasma/look-and-feel,konsole,wallpapers}
cp color-schemes/OmenDark.colors                       ~/.local/share/color-schemes/
cp -r aurorae/OmenDark                                 ~/.local/share/aurorae/themes/
cp -r plasma/desktoptheme/OmenDark                     ~/.local/share/plasma/desktoptheme/
cp -r plasma/look-and-feel/com.omen.dark               ~/.local/share/plasma/look-and-feel/
cp konsole/OmenDark.colorscheme                        ~/.local/share/konsole/
cp -r wallpapers/OmenDark                              ~/.local/share/wallpapers/
```

## 应用

安装完成后，在 **系统设置 → 外观** 中依次选择：

| 设置项 | 选择 |
| --- | --- |
| 颜色 | **Omen Dark** |
| 全局主题 | **OmenDark** |
| Plasma 风格 | **OmenDark** |
| 窗口装饰 | **OmenDark**（也可在装饰按钮里调整按钮位置） |
| 壁纸 | **OmenDark** |
| Konsole | 设置 → 配置文件 → 配色方案 → **OmenDark** |

也可以分项用命令行切换：

```bash
plasma-apply-colorscheme OmenDark
plasma-apply-desktoptheme OmenDark
```

## 目录结构

```text
.
├── OmenDark.colors                        # 配色方案（根目录副本）
├── install.sh                             # 安装脚本
├── uninstall.sh                           # 卸载脚本
├── color-schemes/
│   └── OmenDark.colors
├── aurorae/
│   └── OmenDark/                          # 窗口装饰
│       ├── decoration.svg                 # 边框 + 阴影
│       ├── close.svg / maximize.svg / ... # 按钮（含各状态）
│       ├── OmenDarkrc                     # 布局配置
│       └── metadata.json / metadata.desktop
├── plasma/
│   ├── desktoptheme/OmenDark/             # Plasma 部件风格
│   │   ├── colors
│   │   └── widgets/ dialogs/
│   └── look-and-feel/com.omen.dark/       # 全局主题
│       ├── metadata.json
│       └── contents/defaults
├── konsole/
│   └── OmenDark.colorscheme
├── wallpapers/
│   ├── OmenDark/                          # KDE 壁纸包（含 4K/2K/1080p）
│   └── OmenDark-source.svg                # 壁纸矢量源文件
└── dist/                                  # 各组件安装包
```

## 兼容性

- 面向 KDE Plasma 5.27+ / Plasma 6，Aurorae 窗口装饰对 Plasma 5.8+ 同样可用。
- 窗口装饰同时提供 `metadata.json` 与 `metadata.desktop`，新旧 KWin 都能识别。
- Plasma 风格只覆盖面板、提示框、对话框等高频部件，其余部件自动回落到默认 Breeze 风格。
- 全局主题不强制更改图标、光标和字体，保留你现有的选择。
- 配色中保留了语义色（错误/警告/成功），方便终端、文件管理器等使用。

## 许可证

主题文件基于 GPL v3 发布；SVG 部件文件基于 LGPL。可自由修改与分发。

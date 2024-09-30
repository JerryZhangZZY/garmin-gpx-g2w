# garmin-gpx-g2w

在 Garmin Connect 上创建的路线采用的是按照中国法律法规所规定的火星坐标系（GCJ-02），而佳明设备使用国际通用的地球坐标系（WGS-84），因此将该 `.gpx` 文件同步到佳明设备上时坐标会发生偏移，需要对文件进行坐标系转换。

写了个简单的图形化界面，方便不熟悉计算机的朋友们快速对路线文件进行转换。

## 快速开始

### Linux（macOS）

直接下载运行 [Releases](https://github.com/JerryZhangZZY/garmin-gpx-g2w/releases/latest) 中的 `Garmin GPX Coordinate Converter` 应用程序。

### Windows

由于手头暂时没有 PC，无法将 Python 脚本打包成 `.exe`，需要本地解释器运行 `converter.py`。请确保本地已配置好 Python 环境，并安装 GUI 库：

```bash
pip3 install tk
```

Clone 或下载项目压缩包，在项目根目录下直接运行 `converter.py`:

```bash
python converter.py
```

也可以先使用 `PyInstaller` 打包成可执行文件，方便以后使用：

```bash
pip3 install pyinstaller
pyinstaller --onefile --windowed --name "Garmin GPX Coordinate Converter" --icon=icon.ico converter.py
```

打包成功后就可以在 `dist` 目录下找到 `Garmin GPX Coordinate Converter.exe` 了

## 如何使用

1. 在 Garmin Connect 中下载路线的 `.gpx` 文件。
2. 打开程序，点击 <kbd>Upload GPX Files</kbd> 按钮，选择您需要转换的一个或多个 `.gpx` 文件。
3. 转换成功后会自动跳转至文件目录，将转换后的文件手动添加至 Garmin Connect 中。
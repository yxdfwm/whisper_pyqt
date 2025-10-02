# Whisper SRT 字幕生成器

## 项目简介

这是一个基于 **OpenAI Whisper** 的字幕生成工具，带有 **PyQt6 UI**，功能包括：

- 拖拽音视频文件直接处理  
- 选择 Whisper 模型大小（tiny / base / small / medium / large）  
- 语言选择（自动 / 中文 / 英文 / 日语 / 韩语等）  
- 中文自动 **繁体转简体**  
- 生成标准 **SRT 字幕文件**，保存在视频同目录  
- 同步显示字幕到 **UI 文本框** 和 **控制台**  
- 程序自动检测并安装缺失的依赖库  

---

## 安装与依赖

程序会在启动时自动检测并安装缺失的依赖库，包括：

- `whisper`  
- `opencc-python-reimplemented`  
- `srt`  
- `PyQt6`  

如果需要手动安装，也可以运行：

```bash
pip install whisper opencc-python-reimplemented srt PyQt6
```

> 注意：Whisper 模型可能需要较多磁盘空间，根据模型大小下载。

---

## 使用方法

1. **运行程序**  

```bash
python main.py
```

2. **拖拽音视频文件**到窗口（支持 `.mp3, .wav, .mp4, .mov, .m4a`）  
3. **选择模型大小**（tiny / base / small / medium / large）  
4. **选择语言**（auto / Chinese / English / Japanese / Korean 等）  
5. 点击 **“开始生成 SRT 字幕”**  
6. 程序会在视频文件同目录生成 `.srt` 文件，同时在 **文本框** 和 **控制台** 显示字幕  

---

## 输出说明

- SRT 文件命名与原视频文件相同，例如：

```
video.mp4  ->  video.srt
```

- 中文字幕会自动转换为 **简体中文**  
- 支持多文件批量处理  

---

## 文件结构示例

```
project_folder/
├─ main.py                # 主程序
├─ README.md              # 项目说明
├─ video.mp4              # 测试视频
├─ video.srt              # 生成的字幕文件
```

---

## 注意事项

- 需要 Python 3.10+  
- 大模型（medium / large）可能占用较多内存，推荐 GPU 环境  
- 自动安装依赖需要联网  


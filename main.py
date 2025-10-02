import sys
import subprocess

# =======================
# 自动安装依赖
# =======================
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# 需要安装的包及对应模块名
packages = {
    "whisper": "whisper",
    "opencc-python-reimplemented": "opencc",
    "srt": "srt",
    "PyQt6": "PyQt6"
}

# 检查并安装
for pkg, module_name in packages.items():
    try:
        __import__(module_name)
    except ImportError:
        print(f"缺少依赖 {pkg}，正在安装...")
        install(pkg)
        __import__(module_name)  # 安装后立即导入

# =======================
# 导入库
# =======================
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QComboBox, QVBoxLayout, QTextEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import whisper
import srt
from datetime import timedelta
from opencc import OpenCC

# =======================
# 后台线程处理转写
# =======================
class TranscribeThread(QThread):
    update_text = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, files, model_name, language):
        super().__init__()
        self.files = files
        self.model_name = model_name
        self.language = language
        self.cc = OpenCC('t2s')  # 繁体转简体

    def run(self):
        model = whisper.load_model(self.model_name)
        for file_path in self.files:
            filename = os.path.basename(file_path)
            msg = f"正在处理：{filename} ({self.language})\n"
            self.update_text.emit(msg)
            print(msg, end='')

            result = model.transcribe(file_path, language=self.language)

            subtitles = []
            for i, segment in enumerate(result["segments"], start=1):
                start = timedelta(seconds=segment["start"])
                end = timedelta(seconds=segment["end"])
                text = segment["text"].strip()
                if self.language.lower() in ["chinese", "zh", "zh-cn"]:
                    text = self.cc.convert(text)
                subtitles.append(srt.Subtitle(index=i, start=start, end=end, content=text))

            srt_text = srt.compose(subtitles)
            self.update_text.emit(srt_text + "\n")
            print(srt_text)

            # 保存 SRT 文件
            srt_filename = os.path.splitext(file_path)[0] + ".srt"
            with open(srt_filename, "w", encoding="utf-8") as f:
                f.write(srt_text)
            save_msg = f"SRT 文件已保存：{srt_filename}\n"
            self.update_text.emit(save_msg)
            print(save_msg, end='')

        finish_msg = "全部文件处理完成！\n"
        self.update_text.emit(finish_msg)
        print(finish_msg, end='')
        self.finished.emit()

# =======================
# 主界面
# =======================
class WhisperUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Whisper SRT 字幕生成器（自动依赖安装 + 中文简体转换）")
        self.setGeometry(300, 300, 700, 500)
        self.setAcceptDrops(True)

        # 模型选择
        self.model_label = QLabel("模型大小：")
        self.model_combo = QComboBox()
        self.model_combo.addItems(["tiny", "base", "small", "medium", "large"])

        # 语言选择
        self.lang_label = QLabel("语言：")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems([
            "auto", "Chinese", "English", "Japanese", "Korean",
            "French", "German", "Spanish", "Russian"
        ])

        # 开始按钮
        self.start_btn = QPushButton("开始生成 SRT 字幕")
        self.start_btn.clicked.connect(self.start_transcribe)

        # 日志显示
        self.log = QTextEdit()
        self.log.setReadOnly(True)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.model_label)
        layout.addWidget(self.model_combo)
        layout.addWidget(self.lang_label)
        layout.addWidget(self.lang_combo)
        layout.addWidget(self.start_btn)
        layout.addWidget(QLabel("SRT 字幕输出："))
        layout.addWidget(self.log)
        self.setLayout(layout)

        self.files_to_process = []

    # 拖拽事件
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        for url in urls:
            path = url.toLocalFile()
            if os.path.isfile(path) and path.lower().endswith((".mp3", ".wav", ".mp4", ".mov", ".m4a")):
                self.files_to_process.append(path)
                self.log.append(f"已添加文件：{os.path.basename(path)}")
                print(f"已添加文件：{os.path.basename(path)}")
        if self.files_to_process:
            self.log.append("准备处理这些文件...\n")
            print("准备处理这些文件...\n")

    # 开始处理
    def start_transcribe(self):
        if not self.files_to_process:
            self.log.append("请拖拽音视频文件到窗口！\n")
            print("请拖拽音视频文件到窗口！\n")
            return

        model_name = self.model_combo.currentText()
        language = self.lang_combo.currentText()
        self.start_btn.setEnabled(False)

        self.thread = TranscribeThread(self.files_to_process, model_name, language)
        self.thread.update_text.connect(self.log.append)
        self.thread.finished.connect(self.on_finished)
        self.thread.start()

    def on_finished(self):
        self.start_btn.setEnabled(True)
        self.files_to_process = []

# =======================
# 运行程序
# =======================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WhisperUI()
    window.show()
    sys.exit(app.exec())